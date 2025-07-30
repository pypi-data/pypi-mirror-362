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
Training tools for spatiotemporal TENNs.
"""

import tensorflow as tf

from keras.losses import SparseCategoricalCrossentropy, CategoricalCrossentropy
from keras.metrics import Metric


class TemporalSparseCategoricalCrossentropy(SparseCategoricalCrossentropy):
    """ A Wrapper around the SparseCategoricalCrossentropy loss function to transform labels and
    predictions.
    """

    def __call__(self, y_true, y_pred, sample_weight=None):
        """ Need to extend the predicted output for each of the time steps in y_true, flattening
        y_pred.

        y_true: (B,) -> (B * T,)
        y_pred: (B, T, C) -> (B * T, C)
        """
        num_time_steps = y_pred.shape[1]
        y_true = tf.repeat(y_true, num_time_steps)
        y_pred = tf.reshape(y_pred, (-1, y_pred.shape[-1]))
        return super().__call__(y_true, y_pred, sample_weight)


class TemporalCategoricalCrossentropy(CategoricalCrossentropy):
    """ A wrapper arount the CategoricalCrossentropy loss function
    to transform labels and prediction to allow a prediction
    for each time point
    """

    def __init__(self, from_logits=False, label_smoothing=0.0, num_time_steps=None):
        super().__init__(from_logits=from_logits, label_smoothing=label_smoothing)
        self.num_time_steps = num_time_steps

    def __call__(self, y_true, y_pred, sample_weight=None):
        """ Need to extend the predicted output for each of the time steps in y_true, flattening
        y_pred.

        y_true: (B, C) -> (B * T, C)
        y_pred: (B, T, C) -> (B * T, C)
        """
        if self.num_time_steps is None:
            y_true = tf.repeat(y_true, y_pred.shape[1])
        else:
            y_true = tf.repeat(y_true, self.num_time_steps, axis=0)
        y_pred = tf.reshape(y_pred, (-1, y_pred.shape[-1]))
        return super().__call__(y_true, y_pred)


class TemporalAccuracy(Metric):
    """ Class to calculate the accuracy of the outputs of multiple predictions (in time).
    """

    def __init__(self, is_sparse=True, axis=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.correct = self.add_weight(name='correct', initializer='zeros')
        self.total = self.add_weight(name='total', initializer='zeros')
        self.is_sparse = is_sparse
        self.axis = axis

    def update_state(self, y_true, y_pred, sample_weight=None):
        """
        Has to use dynamic shapes (tf.shape)
        https://github.com/keras-team/keras/issues/15932#issuecomment-1023817668

        Args:
            y_true: (B,) -> (B * T,)
            y_pred: (B, T, C) -> (B * T, C)
        """
        num_time_steps = tf.shape(y_pred)[1]
        y_true = tf.repeat(y_true, num_time_steps, axis=self.axis)
        y_pred = tf.reshape(y_pred, (-1, tf.shape(y_pred)[-1]))
        y_pred = tf.argmax(y_pred, axis=-1)
        if not self.is_sparse:
            y_true = tf.argmax(y_true, axis=-1)

        y_true = tf.cast(y_true, tf.int32)
        y_pred = tf.cast(y_pred, tf.int32)

        correct = tf.cast(tf.equal(y_true, y_pred), tf.float32)

        self.correct.assign_add(tf.math.reduce_sum(correct))
        self.total.assign_add(float(tf.shape(correct)[0]))

    def result(self):
        return self.correct / self.total

    def reset_state(self):
        self.correct.assign(0.)
        self.total.assign(0.)
