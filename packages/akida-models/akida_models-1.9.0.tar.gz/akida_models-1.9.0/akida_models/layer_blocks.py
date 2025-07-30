#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
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
Layers blocks definitions.
"""
from keras.layers import (BatchNormalization, ReLU, Conv2D, DepthwiseConv2D, SeparableConv2D, Dense,
                          MaxPool2D, GlobalAvgPool2D, Conv2DTranspose, Conv3D)
from keras.activations import swish, gelu
from keras.utils import register_keras_serializable
import tensorflow as tf
import numpy as np
from scipy.special import jacobi

from quantizeml.layers import DepthwiseConv2DTranspose
from .utils import get_params_by_version


def _add_pooling_layer(x, pooling_type, pool_size, padding, layer_base_name):
    """Add a pooling layer in the graph.

    From an input tensor 'x', the function returns the output tensor after
    a pooling layer defined by 'pooling_type'.

    Args:
        x (tf.Tensor): the input tensor
        pooling_type (str): type of pooling among the following: 'max' or 'global_avg'.
        pool_size (int or tuple of 2 integers): factors by which to
            downscale (vertical, horizontal). (2, 2) will halve the input in
            both spatial dimension. If only one integer is specified, the same
            window length will be used for both dimensions.
        padding (str): one of "valid" or "same" (case-insensitive).
        layer_base_name (str): base name for the pooling layer.

    Returns:
        tf.Tensor: an output tensor after pooling
    """
    if pooling_type == 'max':
        return MaxPool2D(pool_size=pool_size,
                         padding=padding,
                         name=layer_base_name + '/maxpool')(x)
    if pooling_type == 'global_avg':
        return GlobalAvgPool2D(name=layer_base_name + '/global_avg')(x)
    raise ValueError("'pooling_type' argument must be 'max' or 'global_avg'.")


def conv_block(inputs,
               filters,
               kernel_size,
               pooling=None,
               post_relu_gap=False,
               pool_size=(2, 2),
               add_batchnorm=False,
               relu_activation='ReLU3.75',
               **kwargs):
    """Adds a convolutional layer with optional layers in the following order:
    max pooling, batch normalization, activation.

    Args:
        inputs (tf.Tensor): input tensor of shape `(rows, cols, channels)`
        filters (int): the dimensionality of the output space
            (i.e. the number of output filters in the convolution).
        kernel_size (int or tuple of 2 integers): specifying the
            height and width of the 2D convolution kernel.
            Can be a single integer to specify the same value for
            all spatial dimensions.
        pooling (str, optional): add a pooling layer of type 'pooling' among the values 'max' or
            'global_avg', with pooling size set to pool_size. If 'None', no pooling will be added.
        post_relu_gap (bool, optional): when pooling is 'global_avg', indicates if the pooling comes
            before or after ReLU activation. Defaults to False.
        pool_size (int or tuple of 2 integers, optional): factors by which to downscale (vertical,
            horizontal). (2, 2) will halve the input in both spatial dimension. If only one integer
            is specified, the same window length will be used for both dimensions.
        add_batchnorm (bool, optional): add a BatchNormalization layer
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        **kwargs: arguments passed to the keras.Conv2D layer, such as
            strides, padding, use_bias, weight_regularizer, etc.

    Returns:
        tf.Tensor: output tensor of conv2D block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in conv_block must be None.")
    if 'dilation_rate' in kwargs and kwargs['dilation_rate'] not in [1, [1, 1], (1, 1)]:
        raise ValueError("Keyword argument 'dilation_rate' is not supported in conv_block.")

    conv_layer = Conv2D(filters, kernel_size, **kwargs)
    x = conv_layer(inputs)

    if pooling == 'max' or (pooling == 'global_avg' and not post_relu_gap):
        x = _add_pooling_layer(x, pooling, pool_size, conv_layer.padding, conv_layer.name)

    if add_batchnorm:
        x = BatchNormalization(name=conv_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=conv_layer.name + '/relu')(x)

    if post_relu_gap and pooling == 'global_avg':
        x = _add_pooling_layer(x, pooling, pool_size, conv_layer.padding, conv_layer.name)
    return x


