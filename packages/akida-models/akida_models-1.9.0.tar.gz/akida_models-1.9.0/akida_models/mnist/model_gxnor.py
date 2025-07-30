#!/usr/bin/env python
# ******************************************************************************
# Copyright 2021 Brainchip Holdings Ltd.
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
GXNOR model definition for MNIST classification.
"""

__all__ = ["gxnor_mnist", "gxnor_mnist_pretrained"]

from keras import Model
from keras.layers import Input, Rescaling

from ..layer_blocks import conv_block, dense_block
from ..utils import fetch_file, get_params_by_version
from ..model_io import load_model, get_model_path, get_default_bitwidth


def gxnor_mnist():
    """ Instantiates a Keras GXNOR model with an additional dense layer to make
    better classification.

    The paper describing the original model can be found `here
    <https://www.sciencedirect.com/science/article/pii/S0893608018300108>`_.

    Note: input preprocessing is included as part of the model (as a Rescaling layer). This model
    expects inputs to be float tensors of pixels with values in the [0, 255] range.

    Returns:
        keras.Model: a Keras model for GXNOR/MNIST
    """
    # Model version management
    _, post_relu_gap, relu_activation = get_params_by_version()

    img_input = Input(shape=(28, 28, 1), name="input")
    x = Rescaling(1. / 255, name="rescaling")(img_input)

    # Block 1
    x = conv_block(x,
                   filters=32,
                   name='block_1/conv_1',
                   kernel_size=(5, 5),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=relu_activation,
                   pooling='max',
                   pool_size=(2, 2))

    # Block 2
    x = conv_block(x,
                   filters=64,
                   name='block_2/conv_1',
                   kernel_size=(3, 3),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=relu_activation,
                   strides=2,
                   pool_size=(2, 2))
    # Block 3
    x = conv_block(x,
                   filters=128,
                   name='block_3/conv_1',
                   kernel_size=(3, 3),
                   padding='same',
                   add_batchnorm=True,
                   relu_activation=relu_activation,
                   pooling='global_avg',
                   post_relu_gap=post_relu_gap)

    # Classification block
    x = dense_block(x,
                    units=512,
                    name='fc_1',
                    add_batchnorm=True,
                    relu_activation='ReLU2')
    x = dense_block(x,
                    units=10,
                    name='predictions',
                    add_batchnorm=True,
                    relu_activation=False)

    # Create model
    return Model(img_input, x, name='gxnor_mnist')


def gxnor_mnist_pretrained(quantized=True, bitwidth=None):
    """ Helper method to retrieve a `gxnor_mnist` model that was trained on MNIST dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.
        bitwidth (int, optional): the number of bits for quantized model. Defaults to None.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if bitwidth is None:
        bitwidth = get_default_bitwidth(2, 4)

    if quantized:
        if bitwidth == 2:
            model_name_v1 = 'gxnor_mnist_iq2_wq2_aq1.h5'
            file_hash_v1 = 'f6f3e077c39fa4a65e401d3758af624fb276322e1d694fbf4f773941d43e7c5f'
            model_name_v2, file_hash_v2 = None, None
        elif bitwidth == 4:
            model_name_v1, file_hash_v1 = None, None
            model_name_v2 = 'gxnor_mnist_i8_w4_a4.h5'
            file_hash_v2 = '71acbf6b4dcb77e82c3d01e031a7abb936ab4d1d91e70b84b10d8578ebb65538'
        else:
            raise ValueError(f"bitwidth={bitwidth} is not available, use bitwidth=2 or 4 for this"
                             " model.")
    else:
        model_name_v1 = 'gxnor_mnist.h5'
        file_hash_v1 = '8546a8efde963ff46e42072e2752baeb0cf984ad9a87c88e1d5ee0eb25af25f5'
        model_name_v2 = 'gxnor_mnist.h5'
        file_hash_v2 = '484bbc4cc85c1a91f135129eb45be66e31ee4f7194c97fc4352aa500b8aaed93'

    model_path, model_name, file_hash = get_model_path("gxnor", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
