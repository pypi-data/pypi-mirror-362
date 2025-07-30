#!/usr/bin/env python
# ******************************************************************************
# Copyright 2025 Brainchip Holdings Ltd.
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
Training script Jester Gesture Recognition Challenge
"""
import os
import csv
import argparse
import tensorflow as tf
import numpy as np
from glob import glob
from tqdm import tqdm
from scipy.special import softmax
from collections import namedtuple

import akida
from cnn2snn import convert
from quantizeml.layers import BufferTempConv, DepthwiseBufferTempConv
from quantizeml.models import reset_buffers
from quantizeml.models.transforms.transforms_utils import get_layers_by_type

from ..model_io import load_model
from ..utils import get_tensorboard_callback
from ..training import save_model, get_training_parser, print_history_stats
from ..param_scheduler import CosineDecayWithLinearWarmup
from .img_utils import extract_samples, get_random_affine
from .temporal_training_tools import TemporalCategoricalCrossentropy, TemporalAccuracy


def _read_csv_labels(csv_path):
    """ Extract all classes from the dataset.

    Args:
        csv_path (str): which file to load.

    Returns:
        classes (list): list of the classes.
    """
    classes = []
    with open(csv_path) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            classes.append(row[0])
    return classes


def _read_csv_input(csv_path, classes):
    """ Reads the cvsfile containing the info about the videos in the
        split and returns a list with a tuple containing the ["id","label","path"].

    Args:
        csv_path (str): which file to load.
        classes (list): list of the classes.

    Returns:
        csv_data (list of tuple): loaded data from the csv files.
    """
    ListDataJpeg = namedtuple('ListDataJpeg', ['id', 'label', 'path'])
    data_path = os.path.dirname(csv_path)
    csv_data = []
    with open(csv_path) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
            item = ListDataJpeg(row[0], row[1], os.path.join(data_path, row[0]))
            if row[1] in classes:
                csv_data.append(item)
    return csv_data


def _parse_single_sequence_example(example):
    """Parses a single TFRecord sequence example into its constituent parts.

    Args:
        example (tf.train.Example): A serialized TFRecord example containing
            video frames and metadata.

    Returns:
        frames (tf.Tensor): Tensor containing the encoded video frames.
        label (tf.Tensor): Integer label associated with the video.
        shape (tuple): A tuple representing the videos shape
            as (frame_count, height, width, depth).
    """
    sequence_features = {
        'frames': tf.io.FixedLenSequenceFeature([], dtype=tf.string)
    }
    context_features = {
        'filename': tf.io.FixedLenFeature([], tf.string),
        'height': tf.io.FixedLenFeature([], tf.int64),
        'width': tf.io.FixedLenFeature([], tf.int64),
        'depth': tf.io.FixedLenFeature([], tf.int64),
        'frame_count': tf.io.FixedLenFeature([], tf.int64),
        'label': tf.io.FixedLenFeature([], tf.int64),
    }
    # Parse the input tf.train.Example using the dictionary above.
    # decouples sequence and context features
    context, sequence = tf.io.parse_single_sequence_example(example,
                                                            context_features=context_features,
                                                            sequence_features=sequence_features)

    # extract the output tuple
    frames = sequence['frames']
    label = context['label']
    shape = (
        context['frame_count'],
        context['height'],
        context['width'],
        context['depth'])
    return frames, label, shape


def _decode_image(encoded_buffer, label, shape, frames_per_video, step_size,
                  mode, target_shape, n_classes):
    """Decodes and processes image frames from a TFRecord for video data handling.

    Args:
        encoded_buffer (tf.Tensor): Tensor containing encoded JPEG frames from the TFRecord.
        label (int): Integer label for the video.
        shape (tuple): Shape of the video as (frame_count, height, width, depth).
        frames_per_video (int): Number of frames to sample from each video.
            If -1, all frames are used.
        step_size (int): Step size for frame sampling (e.g., 2 loads every other frame).
        mode (str): mode (str): ["val", "train"]. If train, apply a random offset.
        target_shape (list of int): Target height and width for resizing each frame.
        n_classes (int): Total number of classes for one-hot encoding the label.

    Returns:
        tf.Tensor: A tensor of decoded and resized frames of shape
            (frames_per_video, target_height, target_width, 3).
        tf.Tensor: One-hot encoded label tensor of shape (n_classes,).
    """
    # randomly sample the frames from the total available frames
    total_frames = tf.cast(shape[0], dtype=tf.int32)
    if frames_per_video == -1:
        frames_per_video = total_frames
        step_size = 1
    # add a temporal offset
    offset = 0
    if mode == "train":
        num_frames_necessary = tf.math.multiply(frames_per_video, step_size)
        # If there are more frames, then sample starting offset
        diff = (total_frames - num_frames_necessary)
        if diff > 0:
            offset = tf.random.uniform([], 0, diff, dtype=tf.int32)
    indices = tf.range(offset, offset + frames_per_video *
                       (step_size), step_size)
    indices = tf.math.floormod(indices, total_frames)
    # Initialize frames tensor with the expected shape
    frames = tf.TensorArray(tf.uint8, size=frames_per_video)
    counter = 0
    for idx in indices:
        img = tf.io.decode_jpeg(tf.gather(encoded_buffer, [idx])[0])
        # to resize we need to cast
        img32 = tf.image.convert_image_dtype(img, tf.float32)
        img32 = tf.image.resize_with_crop_or_pad(img32, target_shape[0], target_shape[1])
        imgu8 = tf.image.convert_image_dtype(img32, dtype=tf.uint8)
        frames = frames.write(counter, imgu8)
        counter += 1
    frames = frames.stack()
    return frames, tf.one_hot(label, n_classes)


def get_data(mode, data_path, frames_per_video, target_shape, batch_size, step_size=2):
    """ Creates a TensorFlow dataset for video data processing,
        supporting both training and evaluation modes.

    Args:
        mode (str): ["val", "train"] to load the corresponding split.
        data_path (str): path to the data
        frames_per_video (int): number of frames to get from each video
        target_shape (list of int): list containing the target_height and the targeth_width of the
            after resize.
        batch_size (int, optional): Number of samples per batch. Defaults to 32.
        step_size (int): acts as a stride, e.g. if 2, then only load every other image.

    Returns:
        tf.data.Dataset: A batched dataset with optional augmentations for training.
    """
    if mode not in ["train", "val"]:
        raise ValueError(f"{mode=} should be [train, val]")
    classes = _read_csv_labels(os.path.join(data_path, "jester-v1-labels.csv"))
    if mode == "val":
        csv_path_input = os.path.join(data_path, "jester-v1-validation.csv")
    else:
        csv_path_input = os.path.join(data_path, "jester-v1-train.csv")
    csv_data = _read_csv_input(csv_path_input, classes)
    n_samples = len(csv_data)
    records_path = os.path.join(data_path, 'tfrecords')
    n_classes = len(classes)
    filenames = sorted(glob(os.path.join(records_path, f'*{mode}*')))
    AUTOTUNE = tf.data.AUTOTUNE
    dataset = tf.data.TFRecordDataset(filenames, compression_type="GZIP")
    dataset = dataset.map(_parse_single_sequence_example)
    dataset = dataset.map(lambda encoded_buffer, label, shape: _decode_image(
        encoded_buffer, label, shape, frames_per_video, step_size, mode, target_shape, n_classes),
                            num_parallel_calls=AUTOTUNE)
    if mode == "train":
        # apply affine augment for train only
        random_affine = get_random_affine(height=None, width=None)
        dataset = dataset.repeat().map(random_affine, num_parallel_calls=AUTOTUNE)

    dataset = dataset.batch(batch_size)
    return dataset, n_samples // batch_size


def train(model, train_dataset, val_dataset, steps_per_epoch, validation_steps, epochs):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train
        train_dataset (tensorflow.dataset): train data
        val_dataset (tensorflow.dataset): validation data
        steps_per_epoch (int): training steps
        validation_steps (int): validation steps
        epochs (int): the number of epochs
    """
    callbacks = [get_tensorboard_callback('logs', prefix="jester")]
    history = model.fit(train_dataset,
                        steps_per_epoch=steps_per_epoch,
                        epochs=epochs,
                        validation_data=val_dataset,
                        validation_steps=validation_steps,
                        callbacks=callbacks,
                        verbose=1)
    print_history_stats(history)


