#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
Training script for DVS128 spatiotemporal TENNs.
"""

import os
import argparse
import numpy as np
import tensorflow as tf
from tqdm import tqdm

import akida
from cnn2snn import convert

from quantizeml.layers import BufferTempConv, DepthwiseBufferTempConv
from quantizeml.models import reset_buffers
from quantizeml.models.transforms.transforms_utils import get_layers_by_type

from ..param_scheduler import CosineDecayWithLinearWarmup
from ..training import get_training_parser, print_history_stats, RestoreBest, save_model
from ..utils import get_tensorboard_callback
from ..model_io import load_model
from .img_utils import extract_samples, get_random_affine
from .dvs128_preprocessing import GestureSequence
from .temporal_training_tools import TemporalSparseCategoricalCrossentropy, TemporalAccuracy


def get_data(input_shape, data_path, batch_size, frames_per_segment):
    """ Loads DVS128 gesture_experimentaldata.

    Args:
        input_shape (tuple): spatial shape for inputs
        data_path (str): path to data
        batch_size (int): the batch size
        frames_per_segment (int): number of frames per segment.
            to yield full length trials (don't divide into separate segments).

    Returns:
        tensorflow.dataset, tensorflow.dataset, int, int, int: train and test datasets, train
        and validation steps, validation length
    """
    seq_train = GestureSequence(input_shape, data_path, True,
                                frames_per_segment=frames_per_segment)
    n_train = len(seq_train)
    seq_test = GestureSequence(input_shape, data_path, False,
                               frames_per_segment=frames_per_segment)
    n_test = len(seq_test)

    # (T, H, W, C)
    input_signature_sequence = (
        tf.TensorSpec(shape=(seq_test.frames_per_segment,) + input_shape, dtype=tf.float32),
        tf.TensorSpec(shape=(), dtype=tf.int64))

    # dummy train and test sets generators
    def train_gen():
        for i in range(n_train):
            yield seq_train[i]

    def test_gen():
        for i in range(n_test):
            yield seq_test[i]

    # define preprocessing
    random_affine = get_random_affine(*input_shape[:2])

    # build datasets
    train_ds = tf.data.Dataset.from_generator(train_gen, output_signature=input_signature_sequence)
    train_ds = train_ds.repeat().map(random_affine, num_parallel_calls=tf.data.AUTOTUNE)
    train_ds = train_ds.batch(batch_size, drop_remainder=True).prefetch(tf.data.AUTOTUNE)

    test_ds = tf.data.Dataset.from_generator(test_gen, output_signature=input_signature_sequence)
    test_ds = test_ds.cache().batch(batch_size).prefetch(tf.data.AUTOTUNE)

    return (train_ds, test_ds, n_train // batch_size, n_test // batch_size, seq_test.num_frames)


def train_model(model, train_ds, val_ds, steps_per_epoch, epochs):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train
        train_ds (tensorflow.dataset): train data
        val_ds (tensorflow.dataset): validation data
        steps_per_epoch (int): training steps
        epochs (int): the number of epochs
    """
    # Model checkpoints (save best model and retrieve it when training is complete)
    callbacks = [RestoreBest(model, monitor='val_temporal_accuracy')]

    # Add Tensorboard logs
    tensorboard = get_tensorboard_callback('logs', prefix='dvs128')
    callbacks.append(tensorboard)

    history = model.fit(x=train_ds,
                        validation_data=val_ds,
                        epochs=epochs,
                        steps_per_epoch=steps_per_epoch,
                        callbacks=callbacks)
    print_history_stats(history)


def compile_model(model, total_steps, base_learning_rate):
    """ Compiles the model.

    Args:
        model (keras.Model): the model to compile
        total_steps (int): number of training steps
        base_learning_rate (float): base learning rate
    """
    warmup_ratio = 0.025
    scheduler = CosineDecayWithLinearWarmup(base_learning_rate, warmup_ratio, total_steps)
    optimizer = tf.keras.optimizers.Adam(learning_rate=scheduler)

    model.compile(optimizer=optimizer,
                  loss=TemporalSparseCategoricalCrossentropy(from_logits=True),
                  metrics=[TemporalAccuracy()])


def evaluate_bufferized_model(model, val_ds, val_steps, length, in_akida=False):
    """ Evaluates the model.

    Args:
        model (keras.model): model to evaluate
        val_ds (tf.dataset): validation data
        val_steps (int): number of validation steps.
        length (int): length of input data
        in_akida (bool, optional): True when the evaluation is done with akida.
            Defaults to False.
    """
    if in_akida:
        model = convert(model)
    else:
        model_f = tf.function(model)

    # Manual evaluation routine to prevent compilation
    correct, total = 0, 0
    for frame_id, (frame, label) in enumerate(tqdm(val_ds, total=val_steps)):
        # Reset buffers at the start of each segment. By default a segment is now the full sample
        # in the Bufferized mode.
        if not frame_id % length:
            if in_akida:
                model = akida.Model(model.layers)
            else:
                reset_buffers(model)

        if in_akida:
            frame = frame.numpy().astype(np.int8)
            prediction = model.forward(frame[0])
        else:
            prediction = model_f(frame[0])

        total += 1
        correct += tf.math.reduce_sum(tf.cast(tf.math.argmax(prediction, -1) == label[0],
                                              tf.int32)).numpy()

    print(f"Accuracy: {correct / total * 100: .2f}%")


def main():
    """ Entry point for script and CLI usage.

    Note: [DVS128](https://research.ibm.com/interactive/dvsgesture/): can be downloaded and
    processed / binned using
    [`tonic.datasets.DVSGesture`](https://tonic.readthedocs.io/en/latest/generated/tonic.datasets.DVSGesture.html).
    """  # noqa: E501
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("-d", "--data", type=str, default="./dvs128_dataset",
                               help="Path to save the DVS128 gesture_experimental dataset.")
    global_parser.add_argument("--lr", type=float, default=2e-3,
                               help="base learning rate")
    global_parser.add_argument("-fs", type=int, default=None,
                               help="Number of frames per segment")
    parsers = get_training_parser(batch_size=32, extract=True, global_parser=global_parser)

    args = parsers[0].parse_args()

    # Load the source model
    model = load_model(args.model)

    is_bufferized = get_layers_by_type(model, (BufferTempConv, DepthwiseBufferTempConv))

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    batch_size = args.batch_size
    if args.action == "extract" or not is_bufferized:
        batch_size = args.batch_size
    else:
        batch_size = 1
    if args.fs is not None:
        frames_per_segment = args.fs
    else:
        frames_per_segment = 1 if is_bufferized else model.input_shape[1]

    train_ds, val_ds, train_steps, val_steps, length = get_data(model.input_shape[-3:],
                                                                args.data,
                                                                batch_size,
                                                                frames_per_segment)

    # Train model
    if args.action == "train":
        if is_bufferized:
            raise NotImplementedError("Training of bufferized model is not supported.")
        total_steps = train_steps * args.epochs
        compile_model(model, total_steps, args.lr)
        train_model(model, train_ds, val_ds, train_steps, args.epochs)
        save_model(model, args.model, args.savemodel, args.action)
    elif args.action == "eval":
        if is_bufferized:
            evaluate_bufferized_model(model, val_ds, val_steps, length, args.akida)
        else:
            total_steps = val_steps
            compile_model(model, total_steps, args.lr)
            history = model.evaluate(val_ds, steps=val_steps)
            print(history)
    elif args.action == 'extract':
        extract_samples(train_ds, args.batch_size, args.savefile)


if __name__ == "__main__":
    main()
