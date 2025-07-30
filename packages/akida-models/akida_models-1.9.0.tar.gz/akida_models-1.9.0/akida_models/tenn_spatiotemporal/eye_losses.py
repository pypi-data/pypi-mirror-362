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
""" EyeTracking dataset losses and metrics."""

import tensorflow as tf


def tracking_loss(pred, center, openness, batch_size=8, frames=50, height=3, width=4, gamma=2):
    # Extract ground truth
    x, y = tf.unstack(center, axis=1)
    x_ind = tf.cast(tf.clip_by_value(x * width, 0, width - 1), dtype=tf.int32)
    x_ind = tf.reshape(x_ind, [-1])
    y_ind = tf.cast(tf.clip_by_value(y * height, 0, height - 1), dtype=tf.int32)
    y_ind = tf.reshape(y_ind, [-1])

    bs_range = tf.range(batch_size)
    batch_range = tf.tile(tf.expand_dims(bs_range, axis=1), multiples=[1, frames])
    batch_range = tf.reshape(batch_range, [-1])
    frames_range = tf.tile(tf.range(frames), multiples=[batch_size])
    indices = tf.stack([batch_range, frames_range, y_ind, x_ind], axis=1)
    update_size = tf.cast(tf.math.multiply(tf.cast(batch_size, tf.float32),
                                           tf.cast(frames, tf.float32)), tf.int32)

    pred = tf.clip_by_value(tf.sigmoid(pred), 1e-4, 1 - 1e-4)
    pred_pupil, pred_x, pred_y = tf.unstack(pred, axis=4)

    smooth_l1_loss = tf.keras.losses.Huber(delta=0.11, reduction='none')
    pred_center_mod = tf.stack([pred_x, pred_y], axis=4)
    x_mod = (x * width) % 1
    y_mod = (y * height) % 1
    center_mod = tf.stack([x_mod, y_mod], axis=2)
    center_loss = smooth_l1_loss(pred_center_mod, center_mod[:, :, tf.newaxis, tf.newaxis, :])

    pupil_mask = tf.zeros_like(pred_pupil, dtype=tf.bool)
    updates = tf.ones([update_size], dtype=tf.bool)
    pupil_mask = tf.tensor_scatter_nd_update(pupil_mask, indices, updates)
    focal_loss = tf.where(
        pupil_mask, -1 * tf.pow(1 - pred_pupil, gamma) * tf.math.log(pred_pupil) + center_loss,
        -1 * tf.pow(pred_pupil, gamma) * tf.math.log(1 - pred_pupil))

    # create a valid mask to only propagate the loss when the eye is open
    valid_mask = tf.equal(
        openness, 1) & tf.math.greater(
        x, 0) & tf.math.less(
        x, 1) & tf.math.greater(
        y, 0) & tf.math.less(
        y, 1)
    valid_mask = tf.expand_dims(tf.expand_dims(valid_mask, axis=-1), axis=-1)
    broadcasted_mask = tf.broadcast_to(valid_mask, tf.shape(focal_loss))
    # only compute loss on the valid frame
    masked_focal_loss = tf.boolean_mask(focal_loss, broadcasted_mask)
    masked_focal_loss_reduced = tf.reduce_sum(masked_focal_loss)
    n_valid_mask = tf.reduce_sum(tf.cast(valid_mask, dtype=tf.float32))
    out_loss = tf.divide(masked_focal_loss_reduced, n_valid_mask)
    return out_loss


class EyeLosses(tf.keras.losses.Loss):
    """Custom Keras loss for calculating tracking loss on eye data.

    This class defines a custom loss function for eye tracking tasks, utilizing a specified
    prediction loss function and considering batch size, frames, height, and width of the
    input data.

    Args:
        batch_size (int, optional): The number of samples per batch. Default is 32.
        frames (int, optional): The number of frames per sample. Default is 50.
        height (int, optional): The height dimension of the input data. Default is 3.
        width (int, optional): The width dimension of the input data. Default is 4.
    """

    def __init__(self, batch_size=32, frames=50, height=3, width=4):
        super(EyeLosses, self).__init__()
        self.prediction_loss = tracking_loss
        self.batch_size = batch_size
        self.frames = frames
        self.height = height
        self.width = width

    def __call__(self, y_true, y_pred, sample_weight=None):
        # 3 is num channels
        y_true.set_shape((self.batch_size, 3, self.frames))
        x, y, openness = tf.unstack(y_true, axis=1)
        center = tf.stack([x, y], axis=1)
        loss = self.prediction_loss(y_pred, center, openness,
                                    self.batch_size, self.frames, self.height, self.width)
        if sample_weight is not None:
            loss = loss * sample_weight
        return tf.reduce_mean(loss)


