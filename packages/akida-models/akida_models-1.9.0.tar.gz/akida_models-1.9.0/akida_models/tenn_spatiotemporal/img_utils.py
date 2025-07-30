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
Image util ops.
Originated from:
https://github.com/tensorflow/addons/blob/r0.23/tensorflow_addons/image/transform_ops.py
"""

import tensorflow as tf
import numpy as np
from math import pi

from ..extract import extract_samples as akm_extract_samples


_IMAGE_DTYPES = {
    tf.dtypes.uint8,
    tf.dtypes.int32,
    tf.dtypes.int64,
    tf.dtypes.float16,
    tf.dtypes.float32,
    tf.dtypes.float64,
}


def transform(
    images,
    transforms,
    interpolation="nearest",
    fill_mode="constant",
    output_shape=None,
    name=None,
    fill_value=0.0,
):
    """Applies the given transform(s) to the image(s).

    Args:
        images (tf.Tensor): A tensor of shape (num_images, num_rows, num_columns,
            num_channels) (NHWC), (num_rows, num_columns, num_channels) (HWC), or
            (num_rows, num_columns) (HW).
        transforms (tf.Tensor): Projective transform matrix/matrices. A vector of length 8 or
            tensor of size N x 8. If one row of transforms is
            [a0, a1, a2, b0, b1, b2, c0, c1], then it maps the *output* point
            `(x, y)` to a transformed *input* point
            `(x', y') = ((a0 x + a1 y + a2) / k, (b0 x + b1 y + b2) / k)`,
            where `k = c0 x + c1 y + 1`. The transforms are *inverted* compared to
            the transform mapping input points to output points. Note that
            gradients are not backpropagated into transformation parameters.
        interpolation (str, optional): Interpolation mode. Defaults to nearest.
            Supported values: "nearest", "bilinear".
        fill_mode (str, optional): Points outside the boundaries of the input are filled according
            to the given mode (one of `{'constant', 'reflect', 'wrap', 'nearest'}`).
            Defaults to constant.
            - *reflect*: `(d c b a | a b c d | d c b a)`
            The input is extended by reflecting about the edge of the last pixel.
            - *constant*: `(k k k k | a b c d | k k k k)`
            The input is extended by filling all values beyond the edge with the
            same constant value k = 0.
            - *wrap*: `(a b c d | a b c d | a b c d)`
            The input is extended by wrapping around to the opposite edge.
            - *nearest*: `(a a a a | a b c d | d d d d)`
            The input is extended by the nearest pixel.
        fill_value (tf.Tensor, optional): a float represents the value to be filled outside the
            boundaries when `fill_mode` is "constant".
        output_shape (list, optional): Output dimesion after the transform, [height, width].
            If None, output is the same size as input image.

        name (str, optional): The name of the op. Defaults to None.

    Returns:
        tf.Tensor: Image(s) with the same type and shape as `images`, with the given
        transform(s) applied. Transformed coordinates outside of the input image
        will be filled with zeros.
    """
    with tf.name_scope(name or "transform"):
        image_or_images = tf.convert_to_tensor(images, name="images")
        transform_or_transforms = tf.convert_to_tensor(
            transforms, name="transforms", dtype=tf.dtypes.float32
        )
        if image_or_images.dtype.base_dtype not in _IMAGE_DTYPES:
            raise TypeError("Invalid dtype %s." % image_or_images.dtype)
        images = to_4D_image(image_or_images)
        original_ndims = get_ndims(image_or_images)

        if output_shape is None:
            output_shape = tf.shape(images)[1:3]

        output_shape = tf.convert_to_tensor(
            output_shape, tf.dtypes.int32, name="output_shape"
        )

        if not output_shape.get_shape().is_compatible_with([2]):
            raise ValueError(
                "output_shape must be a 1-D Tensor of 2 elements: "
                "new_height, new_width"
            )

        if len(transform_or_transforms.get_shape()) == 1:
            transforms = transform_or_transforms[None]
        elif transform_or_transforms.get_shape().ndims is None:
            raise ValueError("transforms rank must be statically known")
        elif len(transform_or_transforms.get_shape()) == 2:
            transforms = transform_or_transforms
        else:
            transforms = transform_or_transforms
            raise ValueError(
                "transforms should have rank 1 or 2, but got rank %d"
                % len(transforms.get_shape())
            )

        fill_value = tf.convert_to_tensor(
            fill_value, dtype=tf.float32, name="fill_value"
        )
        output = tf.raw_ops.ImageProjectiveTransformV3(
            images=images,
            transforms=transforms,
            output_shape=output_shape,
            interpolation=interpolation.upper(),
            fill_mode=fill_mode.upper(),
            fill_value=fill_value,
        )
        return from_4D_image(output, original_ndims)


def matrices_to_flat_transforms(
    transform_matrices, name=None
):
    """Converts affine matrices to projective transforms.

    Note that we expect matrices that map output coordinates to input
    coordinates. To convert forward transformation matrices,
    call `tf.linalg.inv` on the matrices and use the result here.

    Args:
        transform_matrices (tf.Tensor): One or more affine transformation matrices, for the
            reverse transformation in homogeneous coordinates. Shape `(3, 3)` or
            `(N, 3, 3)`.
        name (str, optional): The name for the op. Defaults to None.

    Returns:
        tf.Tensor: 2D tensor of flat transforms with shape `(N, 8)`, which may be passed
            into `transform` op.
    """
    with tf.name_scope(name or "matrices_to_flat_transforms"):
        transform_matrices = tf.convert_to_tensor(
            transform_matrices, name="transform_matrices"
        )
        if transform_matrices.shape.ndims not in (2, 3):
            raise ValueError(
                "Matrices should be 2D or 3D, got: %s" % transform_matrices
            )
        # Flatten each matrix.
        transforms = tf.reshape(transform_matrices, tf.constant([-1, 9]))
        # Divide each matrix by the last entry (normally 1).
        transforms /= transforms[:, 8:9]
        return transforms[:, :8]


def get_ndims(image):
    return image.get_shape().ndims or tf.rank(image)


def to_4D_image(image):
    """Convert 2/3/4D image to 4D image.

    Args:
        image (tf.Tensor): 2/3/4D `Tensor`.

    Returns:
        tf.Tensor: 4D `Tensor` with the same type.
    """
    with tf.control_dependencies(
        [
            tf.debugging.assert_rank_in(
                image, [2, 3, 4], message="`image` must be 2/3/4D tensor"
            )
        ]
    ):
        ndims = image.get_shape().ndims
        if ndims is None:
            return _dynamic_to_4D_image(image)
        elif ndims == 2:
            return image[None, :, :, None]
        elif ndims == 3:
            return image[None, :, :, :]
        else:
            return image


def _dynamic_to_4D_image(image):
    shape = tf.shape(image)
    original_rank = tf.rank(image)
    # 4D image => [N, H, W, C] or [N, C, H, W]
    # 3D image => [1, H, W, C] or [1, C, H, W]
    # 2D image => [1, H, W, 1]
    left_pad = tf.cast(tf.less_equal(original_rank, 3), dtype=tf.int32)
    right_pad = tf.cast(tf.equal(original_rank, 2), dtype=tf.int32)
    new_shape = tf.concat(
        [
            tf.ones(shape=left_pad, dtype=tf.int32),
            shape,
            tf.ones(shape=right_pad, dtype=tf.int32),
        ],
        axis=0,
    )
    return tf.reshape(image, new_shape)


def from_4D_image(image, ndims):
    """Convert back to an image with `ndims` rank.

    Args:
        image (tf.Tensor): 4D `Tensor`.
        ndims (int): The original rank of the image.

    Returns:
        tf.Tensor: `ndims`-D `Tensor` with the same type.
    """
    with tf.control_dependencies(
        [tf.debugging.assert_rank(image, 4, message="`image` must be 4D tensor")]
    ):
        if isinstance(ndims, tf.Tensor):
            return _dynamic_from_4D_image(image, ndims)
        elif ndims == 2:
            return tf.squeeze(image, [0, 3])
        elif ndims == 3:
            return tf.squeeze(image, [0])
        else:
            return image


def _dynamic_from_4D_image(image, original_rank):
    shape = tf.shape(image)
    # 4D image <= [N, H, W, C] or [N, C, H, W]
    # 3D image <= [1, H, W, C] or [1, C, H, W]
    # 2D image <= [1, H, W, 1]
    begin = tf.cast(tf.less_equal(original_rank, 3), dtype=tf.int32)
    end = 4 - tf.cast(tf.equal(original_rank, 2), dtype=tf.int32)
    new_shape = shape[begin:end]
    return tf.reshape(image, new_shape)


def get_random_affine(height, width, theta=10, tx=0.1, ty=0.1, zx=(0.9, 1.1), zy=(0.9, 1.1)):
    """ Wrapper to the random_affine preprocessing callable
    """
    @tf.function
    def random_affine(frames, label):
        """ Augments the frames by applying random affine transformations to them (centered).
        """
        if height is not None and width is not None:
            H, W, = height, width
        else:
            _, H, W, _ = frames.shape

        center = tf.convert_to_tensor([[1, 0, (W - 1) / 2], [0, 1, (H - 1) / 2], [0, 0, 1]])
        center_inv = tf.convert_to_tensor([[1, 0, -(W - 1) / 2], [0, 1, -(H - 1) / 2], [0, 0, 1]])

        _theta = tf.random.uniform([], -theta, theta)
        _tx = tf.random.uniform([], -W * tx, W * tx)
        _ty = tf.random.uniform([], -H * ty, H * ty)
        _zx = tf.random.uniform([], zx[0], zx[1])
        _zy = tf.random.uniform([], zy[0], zy[1])

        t_mat = tf.convert_to_tensor([[1, 0, _tx], [0, 1, _ty], [0, 0, 1]])
        z_mat = tf.convert_to_tensor([[_zx, 0, 0], [0, _zy, 0], [0, 0, 1]])
        cos = tf.cos(_theta * pi / 180)
        sin = tf.sin(_theta * pi / 180)
        rot_mat = tf.convert_to_tensor([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])

        aug_mat = tf.matmul(tf.matmul(tf.matmul(tf.matmul(center, t_mat), rot_mat), z_mat),
                            center_inv)
        proj_transform = matrices_to_flat_transforms(aug_mat)

        # Apply the transformation
        return transform(frames, proj_transform), label

    return random_affine


def extract_samples(dataset, batch_size, out_file, dtype=np.int8):
    """Extracts samples from dataset and save them to a npz file.

    Args:
        dataset (numpy.ndarray or tf.data.Dataset): dataset for extract samples
        batch_size (int): batch size over which the sequences are split
        out_file (str): name of output file
        dtype (np.dtype, optional): data type of the extracted samples. Defaults to np.int8.
    """
    # Extract samples with shape (batch_size, length, x, y, c)
    samples, _ = next(iter(dataset))
    # Reshape to (batch_size * length, x, y, c) as expected for TENNs calibration samples.
    length = samples.shape[1]
    target_shape = (samples.shape[0] * samples.shape[1], *samples.shape[2:])
    samples = np.array(tf.reshape(samples, target_shape))
    akm_extract_samples(out_file, samples, length * batch_size, dtype)