def separable_conv_block(inputs,
                         filters,
                         kernel_size,
                         strides=1,
                         padding="same",
                         use_bias=True,
                         pooling=None,
                         post_relu_gap=False,
                         pool_size=(2, 2),
                         add_batchnorm=False,
                         relu_activation='ReLU3.75',
                         fused=True,
                         name=None,
                         kernel_initializer='glorot_uniform',
                         pointwise_regularizer=None):
    """Adds a separable convolutional layer with optional layers in the
    following order: global average pooling, max pooling, batch normalization,
    activation.

    Args:
        inputs (tf.Tensor): input tensor of shape `(height, width, channels)`
        filters (int): the dimensionality of the output space
            (i.e. the number of output filters in the pointwise convolution).
        kernel_size (int or tuple of 2 integers): specifying the
            height and width of the 2D convolution window. Can be a single
            integer to specify the same value for all spatial dimensions.
        strides (int or tuple of 2 integers, optional): strides of the depthwise convolution.
            Defaults to 1.
        padding (str, optional): padding mode for the depthwise convolution. Defaults to 'same'.
        use_bias (bool, optional): whether the layer uses a bias vector. Defaults to True.
        pooling (str, optional): add a pooling layer of type 'pooling' among the values 'max', or
            'global_avg', with pooling size set to pool_size. If 'None', no pooling will be added.
        post_relu_gap (bool, optional): when pooling is 'global_avg', indicates if the pooling comes
            before or after ReLU activation. Defaults to False.
        pool_size (int or tuple of 2 integers, optional): factors by which to downscale (vertical,
            horizontal). (2, 2) will halve the input in both spatial dimension. If only one integer
            is specified, the same window length will be used for both dimensions.
        add_batchnorm (bool, optional): add a BatchNormalization layer
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        fused (bool, optional): If True use a SeparableConv2D layer otherwise use a
            DepthwiseConv2D + Conv2D layers. Defaults to True.
        name (str, optional): name of the layer. Defaults to None.
        kernel_initializer (keras.initializer, optional): initializer for both kernels. Defaults to
            'glorot_uniform'.
        pointwise_regularizer (keras.regularizers, optional): regularizer function applied to the
            pointwise kernel matrix. Defaults to None.

    Returns:
        tf.Tensor: output tensor of separable conv block.
    """
    if name:
        dw_name = "dw_" + name
        pw_name = "pw_" + name

    else:
        dw_name = pw_name = None
    # if fused set a SeparableConv2D layer
    if fused:
        sep_conv_layer = SeparableConv2D(filters, kernel_size, strides=strides, padding=padding,
                                         use_bias=use_bias,
                                         depthwise_initializer=kernel_initializer,
                                         pointwise_initializer=kernel_initializer,
                                         pointwise_regularizer=pointwise_regularizer,
                                         name=name)
        x = sep_conv_layer(inputs)
        main_layer_name = sep_conv_layer.name
    # if not fused set a DepthwiseConv2D + Conv2D layer (the Conv2D applies a Pointwise convolution)
    else:
        depth_conv_layer = DepthwiseConv2D(kernel_size, strides=strides, padding=padding,
                                           use_bias=False,
                                           depthwise_initializer=kernel_initializer,
                                           name=dw_name)
        point_conv_layer = Conv2D(filters, (1, 1), use_bias=use_bias, padding='same',
                                  kernel_initializer=kernel_initializer,
                                  kernel_regularizer=pointwise_regularizer,
                                  name=pw_name)

        x = depth_conv_layer(inputs)
        x = point_conv_layer(x)

        main_layer_name = point_conv_layer.name

    if pooling == 'max' or (pooling == 'global_avg' and not post_relu_gap):
        x = _add_pooling_layer(x, pooling, pool_size, padding, main_layer_name)

    if add_batchnorm:
        x = BatchNormalization(name=main_layer_name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=main_layer_name + '/relu')(x)

    if post_relu_gap and pooling == 'global_avg':
        x = _add_pooling_layer(x, pooling, pool_size, padding, main_layer_name)
    return x