def process_detector_prediction(pred):
    batch_size, frames, height, width, _ = tf.unstack(tf.shape(pred))

    pred_pupil, pred_x_mod, pred_y_mod = tf.unstack(pred, axis=4)
    pred_x_mod = tf.sigmoid(pred_x_mod)
    pred_y_mod = tf.sigmoid(pred_y_mod)

    pupil_ind = tf.argmax(tf.reshape(pred_pupil, shape=[batch_size, frames, -1]), axis=-1)
    pupil_ind_x = tf.math.floormod(tf.cast(pupil_ind, dtype=tf.int32), width)
    pupil_ind_y = tf.math.floordiv(tf.cast(pupil_ind, dtype=tf.int32), width)

    batch_range = tf.repeat(tf.range(batch_size), repeats=frames)
    frames_range = tf.tile(tf.range(frames), multiples=[batch_size])
    indices = tf.stack([batch_range, frames_range, tf.reshape(
        pupil_ind_y, [-1]), tf.reshape(pupil_ind_x, [-1])], axis=1)
    pred_x_mod = tf.gather_nd(pred_x_mod, indices)
    pred_y_mod = tf.gather_nd(pred_y_mod, indices)

    x = tf.divide(tf.cast(pupil_ind_x, dtype=tf.float32) +
                  tf.reshape(pred_x_mod, (batch_size, frames)),
                  tf.cast(width, dtype=tf.float32))
    y = tf.divide(tf.cast(pupil_ind_y, dtype=tf.float32) +
                  tf.reshape(pred_y_mod, (batch_size, frames)),
                  tf.cast(height, dtype=tf.float32))

    return tf.stack([x, y], axis=1)


def p10_acc(y_pred, center, openness, detector_head=True, height=60, width=80, tolerance=10):
    """Calculate P10 accuracy metrics based on predicted and ground truth coordinates.

    Args:
        y_pred (tf.Tensor): Predicted coordinates of shape (batch_size, 2) if detector_head
            is True, or (batch_size, 1) otherwise.
        center (tf.Tensor): Ground truth coordinates of shape (batch_size, 2).
        openness (tf.Tensor): Indicator of openness (blink or not) of shape (batch_size,).
        detector_head (bool, optional): Flag indicating if y_pred needs post-processing with
            a detector function. Defaults to True.
        height (int, optional): Height of the image or frame. Defaults to 60.
        width (int, optional): Width of the image or frame. Defaults to 80.
        tolerance (int, optional): Tolerance distance threshold for accuracy calculation.
            Defaults to 10.

    Returns:
        (tf.Tensor, tf.Tensor, tf.Tensor): Fraction of predictions within tolerance distance,
            including blinks; Fraction of predictions within tolerance distance,
            excluding blinks; Mean distance between predicted and ground truth coordinates.
    """
    if detector_head:
        y_pred = process_detector_prediction(y_pred)
    else:
        y_pred = tf.sigmoid(y_pred)
    y_pred_x = y_pred[:, 0] * width
    y_pred_y = y_pred[:, 1] * height
    center_x = center[:, 0] * width
    center_y = center[:, 1] * height
    distances = tf.sqrt(tf.square(center_x - y_pred_x) + tf.square(center_y - y_pred_y))
    distances_noblinks = tf.boolean_mask(distances, tf.equal(openness, 1))
    # This model as defined generates predictions at 100 Hz (10 ms frames).
    # The original challenge required predictions at 20 Hz thus we take every 5th pred
    distances = distances[..., ::5]
    within_tolerance = tf.divide(tf.reduce_sum(tf.cast(tf.less(distances, tolerance), tf.float32)),
                                 tf.cast(tf.reduce_prod(tf.shape(distances)), dtype=tf.float32))
    within_tolerance_noblinks = tf.divide(
        tf.reduce_sum(tf.cast(tf.less(distances_noblinks, tolerance), tf.float32)),
        tf.cast(tf.reduce_prod(tf.shape(distances_noblinks)), dtype=tf.float32))
    mean_distance = tf.reduce_mean(distances)
    return within_tolerance, within_tolerance_noblinks, mean_distance


class P10Accuracy(tf.keras.metrics.Metric):
    """Custom Keras metric for calculating P10 accuracy metrics.

    This metric computes P10 accuracy metrics based on predicted and ground truth coordinates,
    considering blink detection.

    Args:
        metric (str, optional): Specifies which metric to track, either 'within_tolerance' or
            'mean_distance'. Defaults is 'within_tolerance'.
        name (str, optional): Name of the metric instance. Defaults to None.
    """

    def __init__(self, metric='within_tolerance', name=None, **kwargs):
        super(P10Accuracy, self).__init__(name=name, **kwargs)
        self.metric = metric
        self.within_tolerance = self.add_weight(name='within_tolerance', initializer='zeros')
        self.within_tolerance_noblinks = self.add_weight(name='within_tolerance_noblinks',
                                                         initializer='zeros')
        self.mean_distance = self.add_weight(name='mean_distance', initializer='zeros')
        self.counter = self.add_weight(name='counter', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        x, y, openness = tf.unstack(y_true, axis=1)
        center = tf.stack([x, y], axis=1)
        within_tolerance, within_tolerance_noblinks, mean_distance = p10_acc(
            y_pred, center, openness)
        self.counter.assign_add(1)
        self.within_tolerance.assign_add(within_tolerance)
        self.within_tolerance_noblinks.assign_add(within_tolerance_noblinks)
        self.mean_distance.assign_add(mean_distance)

    def result(self):
        if self.counter <= 0:
            return 0.0
        if self.metric == 'within_tolerance':
            return self.within_tolerance / self.counter
        elif self.metric == 'within_tolerance_noblinks':
            return self.within_tolerance_noblinks / self.counter
        elif self.metric == 'mean_distance':
            return self.mean_distance / self.counter
        else:
            raise ValueError(f"Invalid metric: {self.metric}")

    def reset_state(self):
        self.within_tolerance.assign(0)
        self.within_tolerance_noblinks.assign(0)
        self.mean_distance.assign(0)
        self.counter.assign(0)
