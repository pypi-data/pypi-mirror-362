#!/usr/bin/env python
# *****************************************************************************
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
Tools for Knowledge Distillation training.

Originated from https://keras.io/examples/vision/knowledge_distillation/.

Reference Hinton et al. (2015) https://arxiv.org/abs/1503.02531
"""

from tensorflow import GradientTape
from keras import Model


class Distiller(Model):
    """ The class that will be used to train the student model using the
    distillation knowledge method.

    Reference `Hinton et al. (2015) <https://arxiv.org/abs/1503.02531>`_.

    Args:
        student (keras.Model): the student model
        teacher (keras.Model): the well trained teacher model
        alpha (float, optional): weight to student_loss_fn and 1-alpha
            to distillation_loss_fn. Defaults to 0.1
    """

    def __init__(self, student, teacher, alpha=0.1):
        super().__init__()
        self.teacher = teacher
        self.student = student
        self.student_loss_fn = None
        self.distillation_loss_fn = None
        self.alpha = alpha

    @property
    def base_model(self):
        return self.student

    @property
    def layers(self):
        return self.base_model.layers

    def compile(self,
                optimizer,
                metrics,
                student_loss_fn,
                distillation_loss_fn):
        """ Configure the distiller.

        Args:
            optimizer (keras.optimizers.Optimizer): Keras optimizer
                for the student weights
            metrics (keras.metrics.Metric): Keras metrics for evaluation
            student_loss_fn (keras.losses.Loss): loss function of difference
                between student predictions and ground-truth
            distillation_loss_fn (keras.losses.Loss): loss function of
                difference between student predictions and teacher predictions
        """

        super().compile(optimizer=optimizer, metrics=metrics)
        self.student_loss_fn = student_loss_fn
        self.distillation_loss_fn = distillation_loss_fn

    def train_step(self, data):
        # Unpack data
        x, y = data

        # Forward pass of teacher
        teacher_predictions = self.teacher(x, training=False)
        with GradientTape() as tape:
            # Forward pass of student
            student_predictions = self.student(x, training=True)
            # Compute losses
            student_loss = self.student_loss_fn(y, student_predictions)
            distillation_loss = self.distillation_loss_fn(
                teacher_predictions, student_predictions)
            loss = self.alpha * student_loss + (1 -
                                                self.alpha) * distillation_loss

        # Compute gradients
        trainable_vars = self.student.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        # Update the metrics configured in `compile()`.
        self.compiled_metrics.update_state(y, student_predictions)

        # Return a dict of performance
        results = {m.name: m.result() for m in self.metrics}
        results.update({
            "student_loss": student_loss,
            "distillation_loss": distillation_loss
        })
        return results

    def test_step(self, data):
        # Unpack the data
        x, y = data

        # Compute predictions
        y_prediction = self.student(x, training=False)

        # Calculate the loss
        student_loss = self.student_loss_fn(y, y_prediction)

        # Update the metrics.
        self.compiled_metrics.update_state(y, y_prediction)

        # Return a dict of performance
        results = {m.name: m.result() for m in self.metrics}
        results.update({"student_loss": student_loss})
        return results

    def save(self, *args, **kwargs):
        return self.base_model.save(*args, **kwargs)

    def save_weights(self, *args, **kwargs):
        return self.base_model.save_weights(*args, **kwargs)

    def load_weights(self, *args, **kwargs):
        return self.base_model.load_weights(*args, **kwargs)
