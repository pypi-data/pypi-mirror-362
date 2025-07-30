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
EyeTracking dataset preprocessing and generator.
"""

import math
import h5py
import ast
import tensorflow as tf
import numpy as np

from pathlib import Path

# Predifined folder ids that will be used exclusively for the evaluation/validation
VAL_FILES = ["1_6", "2_4", "4_4", "6_2", "7_4", "9_1", "10_3", "11_2", "12_3"]


def get_index(file_lens, index):
    file_lens_cumsum = np.cumsum(np.array(file_lens))
    file_id = np.searchsorted(file_lens_cumsum, index, side='right')
    sample_id = index - file_lens_cumsum[file_id - 1] if file_id > 0 else index
    return file_id, sample_id


def txt_to_npy(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(ast.literal_eval(line.strip()))
    return np.array(data)


def h5_to_npy(file_path, name):
    with h5py.File(file_path, 'r') as file:
        npy_data = file[name][:]
    return npy_data


def linear_interp(x, xp, fp):
    x = tf.cast(x, tf.float32)
    xp = tf.cast(xp, tf.float32)
    fp = tf.cast(fp, tf.float32)
    x = tf.clip_by_value(x, tf.cast(tf.reduce_min(xp), tf.float32),
                         tf.cast(tf.reduce_max(xp), tf.float32))
    idx = tf.searchsorted(xp, x, side='left')
    idx = tf.clip_by_value(idx, 1, len(xp) - 1)

    x0 = tf.gather(xp, idx - 1)
    x1 = tf.gather(xp, idx)
    y0 = tf.gather(fp, idx - 1)
    y1 = tf.gather(fp, idx)

    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def events_to_frames(events, size, num_frames, spatial_downsample, temporal_downsample):
    """Transforms events (a segment of a trial) into frames by applying causal linear interpolation
        of input spikes,as well as spatial and temporal downsampling.

    Args:
        events (tf.Tensor): The input event data segment.
        size (tuple): A tuple containing two integers representing the height and width of
            the output frames.
        num_frames (int): The number of frames to segment the input data into.
        spatial_downsample (tuple): A tuple containing two integers representing the downsampling
            factors for the height and width dimensions.
        temporal_downsample (int): The downsampling factor for the time dimension.

    Returns:
        tf.Tensor: The processed event data, converted into frames.
    """
    height, width = size

    p, x, y, t = tf.unstack(events, axis=0)
    frames = tf.zeros([num_frames, 2, height, width], dtype=tf.float32)

    def bilinear_interp(x, scale, x_max):
        if scale == 1:
            return x, x, tf.ones_like(x), tf.zeros_like(x)
        # Perform operations on floats, keeping x as float for interpolation
        xd1 = tf.divide(tf.math.mod(x, tf.cast(scale, x.dtype)), tf.cast(scale, x.dtype))
        xd = 1.0 - xd1
        x_int = tf.clip_by_value(tf.math.floordiv(tf.cast(x, tf.int32), scale), 0, x_max)
        x1_int = tf.clip_by_value(x_int + 1, 0, x_max)

        return x_int, x1_int, xd, xd1

    x_int, x1_int, xd, xd1 = bilinear_interp(x, spatial_downsample[0], width - 1)
    y_int, y1_int, yd, yd1 = bilinear_interp(y, spatial_downsample[1], height - 1)
    t_int, t1_int, td, td1 = bilinear_interp(t, temporal_downsample, num_frames - 1)

    # Similar to bilinear, but temporally causal
    p = tf.tile(p, multiples=tf.constant([4]))
    x_int = tf.tile(x_int, multiples=tf.constant([2]))
    x1_int = tf.tile(x1_int, multiples=tf.constant([2]))
    x = tf.concat([x_int, x1_int], axis=0)
    y = tf.tile(tf.concat([y_int, y1_int], axis=0), [2])
    t = tf.tile(t_int, multiples=tf.constant([4]))

    # Repeat and concatenate arrays to create the desired patterns
    # and keep the tensor shapes coherent
    xd_repeated = tf.tile(xd, multiples=[2])
    xd1_repeated = tf.tile(xd1, multiples=[2])
    xd = tf.concat([xd_repeated, xd1_repeated], axis=0)
    yd = tf.tile(tf.concat([yd, yd1], axis=0), multiples=[2])
    td = tf.tile(td1, multiples=[4])
    indices = tf.stack([t, tf.cast(p, tf.int32), y, x], axis=1)
    frames = tf.tensor_scatter_nd_add(
        frames, indices, xd * yd * td)

    return frames


class EventRandomAffine():
    """Perform random affine transformations on the events and labels

    Args:
        size (tuple, optional): A tuple containing two integers representing the height and width
            of the input events and labels. Defaults to (480, 640).
        degrees (float, optional): The range of degrees for random rotation. A single float
            representing the maximum absolute angle. Defaults to 15.
        translate (tuple, optional): A tuple containing two floats representing the maximum
            fraction of translation for the height and width dimensions. Defaults to (0.2, 0.2).
        scale (tuple, optional): A tuple containing two floats representing the minimum and
            maximum scaling factors. Defaults to (0.8, 1.2).
        augment_flag (bool, optional): A boolean flag to enable or disable the augmentation.
            Defaults to True.
    """

    def __init__(self, size=(480, 640),
                 degrees=15, translate=(0.2, 0.2), scale=(0.8, 1.2),
                 augment_flag=True):
        self.degrees = degrees
        self.translate = translate
        self.scale = scale
        self.augment_flag = augment_flag

        self.height, self.width = size

    def normalize(self, coords, backward=False):
        """Normalizes coordinates between -0.5 and 0.5 or projects them back into the
            spatial dimension of the output.

        Args:
            coords (tf.Tensor): The input coordinates to be normalized or denormalized.
            backward (bool, optional): A boolean flag indicating whether to perform normalization
                (False) or denormalization (True). Defaults to False.

        Returns:
            tf.Tensor: The processed coordinates, normalized to the range [-0.5, 0.5] if
            `backward` is False, or projected back into the spatial dimension if `backward`
            is True.
        """
        if not backward:
            updated_coords = tf.stack([
                tf.divide(coords[0], self.width) - 0.5,
                tf.divide(coords[1], self.height) - 0.5,
                coords[2]
            ])
        else:
            updated_coords = tf.stack([
                (coords[0] + 0.5) * self.width,
                (coords[1] + 0.5) * self.height,
                coords[2]
            ])
        return updated_coords

    def __call__(self, events, labels):
        if self.augment_flag:
            # Convert from degrees to radians, to be used with tf.cos and tf.sin
            degrees = tf.divide(tf.random.uniform((), -self.degrees, self.degrees), 180) * math.pi
            translate = [tf.random.uniform((), -t, t) for t in self.translate]
            scale = [tf.random.uniform((), self.scale[0], self.scale[1]) for _ in range(2)]

            cos, sin = tf.cos(degrees), tf.sin(degrees)

            R = tf.convert_to_tensor([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
            S = tf.convert_to_tensor([[scale[0], 0, 0], [0, scale[1], 0], [0, 0, 1]])
            T = tf.convert_to_tensor([[1, 0, translate[0]], [0, 1, translate[1]], [0, 0, 1]])

            trans_matrix = T @ R @ S
        else:
            trans_matrix = tf.eye(3, dtype=tf.float32)

        event1, event2, event3, event4 = tf.unstack(events, axis=0)
        padding_array = tf.ones_like(event1, dtype=event1.dtype)
        coords = tf.stack([event2, event3, padding_array], axis=0)
        # For efficiency reasons, the affine transforms are done as matrix multiplication
        # on the normalized (between 0 and 1) coordinates and then reprojected back into
        # the output shape.
        coords = self.normalize(tf.matmul(trans_matrix, self.normalize(coords)), backward=True)

        # Remove out of frame events after the affine transform
        coord1, coord2, _ = tf.unstack(coords, axis=0)
        events = tf.stack([event1, coord1, coord2, event4], axis=0)
        val_inds = tf.logical_and(
            tf.logical_and(coord1 >= 0, coord1 < self.width),
            tf.logical_and(coord2 >= 0, coord2 < self.height)
        )

        events = tf.boolean_mask(events, val_inds, axis=1)
        labels = tf.transpose(labels)
        label1, label2, closes = tf.unstack(labels, axis=0)
        padding_array = tf.ones_like(label1, dtype=label1.dtype)
        centers = tf.stack([label1, label2, padding_array], axis=0)
        centers = tf.matmul(trans_matrix, self.normalize(centers))
        center1, center2, _ = tf.unstack(centers, axis=0)
        # Note: We add 0.5 because the applied normalization just above actually
        # has a -0.5 in the normalization (i.e. the center coords were projected
        # between -0.5 and 0.5 before the transformation was applied to them)
        centers = tf.stack([center1, center2], axis=0) + tf.constant(0.5)

        return events, centers, closes


def preprocess_data(events, label, train_mode, frames_per_segment, spatial_downsample, time_window):
    """
    Last events' processing before being fed by the model.

    This function performs several transformations on the input events including
    augmentation (if training data), conversion to frames, and optional time and polarity flipping
    also if training data.

    Args:
        events (tf.Tensor): The input events.
        label (tf.Tensor): The corresponding labels.
        train_mode (bool): A flag indicating whether the function is being called in training mode.
        frames_per_segment (int): The number of frames to segment the event data into.
        spatial_downsample (tuple of int): A tuple containing two integers representing the
            downsampling factors for the height and width dimensions.
        time_window (float): The time window in microseconds for aggregating events into frames.

    Returns:
        tf.Tensor, tf.Tensor: The processed events, converted into frames and optionally
        augmented; The processed label data, concatenated with the center and the inverse
        of the close flag.
    """

    augment = EventRandomAffine(augment_flag=train_mode)
    events, center, close = augment(events, label)
    num_frames = frames_per_segment

    frames = events_to_frames(events,
                              (augment.height // spatial_downsample[1],
                               augment.width // spatial_downsample[0]),
                              num_frames,
                              spatial_downsample,
                              time_window)
    final_frames = tf.transpose(frames, perm=(0, 2, 3, 1))
    final_label = tf.concat([center, tf.expand_dims(1 - close, axis=0)],
                            axis=0)
    # Compute mean and std of the sample per channel and per frame
    mean = tf.reduce_mean(final_frames, [1, 2], keepdims=True)
    std = tf.math.reduce_std(final_frames, [1, 2], keepdims=True)
    # Normalize the inputs
    epsilon = 1e-6
    final_frames = 2 * ((final_frames - mean) / (std + epsilon)) - 1
    # Convert to int8 samples compatible with Akida
    final_frames = tf.round(final_frames * 127)
    final_frames = tf.cast(tf.clip_by_value(final_frames, -127, 127), tf.int8)
    return final_frames, final_label


def split_trial(trial, label, train_mode, frames_per_segment, time_window):
    """
    Splits a trial into segments of events and applies optional temporal augmentation for training.

    This function divides the input `event` data into segments based on the specified
    `frames_per_segment` and `time_window`. It also applies random temporal shifts and scaling
    to the event data if `train_mode` is True.

    Args:
        trial (tf.Tensor): The raw input of events data.
        label (tf.Tensor): The corresponding labels for the input event data.
        train_mode (bool): A flag indicating whether the function is being called in training mode.
        frames_per_segment (int): The number of frames to segment the event data into.
        time_window (float): The time window in microseconds for each segment of event data.

    Returns:
        list, list: A list of tensors, where each tensor represents a segment of the input event
            data. A list of tensors, where each tensor represents the corresponding labels for
            each event segment.
    """
    events_segments, label_segments = [], []
    time_window_per_segment = time_window * frames_per_segment
    max_offset = round(time_window_per_segment * 0.1)
    num_frames = label.shape[0]
    max_scale = tf.cast(num_frames * time_window * 0.8, tf.int32)
    num_segments = num_frames // frames_per_segment
    for segment_id in range(num_segments):
        start_t = tf.convert_to_tensor([segment_id * time_window_per_segment])
        end_t = tf.convert_to_tensor([start_t + time_window_per_segment])

        # random temporal shift
        if train_mode and start_t >= max_offset:
            offset = tf.random.uniform(shape=[], minval=0, maxval=max_offset, dtype=tf.int32)
            start_t -= offset
            end_t -= offset
        else:
            offset = 0
        # Copy the event to apply random scaling on it
        event_scaled = tf.identity(trial)
        # random temporal scaling
        if train_mode and end_t < max_scale:
            scale_factor = tf.random.uniform(shape=[], minval=0.8, maxval=1.2)
        else:
            scale_factor = tf.constant(1.0)
        # Compute scaling_vector to apply scaling only on time dimension
        ones_tensor = tf.ones((3, 1), dtype=tf.float32)
        scaling_vector = tf.concat([ones_tensor, tf.reshape(scale_factor, (1, 1))], axis=0)
        event_scaled = event_scaled * scaling_vector
        start_ind = tf.searchsorted(event_scaled[-1], tf.cast(start_t, tf.float32), side='left')
        end_ind = tf.searchsorted(event_scaled[-1], tf.cast(end_t, tf.float32), side='left')
        event_segment = event_scaled[:, tf.squeeze(start_ind):tf.squeeze(end_ind)]
        p, x, y, t = tf.unstack(event_segment, axis=0)
        t = tf.subtract(t, tf.cast(start_t, dtype=tf.float32))
        event_segment = tf.stack([p, x, y, t], axis=0)

        # label interpolation
        arange = tf.range(0, num_frames)
        label_offset = tf.cast(offset / time_window, tf.float32)
        start_label_id = segment_id * frames_per_segment
        end_label_id = (segment_id + 1) * frames_per_segment
        interp_range = tf.linspace(
            (tf.cast(start_label_id, tf.float32) - label_offset) / scale_factor,
            (tf.cast(end_label_id, tf.float32) - label_offset - 1) / scale_factor,
            frames_per_segment,
        )
        x_interp = linear_interp(interp_range, arange, label[:, 0])
        y_interp = linear_interp(interp_range, arange, label[:, 1])
        closeness = label[start_label_id:end_label_id, -1]
        label_segment = tf.stack([x_interp, y_interp, closeness], axis=1)

        events_segments.append(event_segment)
        label_segments.append(label_segment)

    return events_segments, label_segments


def process_files(data_path, label_path, time_window):
    """
    Processes data and label files, converting them to the appropriate format
        and aligning them based on time windows.

    Args:
        data_path (str): Path to the data file in .h5 format containing event data.
        label_path (str): Path to the label file in .txt format.
        time_window (float): Time window in microseconds for each frame in the data.

    Returns:
        - trial (tf.Tensor): Tensor of shape (4, N), where N is the number of frames.
            This tensor contains event data, where the four components represent polarity ("p"),
            spatial positions ("x", "y"), and timestamp ("t") corresponding
            to each spike or event within the trial.
        - labels (tf.Tensor): Tensor representing the labels aligned with the frames.
    """
    trial, labels = h5_to_npy(data_path, 'events'), txt_to_npy(label_path)

    # truncating off trailing events with no labels
    num_frames = labels.shape[0]
    final_t = num_frames * time_window
    final_ind = np.searchsorted(trial['t'], final_t, 'left')
    trial = trial[:final_ind]

    labels = tf.convert_to_tensor(labels, dtype=tf.float32)
    trial = tf.stack([trial[k].astype('float32') for k in ['p', 'x', 'y', 't']], axis=0)

    return trial, labels


def generate_dir_paths(root_path, mode):
    """
    Generates a list of directory paths based on the training mode and specified files.

    Args:
        root_path (str or Path): The root directory path where training data is stored.
        mode (str): Possible values : ['train', 'val', 'test']. A flag indicating the mode in which
            the function is being called.

    Returns:
        list: A list of directory paths filtered based on the training mode and file names.
    """
    postfix = 'train' if mode in ['train', 'val'] else 'test'
    base_path = Path(root_path) / postfix
    dir_paths = base_path.glob('*')
    if mode == 'train':
        return [dir_path for dir_path in dir_paths if dir_path.name not in VAL_FILES]
    elif mode == 'val':
        return [dir_path for dir_path in dir_paths if dir_path.name in VAL_FILES]
    elif mode == 'test':
        return dir_paths
    else:
        raise ValueError(f"Invalid mode: {mode}. Expected one of ['train', 'val', 'test'].")


def load_data(root_path, mode, frames_per_segment, time_window):
    """ Loads Eye Tracking data.

    Args:
        root_path (str): path to data
        mode (str): Possible values : ['train', 'val', 'test', 'buffer']. A flag indicating the mode
            in which the function is being called.
        frames_per_segment (int): The number of frames per segment of a trial.
        time_window (float): The time window in microseconds for aggregating events into frames.

    Returns:
        list, list : list of segments of all the raw trials, list of their respective labels.
    """
    if mode in ['train', 'val', 'test']:
        dir_paths = generate_dir_paths(root_path, mode)
    elif mode == 'buffer':
        dir_paths = [root_path]
    else:
        raise ValueError(f"Invalid mode: {mode}. "
                         "Expected one of ['train', 'val', 'test', 'buffer'].")

    all_events_processed, all_labels_processed = [], []
    for dir_path in dir_paths:
        assert dir_path.is_dir()
        data_path = dir_path / f'{dir_path.name}.h5'
        label_path = dir_path / 'label.txt'

        trial, label = process_files(data_path, label_path, time_window)

        if mode != 'train':
            events_processed, labels_processed = split_trial(trial, label, False,
                                                             frames_per_segment, time_window)
            all_events_processed.extend(events_processed)
            all_labels_processed.extend(labels_processed)
        else:
            all_events_processed.append(trial)
            all_labels_processed.append(label)

    return all_events_processed, all_labels_processed
