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
Helper that replaces activations by quantizeml.layers.Activation
"""

__all__ = ["replace_activations"]

from copy import deepcopy
from keras import layers
import tensorflow as tf

from .transforms_utils import get_layers_by_type, get_layer_index, update_layer_serialization
from ...layers import Activation
from ...models import apply_weights_to_model


def replace_activations(model):
    """ Replaces activations from a model with their equivalent Activation layer.

    This transform handles the following replacements:

        - LeakyRelu() → Activation(LeakyRelu),
        - PRelu() → Activation(LeakyRelu) (when possible).

    Args:
        model (keras.Model): the model of interest

    Returns:
        keras.Model: the original model or a new one with lambda replaced.
    """
    layer_to_name = {layers.LeakyReLU: 'leaky_relu', layers.PReLU: 'leaky_relu'}

    # Get all target activations present in the model
    activations = get_layers_by_type(model, tuple(layer_to_name))

    # When there are no valid candidates, return the original model
    if not activations:
        return model

    # Copy configuration before applying modifications
    config = deepcopy(model.get_config())
    for layer in activations:
        layer_index = get_layer_index(config['layers'], layer.name)
        layer_config = config['layers'][layer_index]
        if isinstance(layer, layers.PReLU):
            # Check if conversion is equivalent
            alpha = tf.reshape(layer.alpha, -1)
            if tf.reduce_any(alpha != alpha[0]):
                continue
            # Remove invalid parameters
            for p in ['alpha_initializer', 'alpha_regularizer', 'alpha_constraint', 'shared_axes']:
                layer_config['config'].pop(p)
            # Include alpha in config and remove it from weights
            layer_config['config']['alpha'] = float(alpha[0])
        # Include activation in config
        layer_config['config']['activation'] = layer_to_name.get(layer.__class__)
        update_layer_serialization(layer_config, Activation)

    # Reconstruct model from the config
    updated_model = model.from_config(config)

    # Restore model weights
    weights = {v.name: v for v in model.variables}
    apply_weights_to_model(updated_model, weights, verbose=False)
    return updated_model