def compile_model(model, learning_rate, steps_per_epoch, epochs, frames_per_segment):
    """ Compiles the model.

    Args:
        model (keras.Model): the model to compile.
        learning_rate (int): training optimizer learning rate.
        steps_per_epoch (float): training steps per epoch.
        epochs (int): Total number of epochs for training.
        frames_per_segment (int): Number of time steps (frames) per segment,
            used in the temporal loss.
    """
    scheduler = CosineDecayWithLinearWarmup(base_learning_rate=learning_rate,
                                            warmup_ratio=0.025,
                                            total_steps=steps_per_epoch * epochs)
    optimizer = tf.keras.optimizers.experimental.AdamW(learning_rate=scheduler, weight_decay=0.001,
                                                       epsilon=1e-8)
    model.compile(optimizer=optimizer,
                  loss=TemporalCategoricalCrossentropy(from_logits=True, label_smoothing=0.1,
                                                       num_time_steps=frames_per_segment),
                  metrics=[TemporalAccuracy(is_sparse=False, axis=0)])


def evaluate_bufferized_model(model, val_ds, val_steps, in_akida=False, n_classes=27):
    """ Evaluates the model.

    Args:
        model (keras.model): model to evaluate.
        val_ds (tf.dataset): validation data.
        val_steps (int): number of validation steps.
        in_akida (bool, optional): True when the evaluation is done with akida.
            Defaults to False.
        n_classes (int, optional): Number of classes of the classifier. Defaults to 27.
    """
    decay_factor = 0.8
    if in_akida:
        model = convert(model)
    else:
        model_f = tf.function(model)

    # Manual evaluation routine to prevent compilation
    correct, total = 0, 0
    for frames, label in tqdm(val_ds, total=val_steps):
        if in_akida:
            model = akida.Model(model.layers)
        else:
            reset_buffers(model)

        # Reset buffers at the start of each segment.
        # By default a segment is now the full sample in the Bufferized mode.
        target_idx = tf.math.argmax(label, -1).numpy()

        predictions = np.zeros((frames.shape[0], n_classes))
        for frame_id in range(frames.shape[1]):
            frame = frames[:, frame_id, ...]
            if in_akida:
                frame = frame.numpy().astype(np.uint8)
                out = model.forward(frame).squeeze()
            else:
                out = model_f(frame)
            # decay the past predictions
            predictions *= decay_factor
            # add the new predicted class
            predictions += softmax(out, axis=-1)
        total += len(target_idx)
        y_pred_idx = np.argmax(predictions, axis=-1)
        correct += np.sum(y_pred_idx == target_idx)
    print(f"Accuracy: {correct / total * 100: .2f}%")