def dense_block(inputs,
                units,
                add_batchnorm=False,
                relu_activation='ReLU3.75',
                **kwargs):
    """Adds a dense layer with optional layers in the following order:
    batch normalization, activation.

    Args:
        inputs (tf.Tensor): Input tensor of shape `(rows, cols, channels)`
        units (int): dimensionality of the output space
        add_batchnorm (bool, optional): add a BatchNormalization layer
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        **kwargs: arguments passed to the Dense layer, such as
            use_bias, kernel_initializer, weight_regularizer, etc.

    Returns:
        tf.Tensor: output tensor of the dense block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in dense_block must be None.")

    dense_layer = Dense(units, **kwargs)
    x = dense_layer(inputs)

    if add_batchnorm:
        x = BatchNormalization(name=dense_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=dense_layer.name + '/relu')(x)

    return x


def act_to_layer(act, **kwargs):
    """ Get activation layer from string.

    This is needed because one cannot serialize a class in layer.get_config, the string is thus
    serialized instead.

    Args:
        act (str): string that values in ['GeLU', 'ReLUx', 'swish'] and that allows to choose from
            GeLU, ReLUx or swish activation inside MLP.

    Returns:
        keras.layers: the activation layer class
    """
    if act == 'GeLU':
        act_funct = gelu
    elif 'ReLU' in act:
        if act == 'ReLU':
            max_value = None
        else:
            try:
                max_value = float(act[4:])
            except ValueError:
                raise ValueError("ReLU must be in the form 'ReLUx', where x is the max-value")
        act_funct = ReLU(max_value=max_value, **kwargs)
    elif act == 'swish':
        act_funct = swish
    else:
        raise NotImplementedError(
            f"act should be in ['GeLU', 'ReLUx', 'swish'] but received {act}.")

    return act_funct


def conv_transpose_block(inputs,
                         filters,
                         kernel_size,
                         add_batchnorm=False,
                         relu_activation='ReLU8',
                         **kwargs):
    """Adds a transposed convolutional layer with optional layers in the following order:
    batch normalization, activation.

    Args:
        inputs (tf.Tensor): input tensor of shape `(rows, cols, channels)`
        filters (int): the dimensionality of the output space (i.e. the number of output filters in
            the convolution).
        kernel_size (int or tuple of 2 integers): specifying the height and width of the 2D
            convolution kernel. Can be a single integer to specify the same value for all spatial
            dimensions.
        add_batchnorm (bool, optional): add a BatchNormalization layer. Defaults to False.
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        **kwargs: arguments passed to the keras.Conv2DTranspose layer, such as strides, padding,
            use_bias, weight_regularizer, etc.

    Returns:
        tf.Tensor: output tensor of transposed convolution block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in conv_transpose_block must be None.")
    if 'dilation_rate' in kwargs and kwargs['dilation_rate'] not in [1, [1, 1], (1, 1)]:
        raise ValueError("Keyword argument 'dilation_rate' is not supported in "
                         "conv_transpose_block.")

    conv_trans_layer = Conv2DTranspose(filters, kernel_size, **kwargs)
    x = conv_trans_layer(inputs)

    if add_batchnorm:
        x = BatchNormalization(name=conv_trans_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=conv_trans_layer.name + '/relu')(x)

    return x


def sepconv_transpose_block(inputs,
                            filters,
                            kernel_size,
                            strides=2,
                            padding='same',
                            use_bias=True,
                            add_batchnorm=False,
                            relu_activation='ReLU3.75',
                            name=None,
                            kernel_initializer='glorot_uniform',
                            pointwise_regularizer=None):
    """Adds a transposed separable convolutional layer with optional layers in the following order:
    batch normalization, activation.

    The separable operation is made of a DepthwiseConv2DTranspose followed by a pointwise Conv2D.

    Args:
        inputs (tf.Tensor): input tensor of shape `(rows, cols, channels)`
        filters (int): the dimensionality of the output space (i.e. the number of output filters in
            the pointwise convolution).
        kernel_size (int or tuple of 2 integers): specifying the height and width of the depthwise
            transpose kernel. Can be a single integer to specify the same value for all spatial
            dimensions.
        strides (int or tuple of 2 integers, optional): strides of the transposed depthwise.
            Defaults to 2.
        padding (str, optional): padding mode for the transposed depthwise. Defaults to 'same'.
        use_bias (bool, optional): whether the layer uses a bias vectors. Defaults to True.
        add_batchnorm (bool, optional): add a BatchNormalization layer. Defaults to False.
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        name (str, optional): name of the layer. Defaults to None.
        kernel_initializer (keras.initializer, optional): initializer for both kernels. Defaults to
            'glorot_uniform'.
        pointwise_regularizer (keras.regularizers, optional): regularizer function applied to the
            pointwise kernel matrix. Defaults to None.

    Returns:
        tf.Tensor: output tensor of transposed separable convolution block.
    """
    if name:
        dw_name = "dw_" + name
        pw_name = "pw_" + name
    else:
        dw_name, pw_name = None, None

    dw_trans_layer = DepthwiseConv2DTranspose(kernel_size,
                                              strides=strides,
                                              padding=padding,
                                              use_bias=use_bias,
                                              depthwise_initializer=kernel_initializer,
                                              name=dw_name)
    pw_layer = Conv2D(filters,
                      kernel_size=1,
                      padding='valid',
                      use_bias=use_bias,
                      kernel_regularizer=pointwise_regularizer,
                      kernel_initializer=kernel_initializer,
                      name=pw_name)

    x = dw_trans_layer(inputs)
    x = pw_layer(x)

    if add_batchnorm:
        x = BatchNormalization(name=pw_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=pw_layer.name + '/relu')(x)

    return x


