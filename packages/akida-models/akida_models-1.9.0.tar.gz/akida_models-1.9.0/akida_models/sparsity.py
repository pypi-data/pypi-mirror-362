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
__all__ = ["compute_sparsity"]

import numpy as np
import tensorflow as tf
from collections import deque, defaultdict

import akida
from tensorflow.keras import Model

from akida.core import LayerType, Model as ak_model

import onnxruntime
from onnx import ModelProto
from quantizeml.onnx_support.quantization.quantize import ONNXModel
from quantizeml.onnx_support.quantization.transforms import sanitize
from quantizeml.onnx_support.graph_tools import value_info_to_tensor_shape
from quantizeml.random import generate_np_random_samples
from quantizeml.models.transforms.transforms_utils import get_layers_by_type
from quantizeml.layers import BufferTempConv, DepthwiseBufferTempConv


def compute_sparsity(model, layer_names=None, layer_types=None,
                     samples=None, batch_size=100, verbose=False):
    """Compute the sparsity of a model across selected layers and samples.

    This function loads a model from the specified path and computes the sparsity for specified
    layers (if not specified, ReLU layers for float models, layers with OutputQuantizer for
    quantized models, all layers for Akida models and Clip and ReLU nodes for ONNX models) using
    input samples.

    Args:
        model (keras.Model or onnx.ModelProto or akida.Model): the model to be analyzed.
        layer_names (list, optional): List of layer names to compute sparsity for. If None,
            sparsity is computed for relevant layers. Defaults to None.
        layer_types (tuple, optional): The types of layers for which sparsity will be computed.
            layer_types is a tuple of type when compute_sparsity is applied on Keras or Akida
            models, and a tuple of str when applied on ONNX models. Defaults to None.
        samples (np.ndarray): the sample to compute the sparsity.
            If None random samples are generated samples. Defaults to None.
        batch_size (int, optional): The number of tensors to generate or extract. Defaults to 100.
        verbose (bool, optional): Whether to print sparsity results. Defaults to False.

    Raises:
        Exception: If the model cannot be loaded or an unsupported model format is provided.

    Returns:
        dict: A dictionary where keys are layer/node names and values are the computed sparsity
        values.
    """
    if layer_names and layer_types:
        raise ValueError(
            "It is not possible to request both options, " +
            "either provide layer_names or layer_types parameter.")

    if isinstance(model, Model):
        samples_shape = model.input_shape[1:]
        dtype = model.dtype

    elif isinstance(model, ak_model):
        samples_shape = tuple(model.input_shape)
        first_layer = model.layers[0]
        if first_layer.parameters.layer_type == akida.LayerType.InputData:
            dtype = "int" if first_layer.output_signed else "uint"
            dtype += f"{np.ceil(first_layer.input_bits/8)*8:.0f}"
            dtype = np.dtype(dtype)
        else:
            dtype = np.uint8

    elif isinstance(model, ModelProto):
        model = ONNXModel(model)
        samples_shape, dtype = value_info_to_tensor_shape(model.input[0])
        samples_shape = samples_shape[1:]

    else:
        raise NotImplementedError("Sparsity computation is only " +
                                  "supported for Keras and Akida and ONNX models.")

    if samples is not None:
        if batch_size > len(samples):
            raise ValueError("Batch size exceeds the available number " +
                             "of tensors in the dataset.")
        samples = samples[:batch_size, ...].astype(dtype)
    else:
        samples = generate_np_random_samples(size=(batch_size,) + samples_shape, dtype=dtype)

    if isinstance(model, Model):
        results = _compute_sparsity_tf(model=model,
                                       layer_names=layer_names,
                                       layer_types=layer_types,
                                       samples=samples)
    elif isinstance(model, ak_model):
        results = _compute_sparsity_ak(model=model,
                                       layer_names=layer_names,
                                       layer_types=layer_types,
                                       samples=samples)
    elif isinstance(model, ONNXModel):
        results = _compute_sparsity_onnx(model=model,
                                         node_names=layer_names,
                                         node_types=layer_types,
                                         samples=samples)

    if verbose:
        for layer, sparsity in results.items():
            print(f"{layer} : {float(f'{sparsity:.3f}')}")
        print(f'Mean sparsity : {np.mean(list(results.values()))}')

    return results