def main():
    global_parser = argparse.ArgumentParser(add_help=False,
                                            description='Jester model training script')
    global_parser.add_argument('-d', '--data', type=str, help='Path to the data')
    global_parser.add_argument("-fs", type=int, default=16, help="Number of frames per segment")
    parsers = get_training_parser(batch_size=32, extract=True, global_parser=global_parser)

    args = parsers[0].parse_args()

    # Load the source model
    model = load_model(args.model)

    if args.data is None or args.data == "":
        raise ValueError("data path should be specified in args.data")

    is_bufferized = get_layers_by_type(model, (BufferTempConv, DepthwiseBufferTempConv))

    # Align the learning rate with the batch size
    # For a batch_size of 32, the optimal lr is 0.008
    lr = args.batch_size * 0.008 / 32

    target_shape = model.input_shape[-3:-1]

    if args.action == "train":
        # generate train dataset.
        train_dataset, train_steps = get_data("train", args.data, args.fs,
                                              target_shape, batch_size=args.batch_size)

        # generate validation dataset.
        val_dataset, val_steps = get_data("val", args.data, args.fs,
                                          target_shape, batch_size=args.batch_size)

        compile_model(model, lr, train_steps, args.epochs, args.fs)
        train(model, train_dataset, val_dataset, train_steps, val_steps, args.epochs)
        save_model(model, args.model, args.savemodel, args.action)

    elif args.action == "eval":
        # generate validation dataset with batch_size only if in akida.
        val_dataset, val_steps = get_data("val", args.data, args.fs, target_shape,
                                          batch_size=1 if args.akida else args.batch_size)
        if args.akida or is_bufferized:
            evaluate_bufferized_model(model, val_dataset, val_steps, in_akida=args.akida)
        else:
            compile_model(model, lr, args.batch_size, val_steps, args.fs)
            history = model.evaluate(val_dataset, steps=val_steps)
            print(history)
    elif args.action == "extract":
        # generate train dataset.
        train_dataset, train_steps = get_data("train", args.data, args.fs,
                                              target_shape, batch_size=args.batch_size)
        extract_samples(train_dataset, args.batch_size, args.savefile, dtype=np.uint8)


if __name__ == "__main__":
    main()
