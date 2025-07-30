#!/usr/bin/env python
# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
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
Training script for the Event-based Eye Tracking AI for Streaming CVPR 2024 Challenge
"""

import argparse
import numpy as np
import tensorflow as tf

from tqdm import tqdm
from functools import partial

import akida
from cnn2snn import convert
from quantizeml.layers import BufferTempConv, DepthwiseBufferTempConv
from quantizeml.models import reset_buffers
from quantizeml.models.transforms.transforms_utils import get_layers_by_type

from ..model_io import load_model
from ..param_scheduler import CosineDecayWithLinearWarmup
from ..utils import get_tensorboard_callback
from ..training import print_history_stats, save_model, get_training_parser, RestoreBest
from .eye_preprocessing import generate_dir_paths, load_data, preprocess_data, split_trial
from .eye_losses import EyeLosses, P10Accuracy, process_detector_prediction
from .img_utils import extract_samples


def get_data(root_path, mode='train', batch_size=32,
             frames_per_segment=50, spatial_downsample=(6, 6),
             time_window=10000):
    """ Load and preprocess the EyeTracking data in a tf.dataset.

    Args:
        root_path (str): path to data
        mode (str, optional): Possible values : ['train', 'val', 'test'].
            A flag indicating the mode in which the function is being called. Defaults to 'train'.
        batch_size (int, optional): the batch size. Defaults to 32.
        frames_per_segment (int, optional): The number of frames to segment the event data into.
            Defaults to 50.
        spatial_downsample (tuple of int, optional): A tuple containing two integers representing
            the downsampling factors for the height and width dimensions. Defaults to (6, 6).
        time_window (float, optional): The time window in microseconds for aggregating events into
            frames. Defaults to 10000.

    Returns:
        tf.dataset, int : dataset, steps per epoch.
    """
    segments, labels = load_data(
        root_path, mode, frames_per_segment, time_window
    )
    total_steps = sum([lbl.shape[0] // frames_per_segment for lbl in labels])

    # Generator function for training dataset. The split_trial method is applied sequentially
    # on each sample of the dataset to handle correctly the random spatial scale and shift
    # data augmentation.
    def train_data_generator():
        for event, label in zip(segments, labels):
            # Apply split_trial at each epoch
            event_processed, label_processed = split_trial(
                event, label, True, frames_per_segment, time_window
            )
            for ep, lp in zip(event_processed, label_processed):
                yield ep, lp

    # Generator function for the validation dataset. Since no data augmentation is applied to
    # the validation dataset, the easiest solution is to handle the Ragged tensors preprocessing
    # outside the graph and keep only the preprocessing that occurs on the consistent
    # shaped Tensors. Doing so the validation step can be processed when calling the fit method
    # without any potential shape inconsistency error.
    def val_data_generator():
        for event, label in zip(segments, labels):
            yield event, label

    input_signature_sequence = (tf.TensorSpec(shape=(4, None), dtype=tf.float32),
                                tf.TensorSpec(shape=(None, 3), dtype=tf.float32))

    partial_processing = partial(preprocess_data,
                                 train_mode=mode == 'train',
                                 frames_per_segment=frames_per_segment,
                                 spatial_downsample=spatial_downsample,
                                 time_window=time_window)
    if mode == 'train':
        dataset = tf.data.Dataset.from_generator(
            train_data_generator, output_signature=input_signature_sequence)
        # Apply the preprocessing function
        expanded_dataset = dataset.map(partial_processing, num_parallel_calls=tf.data.AUTOTUNE)
        expanded_dataset = expanded_dataset.repeat().batch(batch_size).prefetch(tf.data.AUTOTUNE)
    else:
        dataset = tf.data.Dataset.from_generator(
            val_data_generator, output_signature=input_signature_sequence)
        # Apply the preprocessing function
        expanded_dataset = dataset.map(partial_processing, num_parallel_calls=tf.data.AUTOTUNE)
        expanded_dataset = expanded_dataset.batch(batch_size).prefetch(
            tf.data.AUTOTUNE)

    return expanded_dataset, total_steps // batch_size


def train(model, train_dataset, val_dataset, steps_per_epoch,
          validation_steps, epochs):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train
        train_dataset (tensorflow.dataset): train data
        val_dataset (tensorflow.dataset): validation data
        steps_per_epoch (int): training steps
        validation_steps (int): validation steps
        epochs (int): the number of epochs
    """
    # Model checkpoints (save best model and retrieve it when training is complete)
    callbacks = [RestoreBest(model, monitor='val_mean_distance', mode="min")]

    # Add Tensorboard logs
    tensorboard = get_tensorboard_callback('logs', prefix='eye_tracking')
    callbacks.append(tensorboard)

    # Train model
    history = model.fit(train_dataset,
                        steps_per_epoch=steps_per_epoch,
                        epochs=epochs,
                        validation_data=val_dataset,
                        validation_steps=validation_steps,
                        callbacks=callbacks,
                        verbose=1)
    print_history_stats(history)


def compile_model(model, learning_rate, batch_size, steps_per_epoch, epochs):
    """ Compiles the model.

    Args:
        model (keras.Model): the model to compile
        learning_rate (int): training optimizer learning rate
        batch_size (int): batch size
        steps_per_epoch (float): training steps per epoch
    """
    scheduler = CosineDecayWithLinearWarmup(base_learning_rate=learning_rate,
                                            warmup_ratio=0.025,
                                            total_steps=steps_per_epoch * epochs)
    optimizer = tf.keras.optimizers.experimental.AdamW(learning_rate=scheduler,
                                                       weight_decay=0.001)
    model.compile(optimizer=optimizer,
                  loss=EyeLosses(batch_size),
                  metrics=[P10Accuracy(metric='within_tolerance', name='p10acc'),
                           P10Accuracy(metric='within_tolerance_noblinks', name='p10acc_noblinks'),
                           P10Accuracy(metric='mean_distance', name='mean_distance')])


