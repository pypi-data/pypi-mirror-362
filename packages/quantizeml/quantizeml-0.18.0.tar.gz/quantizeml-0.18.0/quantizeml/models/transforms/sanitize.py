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
Helper that prepares a model for quantization.
"""

__all__ = ['sanitize']

from . import (align_rescaling, invert_batchnorm_pooling, fold_batchnorms, remove_zeropadding2d,
               invert_activation_maxpool, replace_lambda, convert_conv_to_dw_conv, remove_reshape,
               fold_activations_in_add, split_layers_with_activations, split_concat_layers,
               convert_even_to_odd_kernel, replace_activations, insert_identity_convs,
               replace_conv3d)


def sanitize_base(model):
    """ Perform standard sanitizing steps.

    Args:
        model (keras.Model): the input model

    Returns:
        keras.Model: the sanitized model
    """
    # Splits layers with activation into two separate layers
    model = split_layers_with_activations(model)

    # Replace lambda layers
    model = replace_lambda(model)

    # Replaces 3D convolution layers with equivalent 2D convolutions
    # and removes the temporal dimension
    model = replace_conv3d(model)

    # Replace custom activations
    model = replace_activations(model)

    # Replace Conv2D layers that behave as DepthwiseConv2D to the latest.
    model = convert_conv_to_dw_conv(model)

    # Multiple Reshape/Flatten removal transformation
    model = remove_reshape(model)

    # Align Rescaling (if needed)
    model = align_rescaling(model)

    # Invert ReLU <-> MaxPool layers so that MaxPool comes first
    model = invert_activation_maxpool(model)

    # Invert BN <-> Pooling layers and fold BN into their preceding layers
    model = invert_batchnorm_pooling(model)
    model = fold_batchnorms(model)

    # Fold ReLUs with no max_value that comes after an Add layer
    model = fold_activations_in_add(model)

    # Remove unsupported ZeroPadding2D layers and replace them with 'same' padding convolution when
    # possible
    return remove_zeropadding2d(model)


def sanitize_for_hardware(model):
    """ Perform sanitizing steps targetting hardware compatiblity.

    Akida hardware comes with some limitations that can be avoided by smart transformations on the
    model.

    Args:
        model (keras.Model): the input model

    Returns:
        keras.Model: the sanitized model
    """
    # Split Concatenate layers with more than two inputs into multiple Concatenate layers
    # with exactly two inputs when possible
    model = split_concat_layers(model)

    # Convert even kernels to odd for Conv2D et DepthwiseConv2D when possible
    model = convert_even_to_odd_kernel(model)

    # Add identity convolution after some patterns
    model = insert_identity_convs(model)
    return model


def sanitize(model):
    """ Sanitize a model preparing it for quantization.

    This is a wrapping successive calls to several model transformations which aims at making the
    model quantization ready.

    Args:
        model (keras.Model): the input model

    Returns:
        keras.Model: the sanitized model
    """
    return sanitize_for_hardware(sanitize_base(model))