def yolo_head_block(x, num_boxes, classes, filters=1024):
    """Adds the `YOLOv2 detection head <https://arxiv.org/pdf/1612.08242.pdf>`_, at the output
    of a model.

    Args:
        x (:obj:`tf.Tensor`): input tensor of shape `(rows, cols, channels)`.
        num_boxes (int): number of boxes.
        classes (int): number of classes.
        filters (int, optional): number of filters in hidden layers. Defaults to 1024.

    Returns:
        :obj:`tf.Tensor`: output tensor of yolo detection head block.

    Notes:
        This block replaces conv layers by separable_conv, to decrease the amount of parameters.
    """
    # Model version management
    fused, _, relu_activation = get_params_by_version(relu_v2='ReLU7.5')

    x = separable_conv_block(x, filters=filters, name='1conv',
                             kernel_size=(3, 3), padding='same', use_bias=False,
                             relu_activation=relu_activation, add_batchnorm=True, fused=fused)
    x = separable_conv_block(x, filters=filters, name='2conv',
                             kernel_size=(3, 3), padding='same', use_bias=False,
                             relu_activation=relu_activation, add_batchnorm=True, fused=fused)
    x = separable_conv_block(x, filters=filters, name='3conv',
                             kernel_size=(3, 3), padding='same', use_bias=False,
                             relu_activation=relu_activation, add_batchnorm=True, fused=fused)
    x = separable_conv_block(x, filters=(num_boxes * (4 + 1 + classes)), name='detection_layer',
                             kernel_size=(3, 3), padding='same', use_bias=True,
                             relu_activation=False, add_batchnorm=False, fused=fused)
    return x


def get_ortho_polynomials(length, degrees, alpha, beta):
    """ Generate the set of Jacobi orthogonal polynomials with shape (degrees + 1, length)

    Args:
        length (int): The length of the discretized temporal kernel,
            assuming the range [0, 1] for the polynomials.
        degrees (int): The maximum polynomial degree. Note that degrees + 1 polynomials
            will be generated (counting the constant).
        alpha (float): The alpha Jacobi parameter.
        beta (float): The beta Jacobi parameter.

    Returns:
        np.ndarray: shaped (degrees + 1, length)
    """
    coeffs = np.vstack([np.pad(np.flip(jacobi(degree, alpha, beta).coeffs), (0, degrees - degree))
                        for degree in range(degrees + 1)]).astype(np.float32)
    steps = np.linspace(0, 1, length + 1)
    X = np.stack([steps ** (i + 1) / (i + 1) for i in range(degrees + 1)])
    polynomials_integrated = coeffs @ X
    transform = np.diff(polynomials_integrated, 1, -1) * length
    return transform