def evaluate_bufferized_model(model, root_path, in_akida=False):
    """ Evaluates the model.

    Args:
        model (keras.model): The model to evaluate
        root_path (str): The path of the folder containing the validation files.
        in_akida (bool, optional): True if the validation is done with Akida. Defaults to False.
    """
    dir_paths = generate_dir_paths(root_path, 'test')

    distances = {}
    distances_noblinks = {}
    all_distances = []
    all_dist_noblinks = []
    p10 = {}
    p10_noblinks = {}

    if in_akida:
        model = convert(model)
    else:
        model_f = tf.function(model)

    for dir_path in tqdm(dir_paths):

        # Files contain different track lengths,
        # hence loading on by one to compute accuracy and average over all files.
        val_dataset, val_steps = get_data(
            root_path=dir_path, mode='buffer', batch_size=1, frames_per_segment=1)

        collected_distances = []
        collected_dist_noblinks = []

        for frame, label in tqdm(val_dataset, total=val_steps):

            if in_akida:
                frame = frame.numpy().astype(np.int8)
                pred = model.forward(frame[0])
            else:
                pred = model_f(frame[0])

            x, y, openness = tf.unstack(tf.squeeze(label), axis=0)
            center = tf.expand_dims(tf.stack([x, y], axis=0), 0)
            pred = process_detector_prediction(tf.expand_dims(pred, 0))
            y_pred_x = pred[:, 0] * 80
            y_pred_y = pred[:, 1] * 60
            center_x = center[:, 0] * 80
            center_y = center[:, 1] * 60
            distance = tf.sqrt(tf.square(center_x - y_pred_x) +
                               tf.square(center_y - y_pred_y)).numpy()[0, 0]
            collected_distances.append(distance)
            if openness.numpy() == 1.:
                collected_dist_noblinks.append(distance)

        distances[dir_path] = collected_distances
        all_distances += collected_distances
        distances_noblinks[dir_path] = collected_dist_noblinks
        all_dist_noblinks += collected_dist_noblinks
        p10[dir_path] = (np.array(collected_distances) < 10).sum() / len(collected_distances)
        p10_noblinks[dir_path] = ((np.array(collected_dist_noblinks) < 10).sum() /
                                  len(collected_dist_noblinks))

        if in_akida:
            model = akida.Model(model.layers)
        else:
            reset_buffers(model)

    print(f"overall mean distance: {np.mean(all_distances)}")
    print(f"overall p10: {(np.array(all_distances) < 10).sum() / len(all_distances)}")
    len_dist_nob = len(all_dist_noblinks)
    print(f"overall mean distance noblinks: {np.mean(all_dist_noblinks)}")
    print(f"overall p10_noblinks: {((np.array(all_dist_noblinks) < 10).sum() / len_dist_nob)}")


def main():
    global_parser = argparse.ArgumentParser(add_help=False,
                                            description='Eye tracking model training script')
    global_parser.add_argument('-d',
                               '--data',
                               type=str,
                               help='Path to the data')
    global_parser.add_argument("-fs", type=int, default=50,
                               help="Number of frames per segment")
    parsers = get_training_parser(batch_size=32, extract=True, global_parser=global_parser)

    args = parsers[0].parse_args()
    model = load_model(args.model)

    if args.data is None or args.data == "":
        raise ValueError("data path should be specified in args.data")

    is_bufferized = get_layers_by_type(model, (BufferTempConv, DepthwiseBufferTempConv))

    # Align the learning rate with the batch size
    # For a batch_size of 32, the optimal lr is 0.002
    lr = args.batch_size * 0.002 / 32
    if args.action == "train":
        if is_bufferized:
            raise NotImplementedError("Training of bufferized model is not supported.")
        # Load the datasets.
        train_dataset, steps_per_epoch = get_data(
            root_path=args.data, mode='train', batch_size=args.batch_size,
            frames_per_segment=args.fs)
        val_dataset, val_steps = get_data(
            root_path=args.data, mode='val', batch_size=args.batch_size,
            frames_per_segment=args.fs)
        # Compile the model
        compile_model(model, lr, args.batch_size, steps_per_epoch, args.epochs)
        train(model, train_dataset, val_dataset, steps_per_epoch, val_steps, args.epochs)
        save_model(model, args.model, args.savemodel, args.action)

    elif args.action == "eval":
        if args.akida or is_bufferized:
            evaluate_bufferized_model(model, args.data, in_akida=args.akida)
        else:
            # Load the dataset.
            val_dataset, val_steps = get_data(
                root_path=args.data, mode='test', batch_size=args.batch_size,
                frames_per_segment=args.fs)
            # Compile the model
            compile_model(model, lr, args.batch_size, val_steps, 1)
            history = model.evaluate(val_dataset, steps=val_steps)
            print(history)

    elif args.action == 'extract':
        train_dataset, _ = get_data(
            root_path=args.data, mode='train', batch_size=args.batch_size,
            frames_per_segment=args.fs)
        extract_samples(train_dataset, args.batch_size, out_file=args.savefile)


if __name__ == "__main__":
    main()
