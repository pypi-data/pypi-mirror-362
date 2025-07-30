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
Activation > MaxPool inversion helper.
"""

__all__ = ["invert_activation_maxpool"]

from keras.layers import MaxPool2D, ReLU

from ...layers import Activation
from .transforms_utils import find_layers_pairs, invert_layer_pairs


def invert_activation_maxpool(model):
    """ Inverts ReLU/Activation and MaxPool2D layers in a model to have MaxPool2D first.

    This transformation produces a strictly equivalent model.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: keras.Model: the original model or the updated model
    """
    def _filter_pairs(parent_layer, dst_layer):
        return not (isinstance(parent_layer, Activation) and
                    parent_layer.activation not in ["leaky_relu"])

    # Find ReLU/Activation followed by MaxPool2D layer pairs that are candidates for inversion
    map_activation_mp = find_layers_pairs(model, (ReLU, Activation), MaxPool2D)

    # Filter incompatible pairs
    map_activation_mp = {parent: dest for parent, dest in map_activation_mp.items()
                         if _filter_pairs(parent, dest)}

    # When there are no valid candidates, return the original model
    if not map_activation_mp:
        return model

    # Rebuild a model with MP and ReLU inverted by editing the configuration
    return invert_layer_pairs(model, map_activation_mp)