@register_keras_serializable()
class PleiadesLayer(Conv3D):
    """A 3D convolutional layer utilizing orthogonal polynomials for kernel transformation.

    Inherits from `Conv3D` and modifies its kernel transformation before applying convolution.

    Args:
        filters (int): Number of output filters.
        kernel_size (tuple): Size of the convolution kernel.
        degrees (int): Degree of the orthogonal polynomials.
        alpha (float): Alpha parameter for the orthogonal polynomials.
        beta (float): Beta parameter for the orthogonal polynomials.
        **kwargs: Additional arguments passed to `Conv3D`.
    """
    def __init__(self, filters, kernel_size, degrees, alpha, beta, **kwargs):
        super().__init__(filters, kernel_size, **kwargs)

        self.degrees = degrees
        self.alpha = alpha
        self.beta = beta

    def build(self, input_shape):
        with tf.name_scope(self.name + '/'):
            super().build(input_shape)
            # Generate the transformation matrix
            transform = get_ortho_polynomials(self.kernel_size[0], self.degrees, self.alpha,
                                              self.beta)
            transform = tf.convert_to_tensor(transform, dtype=tf.float32)
            # Normalize transform based on input dimensions
            scale = tf.sqrt(tf.cast(input_shape[-1],
                                    tf.float32)) * tf.sqrt(tf.cast(self.kernel_size[0],
                                                                   tf.float32))
            self.transform = transform / scale
            new_kernel_shape = (self.kernel.shape[-2], self.filters, self.kernel_size[1],
                                self.kernel_size[2], self.degrees + 1)
            self.kernel = self.add_weight(shape=new_kernel_shape,
                                          initializer=self.kernel_initializer,
                                          trainable=True, name="kernel")

    def call(self, inputs):
        # Apply polynomial transformation to kernel
        kernel = tf.tensordot(self.kernel, self.transform, axes=[[4], [0]])
        kernel = tf.transpose(kernel, perm=[4, 2, 3, 0, 1])
        # Perform convolution with transformed kernel
        if self.groups > 1:
            # The '_jit_compiled_convolution_op' is a specialized operation that efficiently
            # handles grouped convolutions, addressing limitations in some TensorFlow versions
            # where grouped convolutions are not directly supported.
            conv_output = self._jit_compiled_convolution_op(inputs, kernel)
        else:
            conv_output = self.convolution_op(inputs, kernel)
        if self.use_bias:
            conv_output = tf.nn.bias_add(conv_output, self.bias)
        return conv_output

    def get_config(self):
        config = super().get_config()
        config.update({
            'degrees': self.degrees,
            'alpha': self.alpha,
            'beta': self.beta
        })
        return config


