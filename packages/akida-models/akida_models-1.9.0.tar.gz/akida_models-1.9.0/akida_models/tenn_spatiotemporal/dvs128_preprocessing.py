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
DVS128 gesture_experimental dataset preprocessing and generator.
"""

import cv2
import tonic
import numpy as np

from keras.utils import Sequence


class GestureSequence(Sequence):
    """ Preprocessed DVS128 gesture_experimental data generator.

    Args:
        input_shape (tuple): desired data shape
        data_path (str): path to the DVS128 gesture_experimental dataset
        train (bool): True to get training data, False for validation
        frames_per_segment (int): number of frames per segment
    """

    def __init__(self, input_shape, data_path, train, frames_per_segment):
        # dataset parameters
        # raw event timesteps are in microseconds (= 20 ms bins)
        downsample = 20000
        # First 1500 ms of each sample
        total_length = 1500000

        # segments are what the model is predicting
        self.train = train
        self.input_shape = input_shape

        self.num_frames = total_length // downsample
        self.frames_per_segment = frames_per_segment
        self.segments_per_trial = self.num_frames // self.frames_per_segment

        # frame_transform outputs a tensor of shape (T, C, H, W)
        to_frame = tonic.transforms.ToFrame(sensor_size=tonic.datasets.DVSGesture.sensor_size,
                                            time_window=downsample, include_incomplete=True)
        # crop trials to desired time duration to reduce processing
        to_frame = tonic.transforms.Compose([tonic.transforms.CropTime(max=total_length - 1),
                                             to_frame])

        # load from the tonic dataset
        # This has a data attribute that is a list of filenames for each trial
        # and a target attribute that is a list of the target values for each trial
        dataset = tonic.datasets.DVSGesture(data_path, train=train, transform=to_frame)

        # Dataset preprocessing
        num_trials = len(dataset)
        # (N, T, H, W, C)
        self.events = np.zeros((num_trials, self.num_frames) + input_shape, dtype=np.float32)
        self.labels = np.zeros(num_trials, dtype=np.int64)
        for data_id in range(num_trials):
            event, label = dataset[data_id]
            event = event.transpose(0, 2, 3, 1).astype(np.float32)
            event = self.pad_time(self.batch_resize(event))
            self.events[data_id] = np.clip(event, 0, 1)
            self.labels[data_id] = label

        valid_inds = self.labels != 10
        self.events, self.labels = self.events[valid_inds], self.labels[valid_inds]

        num_trials = len(self.events)
        self.tot_segments = num_trials * self.segments_per_trial
        self.segment_ids = np.arange(self.tot_segments)

    def pad_time(self, imgs):
        if imgs.shape[0] < self.num_frames:
            padding = self.num_frames - imgs.shape[0]
            return np.pad(imgs, ((padding, 0), (0, 0), (0, 0), (0, 0)))
        return imgs

    def batch_resize(self, imgs):
        if self.input_shape[:2] != (128, 128):
            return np.array([cv2.resize(img, self.input_shape[:2]) for img in imgs])
        return imgs

    def __len__(self):
        return self.tot_segments

    def __getitem__(self, idx):
        if idx == 0 and self.train:
            np.random.shuffle(self.segment_ids)

        index = self.segment_ids[idx]
        trial_id = index // self.segments_per_trial
        index = index % self.segments_per_trial

        start_frame = index * self.frames_per_segment
        end_frame = start_frame + self.frames_per_segment

        return self.events[trial_id, start_frame:end_frame], self.labels[trial_id]