def _compute_sparsity_tf(model, samples, layer_names=None, layer_types=None):
    """Compute the sparsity of selected layers in a TensorFlow model.

    This function calculates the sparsity (proportion of zero-valued elements)
    in specific layers of a TensorFlow model across a set of input samples.
    If layer names are provided, it computes sparsity for those layers, otherwise,
    it computes sparsity for all ReLU layers or layers with an OutputQuantizer.

    Args:
        model (tf.keras.Model): The TensorFlow model to analyze.
        samples (list): List of input samples to evaluate sparsity on.
        layer_names (list, optional): List of layer names to compute sparsity for. Defaults to None.
        layer_types (tuple of type, optional): The types of layers for which sparsity will be
            computed. Defaults to None. If None, it will compute sparsity for all ReLU or
            QuantizedReLU layers.

    Returns:
        dict: A dictionary where keys are layer names and values are the computed sparsity values.
    """
    outputs = []
    results = {}

    if layer_names:
        target_layers = [model.get_layer(lname) for lname in layer_names]
    elif layer_types:
        target_layers = [layer for layer in model.layers if isinstance(layer, layer_types)]
    else:
        target_layers = [layer for layer in model.layers
                         if isinstance(layer, tf.keras.layers.ReLU) or
                         hasattr(layer, 'out_quantizer') and layer.out_quantizer]

    if target_layers == []:
        raise ValueError("No layers found to compute the sparsity")

    for layer in target_layers:
        outputs.append(layer.output)

    # Force the new model to generate a list of tensors
    if len(outputs) == 1:
        outputs = [outputs]

    new_model = Model(inputs=model.inputs, outputs=outputs, name="sparsity")

    if get_layers_by_type(model, (BufferTempConv, DepthwiseBufferTempConv)):
        all_outputs = new_model(samples[0][None, ...])
        for frame in samples[1:]:
            frame = frame[None, ...]
            outputs = new_model(frame)
            for i, output in enumerate(outputs):
                all_outputs[i] = tf.concat([all_outputs[i], output], axis=0)
    else:
        all_outputs = new_model(samples)
        # If there is only one tensor in `target_layers`, wrap `all_outputs` in a list
        # to ensure `all_outputs` is always a list
        if len(target_layers) == 1:
            all_outputs = [all_outputs]
    for layer, out in zip(target_layers, all_outputs):
        if isinstance(out, tf.Tensor):
            results[layer.name] = np.sum(out == 0) / np.prod(out.shape)
        else:  # out is a FixedPoint or QTensor
            results[layer.name] = np.sum(out.values == 0) / np.prod(out.shape)
    return results