def conv3d_block(inputs,
                 filters,
                 kernel_size,
                 add_batchnorm=False,
                 relu_activation='ReLU3.75',
                 reg_factor=None,
                 normalize_reg=False,
                 use_pleiades=False,
                 degrees=None,
                 alpha=None,
                 beta=None,
                 **kwargs):
    """Adds a Conv3D layer with optional layers: batch normalization and activation.

    Args:
        inputs (tf.Tensor): input tensor
        filters (int): the dimensionality of the output space
        kernel_size (int or tuple): dimensions of the convolution kernel.
        add_batchnorm (bool, optional): add a BatchNormalization layer. Defaults to False.
        relu_activation (str, optional): the ReLU activation to add to the layer in the form 'ReLUx'
            where 'x' is the max_value to use. Set to False to disable activation. Defaults to
            'ReLU3.75'.
        reg_factor (float, optional): the L1-regularization factor of the ActivityRegularization
            layers that are added after the ReLU layers if reg_factor is not None.
            Defaults to None.
        normalize_reg (bool, optional): if True, normalize the L1-regularization factor.
            Defaults to False.
        use_pleiades (bool, optional): if True, the first conv3d of the TemporalBlock
            is a PleiadesLayer. Defaults to False.
        degrees (int, optional): The maximum polynomial degree of the Jacobi matrix. It needs to be
            set if use_pleiades is True. Defaults to None.
        alpha (int, optional): The alpha Jacobi parameter. It needs to be set if
            use_pleiades is True. Defaults to None.
        beta (int, optional): The beta Jacobi parameter. It needs to be set if use_pleiades is True.
            Defaults to None.
        **kwargs: arguments passed to the keras.Conv3D layer, such as strides, use_bias, etc.

    Returns:
        tf.Tensor: output tensor of conv2D block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in conv3d_block must be None.")
    # If it's a temporal Conv3d with a same padding, convert it to a one sided-left padding,
    # by adding a ZeroPadding3D layer and setting the Conv3D padding to "valid"
    if kernel_size[0] != 1 and kwargs.get('padding', 'valid') == 'same':
        padding_layer = tf.keras.layers.ZeroPadding3D(
            padding=((kernel_size[0] - 1, 0), (0, 0), (0, 0)))
        inputs = padding_layer(inputs)
        kwargs['padding'] = 'valid'
    if use_pleiades:
        assert degrees and alpha and beta
        conv_layer = PleiadesLayer(filters, kernel_size, degrees, alpha, beta, **kwargs)
    else:
        conv_layer = Conv3D(filters, kernel_size, **kwargs)
    x = conv_layer(inputs)

    if add_batchnorm:
        x = BatchNormalization(name=conv_layer.name + '/BN')(x)

    if relu_activation:
        x = act_to_layer(relu_activation, name=conv_layer.name + '/relu')(x)
        if reg_factor:
            if normalize_reg:
                reg_factor /= np.prod(x.shape[1:])
            x = tf.keras.layers.ActivityRegularization(l1=reg_factor)(x)
    return x


def temporal_block(inputs, in_channels, out_channels, t_kernel_size,
                   depthwise, index, reg_factor=None, normalize_reg=False,
                   use_pleiades=False, degrees=None, alpha=None, beta=None):
    """ Add a temporal block to the inputs.

    Note that the depthwise layers are implemented as Conv3D with groups=filters because TensorFlow
    does not have a DepthwiseConv3D layer.

    Args:
        inputs (tf.Tensor): input tensor
        in_channels (int): input channels
        out_channels (int): output channels
        t_kernel_size (int): the temporal kernel size
        depthwise (bool): whether the temporal layer is dw_separable
        index (int): index of the block
        reg_factor (float, optional): the L1-regularization factor of the ActivityRegularization
            layers that are added after the ReLU layers if reg_factor is not None.
            Defaults to None.
        normalize_reg (bool, optional): if True, normalize the L1-regularization factor.
            Defaults to False.
        use_pleiades (bool, optional): if True, the first conv3d of the temporal block
            is a PleiadesLayer. Defaults to False.
        degrees (int, optional): The maximum polynomial degree of the Jacobi matrix. It needs to be
            set if use_pleiades is True. Defaults to None.
        alpha (int, optional): The alpha Jacobi parameter. It needs to be set if
            use_pleiades is True. Defaults to None.
        beta (int, optional): The beta Jacobi parameter. It needs to be set if use_pleiades is True.
            Defaults to None.

    Returns:
        tf.Tensor: output tensor of the temporal block.
    """
    if not depthwise:
        x = conv3d_block(inputs,
                         out_channels,
                         (t_kernel_size, 1, 1),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         strides=(1, 1, 1),
                         padding='same',
                         use_bias=True,
                         name=f'convt_full_{index}',
                         reg_factor=reg_factor,
                         normalize_reg=normalize_reg,
                         use_pleiades=use_pleiades,
                         degrees=degrees,
                         alpha=alpha,
                         beta=beta)
    else:
        # This is a DepthwiseConv3D (groups=filters)
        x = conv3d_block(inputs,
                         in_channels,
                         (t_kernel_size, 1, 1),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         strides=(1, 1, 1),
                         padding='same',
                         groups=in_channels,
                         use_bias=False,
                         name=f'convt_dw_{index}',
                         reg_factor=reg_factor,
                         normalize_reg=normalize_reg,
                         use_pleiades=use_pleiades,
                         degrees=degrees,
                         alpha=alpha,
                         beta=beta)
        x = conv3d_block(x,
                         out_channels,
                         (1, 1, 1),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         name=f'convt_pw_{index}',
                         reg_factor=reg_factor,
                         normalize_reg=normalize_reg)
    return x


def spatial_block(inputs, in_channels, out_channels, depthwise, index, reg_factor=None,
                  normalize_reg=False):
    """ Add a spatial block to the inputs.

    Note that the depthwise layers are implemented as Conv3D with groups=filters because TensorFlow
    does not have a DepthwiseConv3D layer.

    Args:
        inputs (tf.Tensor): input tensor
        in_channels (int): input channels
        out_channels (int): output channels
        depthwise (bool): whether the spatial layer is dw_separable
        index (int): index of the block
        reg_factor (float, optional): the L1-regularization factor of the ActivityRegularization
            layers that are added after the ReLU layers if reg_factor is not None.
            Defaults to None.
        normalize_reg (bool, optional): if True, normalize the L1-regularization factor.
            Defaults to False.

    Returns:
        tf.Tensor: output tensor of the spatial block.
    """
    if not depthwise:
        x = conv3d_block(inputs,
                         out_channels,
                         (1, 3, 3),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         strides=(1, 2, 2),
                         padding='same',
                         use_bias=True,
                         name=f'convs_full_{index}',
                         reg_factor=reg_factor,
                         normalize_reg=normalize_reg)
    else:
        # This is a DepthwiseConv3D (groups=filters)
        x = conv3d_block(inputs,
                         in_channels,
                         (1, 3, 3),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         strides=(1, 2, 2),
                         padding='same',
                         groups=in_channels,
                         use_bias=False,
                         name=f'convs_dw_{index}',
                         reg_factor=reg_factor,
                         normalize_reg=normalize_reg)
        x = conv3d_block(x,
                         out_channels,
                         (1, 1, 1),
                         add_batchnorm=True,
                         relu_activation='ReLU',
                         name=f'convs_pw_{index}',
                         reg_factor=reg_factor,
                         normalize_reg=normalize_reg)
    return x


def spatiotemporal_block(inputs, in_channels, med_channels, out_channels, t_kernel_size,
                         t_depthwise, s_depthwise, index, temporal_first=True, reg_factor=None,
                         normalize_reg=False, use_pleiades=False, degrees=None, alpha=None,
                         beta=None):
    """ Add a spatiotemporal block to the inputs.

    The spatio-temporal block consists of a temporal convolution (potentially separable) followed by
    a spatial convolution (potentially separable) or the inverse.

    Note that the depthwise layers are implemented as Conv3D with groups=filters because TensorFlow
    does not have a DepthwiseConv3D layer.

    Args:
        inputs (tf.Tensor): input tensor
        in_channels (int): input channels
        med_channels (int): intermediate channels between blocks
        out_channels (int): output channels
        t_kernel_size (int): the temporal kernel size
        t_depthwise (bool): whether the temporal layer is dw_separable
        s_depthwise (bool): whether the spatial layer is dw_separable
        index (int): index of the block
        temporal_first (bool, optional): if True, the first block is a temporal block.
            Defaults to True.
        reg_factor (float, optional): the L1-regularization factor of the ActivityRegularization
            layers that are added after the ReLU layers if reg_factor is not None.
            Defaults to None.
        normalize_reg (bool, optional): if True, normalize the L1-regularization factor.
            Defaults to False.
        use_pleiades (bool, optional): if True, the first conv3d of the TemporalBlock
            is a PleiadesLayer. Defaults to False.
        degrees (int, optional): The maximum polynomial degree of the Jacobi matrix. It needs to be
            set if use_pleiades is True. Defaults to None.
        alpha (int, optional): The alpha Jacobi parameter. It needs to be set if
            use_pleiades is True. Defaults to None.
        beta (int, optional): The beta Jacobi parameter. It needs to be set if use_pleiades is True.
            Defaults to None.

    Returns:
        tf.Tensor: output tensor of the spatiotemporal block.
    """
    if temporal_first:
        x = temporal_block(inputs, in_channels, med_channels, t_kernel_size,
                           t_depthwise, index, reg_factor=reg_factor, normalize_reg=normalize_reg,
                           use_pleiades=use_pleiades, degrees=degrees, alpha=alpha, beta=beta)
        x = spatial_block(x, med_channels, out_channels, s_depthwise, index, reg_factor=reg_factor,
                          normalize_reg=normalize_reg)
    else:
        x = spatial_block(inputs, in_channels, med_channels, s_depthwise, index,
                          reg_factor=reg_factor, normalize_reg=normalize_reg)
        x = temporal_block(x, med_channels, out_channels, t_kernel_size,
                           t_depthwise, index, reg_factor=reg_factor, normalize_reg=normalize_reg,
                           use_pleiades=use_pleiades, degrees=degrees, alpha=alpha, beta=beta)
    return x
