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
Sanitize to add an identity convolution after some pattern
"""

__all__ = ['insert_identity_convs']

import keras
import numpy as np

from ... import layers as qml_layers
from ..utils import apply_weights_to_model
from .insert_layer import insert_in_config
from .transforms_utils import find_layers_pairs, get_layer_index, update_inbound


def _insert_add_identity_relu_gap(model):
    # Adds an identity convolution after 'Add' in the {Add > Relu > GlobalAveragePool} pattern
    map_add_layer_to_relu_gap = _find_add_relu_gap_sequences(model)

    # When there are no valid candidates, return the original model
    if len(map_add_layer_to_relu_gap) == 0:
        return model

    return _insert_conv_identity(model, map_add_layer_to_relu_gap)


def _insert_identity_after_skips(model):
    # Adds an identity convolution after a skip connection if next operator is not mappable in CNP.
    candidates = _find_skip_sequences(model)

    # When there are no valid candidates, return the original model
    if len(candidates) == 0:
        return model

    return _insert_conv_identity(model, candidates)


def _insert_identity_after_hrc(model):
    # Adds an identity convolution after a HRC block with multi-outbounds.
    candidates = _find_hrc_with_multi_outbounds(model)

    # When there are no valid candidates, return the original model
    if len(candidates) == 0:
        return model

    return _insert_conv_identity(model, candidates)


def _insert_identity_to_force_different_inbounds(model):
    # Adds an identity convolution before a skip connection if it has the same inputs
    candidates = _find_skip_with_same_inbounds(model)

    # When there are no valid candidates, return the original model
    if len(candidates) == 0:
        return model

    variables_dict = {var.name: var for var in model.variables}
    config = model.get_config()
    layers = config["layers"]

    for candidate in candidates:
        layer_index = get_layer_index(layers, candidate.name)

        # inbound_nodes rpr: [['inbound_1', 0, 0, {}], ['inbound_2', 0, 0, {}]]
        first_inbound_name = layers[layer_index]['inbound_nodes'][0][0][0]

        # Find number of filters from the inbound
        filters = model.get_layer(first_inbound_name).output_shape[0][-1]

        # Create a new identity convolution layer
        id_conv_name = f"{first_inbound_name}_identity_conv"
        id_conv_config = keras.saving.serialize_keras_object(
            keras.layers.Conv2D(filters=filters,
                                kernel_size=(1, 1),
                                use_bias=False,
                                name=id_conv_name))

        # Connect id_conv to the first inbound
        id_conv_config["inbound_nodes"] = [[[first_inbound_name, 0, 0, {}]]]
        id_conv_config["name"] = id_conv_name

        # Update the first candidate inbound to be id_conv
        layers[layer_index]['inbound_nodes'][0][0][0] = id_conv_name

        # Store weights of the identity convolution layer
        variables_dict[f'{id_conv_name}/kernel:0'] = np.eye(filters)[None, None]

        # Add id conv to config
        layers.append(id_conv_config)

    # Build the new model
    updated_model = model.from_config(config)
    apply_weights_to_model(updated_model, variables_dict)

    return updated_model


def _insert_identity_to_force_two_outbounds(model):
    target_layers = _find_nodes_with_more_than_two_outbounds(model)

    # When there are no valid candidates, return the original model
    if len(target_layers) == 0:
        return model

    variables_dict = {var.name: var for var in model.variables}
    config = model.get_config()
    layers = config["layers"]

    for layer in target_layers:
        outbound_names = [node.layer.name for node in layer.outbound_nodes]

        while len(outbound_names) > 2:
            filters = model.get_layer(layer.name).output_shape[-1]
            id_conv_name = f"{layer.name}_identity_conv_{len(outbound_names)}"
            id_conv_config = keras.saving.serialize_keras_object(
                keras.layers.Conv2D(filters=filters,
                                    kernel_size=(1, 1),
                                    use_bias=False,
                                    name=id_conv_name))
            # Connect the identity conv to the target layer
            id_conv_config["inbound_nodes"] = [[[layer.name, 0, 0, {}]]]
            id_conv_config["name"] = id_conv_name

            # Store weights of the identity convolution layer
            variables_dict[f'{id_conv_name}/kernel:0'] = np.eye(filters)[None, None]

            # Get the last two outbounds and update their inbound to be the identity conv
            outbound1_id = get_layer_index(layers, outbound_names.pop())
            outbound2_id = get_layer_index(layers, outbound_names.pop())
            update_inbound(layers[outbound1_id], layer.name, id_conv_name)
            update_inbound(layers[outbound2_id], layer.name, id_conv_name)

            # Add identity Conv to the outbounds of the layer
            # (it is like merging the last two outbounds into the identity conv)
            outbound_names.append(id_conv_name)

            # Add id conv to config
            layers.append(id_conv_config)

    updated_model = model.from_config(config)
    apply_weights_to_model(updated_model, variables_dict)

    return updated_model


def _find_add_relu_gap_sequences(model):
    def _filter_pairs(src_layer, dst_layer):
        out_nodes = dst_layer.outbound_nodes
        # Check if dst_layer has a Relu as outbound and src_layer is a single Add (no activation)
        return (len(out_nodes) == 1 and
                isinstance(out_nodes[0].outbound_layer, keras.layers.GlobalAveragePooling2D) and
                not (isinstance(src_layer, qml_layers.Add) and src_layer.activation))

    supported_layers = (keras.layers.Add, qml_layers.Add)
    candidates = find_layers_pairs(model, supported_layers, keras.layers.ReLU)

    # Filter incompatible pairs
    return {parent: dest for parent, dest in candidates.items() if _filter_pairs(parent, dest)}


def _find_skip_sequences(model):
    supported_layers = (keras.layers.Add, qml_layers.Add, keras.layers.Concatenate)
    supported_conv_layers = (keras.layers.Conv2D, keras.layers.Conv2DTranspose)
    target_layers = set()

    for layer in model.layers:
        if isinstance(layer, supported_layers):
            # Transformation must be applied if no outbound or no outbound that is mappable in CNP
            # and output is a 4D tensor
            if not any(isinstance(outbound_node.outbound_layer, supported_conv_layers)
                       for outbound_node in layer.outbound_nodes) and len(layer.output_shape) == 4:
                target_layers.add(layer)

    return target_layers


def _find_hrc_with_multi_outbounds(model):
    # This sanitize does not support models with multiple inputs
    if len(model.inputs) != 1:
        return []

    # Skip input/rescaling layer(s)
    target = model.layers[0]
    rescaling_layers = (keras.layers.InputLayer, keras.layers.Rescaling)
    while len(target.outbound_nodes) == 1 and isinstance(target, rescaling_layers):
        target = target.outbound_nodes[0].outbound_layer

    # Check if the first layer is a HRC Conv2D layer
    if not (isinstance(target, keras.layers.Conv2D) and target.input_shape[-1] in [1, 3]):
        return []

    # Skip activation/maxpool layer(s)
    supported_layers = (keras.layers.ReLU, keras.layers.MaxPool2D, qml_layers.Activation)
    while len(target.outbound_nodes) == 1 and isinstance(
            target.outbound_nodes[0].outbound_layer, supported_layers):
        target = target.outbound_nodes[0].outbound_layer

    # Check if the target layer has multiple outbound nodes
    if len(target.outbound_nodes) <= 1:
        return []
    return [target]


def _find_skip_with_same_inbounds(model):
    supported_layers = (keras.layers.Add, qml_layers.Add, keras.layers.Concatenate)
    target_layers = []

    for layer in model.layers:
        if isinstance(layer, supported_layers):
            # Check that the skip layer has 2 inputs and they are the same
            if len(layer.input) == 2 and layer.input[0].name == layer.input[1].name:
                target_layers.append(layer)

    return target_layers


def _find_nodes_with_more_than_two_outbounds(model):
    target_layers = set()
    for layer in model.layers:
        if len(layer.outbound_nodes) > 2 and len(layer.output_shape) == 4:
            target_layers.add(layer)

    return target_layers


def _insert_conv_identity(model, candidates):
    config = model.get_config()
    variables_dict = {var.name: var for var in model.variables}
    for add_layer in candidates:
        # Create a new identity convolution layer
        identity_conv = keras.layers.Conv2D(filters=add_layer.output_shape[-1],
                                            kernel_size=(1, 1),
                                            use_bias=False,
                                            name=f"{add_layer.name}_identity_conv")

        # Insert the identity convolution layer in the model configuration
        insert_in_config(model, add_layer.name, identity_conv, config)

        # Store weights of the identity convolution layer
        variables_dict[f'{identity_conv.name}/kernel:0'] = np.eye(identity_conv.filters)[None, None]

    # Build the new model
    updated_model = model.from_config(config)
    apply_weights_to_model(updated_model, variables_dict)
    return updated_model


def insert_identity_convs(model):
    """Adds an identity convolution after some patterns.

    Args:
        model (keras.Model): a model to be processed.

    Returns:
        keras.Model: the new model.
    """
    model = _insert_add_identity_relu_gap(model)
    model = _insert_identity_after_skips(model)
    model = _insert_identity_after_hrc(model)
    model = _insert_identity_to_force_different_inbounds(model)
    model = _insert_identity_to_force_two_outbounds(model)
    return model