def _compute_sparsity_ak(model, samples, layer_names=None, layer_types=None):
    """Compute the sparsity of selected layers in an Akida model.

    This function calculates the sparsity (proportion of zero-valued elements)
    for specific layers in an Akida model by running forward passes on input samples.
    If layer names are provided, it computes sparsity for those layers; otherwise,
    it computes sparsity for all layers that have activation functions, excluding
    input and dequantizer layers.

    Args:
        model (akida.Model): The Akida model to analyze.
        samples (numpy.ndarray): Input samples to evaluate sparsity on.
        layer_names (list, optional): List of layer names to compute sparsity for. Defaults to None.
        layer_types (tuple of type, optional): The types of layers for which sparsity will be
            computed. Defaults to None. If None, sparsity is computed for all applicable layers
            with activations.

    Returns:
        dict: A dictionary where keys are layer names and values are the computed sparsity values.
    """
    def _search_layers_to_build_submodel(layer):
        queue, visited = [layer], []
        in_degree, dependents, queue_sort = {}, defaultdict(list), deque()
        # Search all the inbounds up to the input
        while len(queue) > 0:
            target_layer = queue.pop(0)
            visited.insert(0, target_layer)
            # Insert in queue all the inbounds of target layer
            queue.extend([ly for ly in target_layer.inbounds if ly not in visited])
            # Update dictionnaries requires to sort layer list
            in_degree[target_layer] = len(target_layer.inbounds)
            if in_degree[target_layer] == 0:
                queue_sort.append(target_layer)
            for inbound in target_layer.inbounds:
                dependents[inbound].append(target_layer)

        # Topologically sort the inbounds layers, using Kahn's algorithm
        sorted_layers = []
        while queue_sort:
            current = queue_sort.popleft()
            sorted_layers.append(current)

            # Reduce the in-degree of its dependents
            for dependent in dependents[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue_sort.append(dependent)

        return sorted_layers

    results = {}

    if layer_names:
        target_layers = [model.get_layer(lname) for lname in layer_names]
    elif layer_types:
        target_layers = [layer for layer in model.layers
                         if layer.parameters.layer_type in layer_types]
    else:
        target_layers = [layer for layer in model.layers
                         if layer.parameters.layer_type not in (LayerType.InputData,
                                                                LayerType.Dequantizer)]

    if target_layers == []:
        raise ValueError("No layers found to compute the sparsity")

    for layer in target_layers:
        sub_model = akida.Model(layers=_search_layers_to_build_submodel(layer))
        output = sub_model.forward(samples)
        results[layer.name] = np.count_nonzero(output == 0) / np.prod(output.shape)

    return results


def _compute_sparsity_onnx(model, samples, node_names=None, node_types=None):
    """Compute the sparsity of selected nodes in an ONNX model.

    This function calculates the sparsity (proportion of zero-valued elements)
    for specific nodes in an ONNX model by running forward passes on input samples.
    If node names are provided, it computes sparsity for those nodes; otherwise,
    it computes sparsity for Clip and ReLU nodes.

    Args:
        model (onnx.ModelProto): The ONNX model to analyze.
        samples (numpy.ndarray): Input samples to evaluate sparsity on.
        node_names (list, optional): List of node names to compute sparsity for. Defautls to None.
        node_types (tuple of str, optional): The types of nodes for which sparsity will be computed.
            Defaults to None. If None, sparsity is computed for Clip and ReLU nodes.

    Returns:
        dict: A dictionary where keys are node names and values are the computed sparsity values.
    """
    is_quantized = any(node.domain == "com.brainchip" for node in model.nodes())
    if not is_quantized:
        model = sanitize(model)
    if node_names:
        target_nodes = []
        for name in node_names:
            if (tnode := model.find_node_by_name(name)) is None:
                all_node_names = [node.name for node in model.nodes()]
                raise ValueError(f'No such node: {name}. Existing nodes are: [{all_node_names}].')
            target_nodes.append(tnode)
    elif node_types:
        target_nodes = [node for node in model.nodes() if node.op_type in node_types]
    elif is_quantized:
        target_nodes = [node for node in model.nodes() if node.op_type not in ("InputQuantizer",
                                                                               "Dequantizer")]
    else:
        target_nodes = [node for node in model.nodes() if node.op_type in ["Relu", "Clip"]]

    if len(target_nodes) == 0:
        raise ValueError("No nodes found to compute the sparsity")

    # Create an intermediate model with the inputs of target_nodes
    model.graph().ClearField("output")
    out_names = []
    for node in target_nodes:
        for oname in node.output:
            vi = model.find_value_info_by_name(oname)
            if vi is not None:
                model.output.append(vi)
                out_names.append(vi.name)

    samples_dict = {}
    samples_dict[model.input[0].name] = samples
    outputs = onnxruntime.InferenceSession(model.serialized).run(out_names, samples_dict)
    # Compute sparsity per node
    results = {}
    for node, output in zip(target_nodes, outputs):
        results[node.name] = np.count_nonzero(output == 0) / np.prod(output.shape)

    return results
