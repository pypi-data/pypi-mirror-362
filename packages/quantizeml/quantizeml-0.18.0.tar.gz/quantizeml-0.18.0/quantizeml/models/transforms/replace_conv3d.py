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

__all__ = ['replace_conv3d']

import numpy as np
import tensorflow as tf
from copy import deepcopy
from keras import layers
from keras.models import Sequential, Model
from keras.saving import serialize_keras_object

from ...models.utils import apply_weights_to_model
from ...models.transforms.transforms_utils import (get_layers_by_type, get_layer_index,
                                                   update_inbound, get_layers,
                                                   get_inbound_layers_config)
from ...models import reset_buffers
from ...layers import BufferTempConv, DepthwiseBufferTempConv, PleiadesLayer


def _drop_input_first_dim(config):
    """ Drops input first dimension.

    Args:
        config (dict): model config being updated
    """
    input_layers = [layer_config for layer_config in config['layers']
                    if layer_config['class_name'] == 'InputLayer']
    if len(input_layers) != 1:
        raise RuntimeError(f'Detected {len(input_layers)} InputLayer layers while expecting 1.')
    else:
        shape = input_layers[0]['config']['batch_input_shape']
        input_layers[0]['config']['batch_input_shape'] = (shape[0], *shape[2:])


def _update_bn_axis(model, config):
    """ Update BatchNormalization axis.

    BatchNormalization axis set to -1 at layer creation will be saved as the actual positive
    dimension in the configuration (e.g -1 saved to 4). As the temporal dimension is removed, axis
    must be updated.

    Args:
        model (keras.Model): original model
        config (dict): model config being updated
    """
    # Retrieve BatchNormalization layers
    bns = get_layers_by_type(model, layers.BatchNormalization)
    for bn in bns:
        bn_index = get_layer_index(config['layers'], bn.name)
        bn_config = config['layers'][bn_index]
        axis = bn_config['config']['axis']
        if 1 in axis:
            raise ValueError(f"Layer {bn.name} keras.layers.BatchNormalization operates on temporal"
                             " dimension which is not supported.")
        axis = [dim - 1 if dim > 0 else dim for dim in axis]
        bn_config['config']['axis'] = axis


def _ap3_to_gap(model, config):
    """ Replace AveragePooling3D with GlobalAveragePooling2D.

    Args:
        model (keras.Model): original model
        config (dict): model config being updated
    """
    # Retrieve AP3 layer and config
    ap3 = get_layers_by_type(model, layers.AveragePooling3D)
    if len(ap3) == 0:
        return
    elif len(ap3) != 1:
        raise RuntimeError(f'Detected {len(ap3)} AveragePooling3D layers while expecting 1.')
    gap = ap3[0]
    if gap.padding != "valid":
        raise ValueError(f"To convert to GAP, padding should be valid. Receives layer {gap.name}"
                         f" with padding {gap.padding}.")
    elif gap.pool_size[0] != 1:
        raise ValueError(f"To convert to GAP, temporal dimension (pos 0) of the pool size should"
                         f"  be 1. Receives layer {gap.name} with pool_size=={gap.pool_size}.")
    elif gap.pool_size != (1, *gap.input_shape[2:4]):
        raise ValueError("To convert to GAP, pool_size spatial dims should be equal to the input"
                         f" spatial dims. Receives layer {gap.name} with strides=={gap.strides}"
                         f" and pool_size=={gap.pool_size}.")
    elif gap.pool_size != gap.strides:
        raise ValueError("To convert to GAP, strides should equal pool_size. Receives layer "
                         f"{gap.name} with strides=={gap.strides} and pool_size=={gap.pool_size}.")
    ap3_index = get_layer_index(config['layers'], gap.name)
    ap3_config = config['layers'][ap3_index]

    # Drop parameters that are not required
    for param in ['pool_size', 'padding', 'strides']:
        ap3_config['config'].pop(param)

    # Update layer type
    new_config = layers.GlobalAveragePooling2D.from_config(ap3_config['config'])
    ap3_config.update(serialize_keras_object(new_config))


def _verify_reshape(model, config):
    """Verify Reshape layers do not depend on the temporal dimension.

    Args:
        model (keras.Model): original model
        config (dict): model config being updated
    """
    reshape_layers = get_layers_by_type(model, layers.Reshape)
    for layer in reshape_layers:
        if layer.input_shape[1] != layer.output_shape[1]:
            raise ValueError(f"Layer {layer.name} keras.layers.Reshape operates on temporal "
                             "dimension which is not supported.")
        index = get_layer_index(config['layers'], layer.name)
        layer_config = config['layers'][index]
        layer_config['config']['batch_input_shape'] = (
            None, *layer_config['config']['batch_input_shape'][2:])
        layer_config['config']['target_shape'] = layer_config['config']['target_shape'][1:]


def _update_permute(model, config):
    """Verify Permute layers do not permute the temporal dimension with another dimension and
    updates them to account for removed temporal dimension.

    Args:
        model (keras.Model): original model
        config (dict): model config being updated
    """
    permute_layers = get_layers_by_type(model, layers.Permute)
    for layer in permute_layers:
        index = get_layer_index(config['layers'], layer.name)
        layer_config = config['layers'][index]
        dims = layer_config['config']['dims']
        if dims[0] != 1:
            raise ValueError(f"Layer {layer.name} keras.layers.Permute operates on temporal "
                             "dimension which is not supported.")
        dims = tuple(dim - 1 for dim in dims[1:])
        layer_config['config']['dims'] = dims


def _remove_temporal_dimension(model, config):
    """Removes the temporal dimension from a Keras model configuration.

    It performs the following transformations:
      - Drops the temporal axis from the input shape
      - Updates BatchNormalization axis values accordingly
      - Replaces AveragePooling3D with GlobalAveragePooling2D (if applicable)
      - Verifies Reshape layers do not depend on temporal dimensions
      - Adjusts Permute layers to account for removed dimensions

    Args:
        model (keras.Model): The original Keras model instance.
        config (dict): The serialized model config to be updated.
    """
    # Check that Reshape layers are compatible with temporal dimension removal
    _verify_reshape(model, config)

    # Update Permute layers to prepare for temporal dimension removal
    _update_permute(model, config)

    # Drop input shape first dimension, data will be streamed to the model
    _drop_input_first_dim(config)

    # Update BatchNormalization axis
    _update_bn_axis(model, config)

    # Replace AveragePooling3D with GlobalAveragePooling2D
    _ap3_to_gap(model, config)


def _replace_pleiades(model, config):
    """Replace Pleiades layers in a given model with Conv3D layers.

    Args:
        model (keras.Model): The original Keras model instance.
        config (dict): The serialized model config to be updated.

    Returns:
        keras.Model: A new model with Pleiades layers replaced by Conv3D layers or the
        original model if no PleiadesLayer are found.

    """
    pleiades_layers = get_layers_by_type(model, PleiadesLayer)
    if len(pleiades_layers) == 0:
        return model

    weights = {var.name: var for var in model.variables}

    for layer in pleiades_layers:
        index = get_layer_index(config['layers'], layer.name)
        conv_config = config['layers'][index]

        # Compute the transformed weight using the Pleiades transformation matrix
        new_weight = tf.tensordot(layer.kernel, layer.transform, axes=[[4], [0]])
        new_weight = tf.transpose(new_weight, perm=[4, 2, 3, 0, 1])
        # Replace the original layer weights with the transformed weights
        weights[layer.kernel.name] = new_weight

        # Create a new Conv3D layer from the updated configuration
        conv_config['config']['kernel_size'] = tuple(new_weight.shape[:3])
        # Remove unused Pleiades-specific parameters
        for param in ['degrees', 'alpha', 'beta']:
            conv_config['config'].pop(param)
        new_config = layers.Conv3D.from_config(conv_config['config'])
        conv_config.update(serialize_keras_object(new_config))

    new_model = model.from_config(config)

    apply_weights_to_model(new_model, weights)

    return new_model


def _remove_zeropad3d_actregul(model, config):
    """ Remove ZeroPadding3D and ActivityRegularization layers.

    Args:
        model (keras.Model): original model
        config (dict): model config being updated
    """
    model_layers = config['layers']
    new_output_name = None

    # Retrieve ZeroPadding3D and ActivityRegularization layers.
    removables = get_layers_by_type(model, (layers.ZeroPadding3D, layers.ActivityRegularization))
    if len(removables) == 0:
        return

    # For Sequential models, the changes stop here: the ZeroPad3D and ActivityRegularization
    # layers will simply be removed in the following step.
    # For other models, the layers inbounds/outbounds must be rebuilt.
    if not isinstance(model, Sequential):
        for layer in removables:
            # Retrieve the layer's inbound_nodes. (Assuming it has only one inbound layer).
            zp_index = get_layer_index(model_layers, layer.name)
            # tfmot code: 'inbound_nodes' is a nested list where first element is the inbound
            # layername, e.g: [[['conv1', 0, 0, {} ]]]
            updated_inbound = model_layers[zp_index]['inbound_nodes'][0][0][0]

            # Get the outbounds layers
            zp_outbound_names = [outbound.layer.name for outbound in layer.outbound_nodes]
            outbound_ids = [get_layer_index(model_layers, zp_outbound)
                            for zp_outbound in zp_outbound_names]

            # Update the outbounds layers inputs: their current inbound is the current
            # layer that will be removed. So in order to not break the graph connexions,
            # their initial inbound must be replaced with the layer's
            # inbound. This will results in: inbound > layer > outbounds
            # becomes inbound > outbounds.
            if len(outbound_ids) == 0:
                new_output_name = layer.inbound_nodes[0].inbound_layers.name
                last_layer = layer.name

            for id in outbound_ids:
                update_inbound(model_layers[id], layer.name, updated_inbound)

    # Remove the removable layers from the config now
    layers_to_remove = get_layers(config, [zp.name for zp in removables])
    for l_zp in layers_to_remove:
        model_layers.remove(l_zp)

    # Update the model outputs if needed
    if new_output_name:
        for index, out_layer in enumerate(config['output_layers']):
            if out_layer[0] == last_layer:
                config['output_layers'][index][0] = new_output_name


def _check_causal_padding(layer, config):
    inbound_layer = get_inbound_layers_config(layer, model_config=config)
    return len(inbound_layer) == 1 and inbound_layer[0]['class_name'] == 'ZeroPadding3D' and \
        inbound_layer[0]['config']['padding'] == (
            (layer['config']['kernel_size'][0] - 1, 0), (0, 0), (0, 0))


def _squeeze_conv3D_layers(model, config):
    """ Replace Conv3D layers with the appropriate BufferTempConv or Conv2D layer

    Args:
        model (keras.Model): original model
        config (dict): model config being updated
    """
    # Retrieve Conv3D layers
    conv3ds = get_layers_by_type(model, layers.Conv3D)

    for conv3d in conv3ds:
        new_config = None
        conv_index = get_layer_index(config['layers'], conv3d.name)
        conv_config = config['layers'][conv_index]

        # Retrieve convolution parameters that will require an update
        kernel_size = conv_config['config']['kernel_size']
        strides = conv_config['config']['strides']
        dilation_rate = conv_config['config']['dilation_rate']

        # Spatial Conv3D are replaced with Conv2D, those are convolution where first kernel
        # dimension is 1.
        if kernel_size[0] == 1:
            # Set useful param alias
            conv_input_channel = conv3d.input_shape[-1]
            conv_groups = conv_config['config']['groups']
            conv_filters = conv_config['config']['filters']
            # Set common params between depth and full conv layers
            conv_config['config']['kernel_size'] = kernel_size[1:]
            conv_config['config']['strides'] = strides[1:]
            conv_config['config']['dilation_rate'] = dilation_rate[1:]
            # If in_channel==groups==filters the layer behaves as a DepthwiseConv2D
            if conv_input_channel == conv_groups and conv_groups == conv_filters:
                for param in ['kernel_regularizer', 'kernel_initializer', 'kernel_constraint']:
                    conv_config['config'][param.replace(
                        'kernel', 'depthwise')] = conv_config['config'].pop(param)
                for param in ['filters', "groups"]:
                    conv_config['config'].pop(param)
                new_config = layers.DepthwiseConv2D.from_config(conv_config['config'])
            # We do support Conv layer with groups==1 only
            elif conv_groups == 1:
                new_config = layers.Conv2D.from_config(conv_config['config'])
            else:
                raise RuntimeError("Conv2D layers with groups!=1 for quantization are not "
                                   f"supported. Receives the layer {conv3d.name} with "
                                   f"groups={conv_groups}.")
        elif (strides == dilation_rate == (1, 1, 1) and kernel_size[1:] == (1, 1) and
              _check_causal_padding(conv_config, config)):
            # When first kernel dimension is not 1, the convolution is a temporal one and is thus
            # converted to a BufferTempConv
            conv_config['config']['trainable'] = False
            conv_config['config']['kernel_size'] = kernel_size[0]

            if conv_config['config']['groups'] == 1:
                target_class = BufferTempConv
            else:
                conv_config['config'].pop('filters')
                target_class = DepthwiseBufferTempConv

            # Drop parameters that are not required
            for param in ['padding', 'strides', 'kernel_initializer', 'bias_initializer',
                          'kernel_regularizer', 'bias_regularizer', 'activity_regularizer',
                          'kernel_constraint', 'bias_constraint', 'activation', 'groups',
                          'dilation_rate', 'data_format']:
                conv_config['config'].pop(param)

            new_config = target_class.from_config(conv_config['config'])

        else:
            raise RuntimeError(f"Layer '{conv_config['config']['name']}' could not be replaced. "
                               "The model cannot be sanitized or quantized.")

        if new_config is not None:
            conv_config.update(serialize_keras_object(new_config))


def _set_weights(weights, dst_model):
    """ Set the given weights in the bufferized model, adapting Conv3D weights to Conv2D or
    BufferTempConv when required.

    Args:
        weights (np.array): original weights
        keras.Model: bufferized model to set weights into
    """
    for i, w in enumerate(weights):
        # Update Conv3D weights (ndims > 3) to Conv2D or BufferTempConv weights dimensions
        if w.ndim > 3:
            # Spatial kernels: (T=1, H, W, C, F) -> (H, W, C, F)
            if w.shape[0] == 1:
                axis = 0
                if w.shape[3] == 1:
                    # Depthwise spatial kernels: ((T=1, H, W, C=1, F)) -> (H, W, F, 1)
                    w = np.transpose(w, axes=[0, 1, 2, 4, 3])
                w = np.squeeze(w, axis=axis)
            elif w.shape[3] == 1:
                # Depthwise temporal kernels: (T, H=1, W=1, C=1, F) -> (T, F)
                axis = (1, 2, 3)
                w = np.squeeze(w, axis=axis)
            else:
                # Transpose standard kernels: (T, H, W, C, F) -> (H, W, T, C, F)
                w = np.transpose(w, axes=[1, 2, 0, 3, 4])
                # merge axis 2 and 3: (H, W, T, C, F) -> (H=1, W=1, T * C, F)
                w = np.reshape(w, (*w.shape[:2], -1, w.shape[-1]))
            weights[i] = w
    dst_model.set_weights(weights)


def replace_conv3d(model):
    """ Converts the given spatiotemporal Conv3D based model to its bufferized version.

    Args:
        model (keras.Model): the source model

    Returns:
        keras.Model: bufferized model
    """
    assert isinstance(model, (Model, Sequential))

    if len(model.input_shape) != 5:
        return model

    unsupported_layers = [layers.Add, layers.Subtract, layers.Concatenate]
    if any(len(get_layers_by_type(model, layer)) != 0 for layer in unsupported_layers):
        raise RuntimeError(f"Unsupported layers found. {unsupported_layers} are not "
                           "supported for 5-dimensional models.")

    # Copy configuration before applying modifications
    config = deepcopy(model.get_config())

    # Replace the Pleiades layers with Conv3D layers with the appropriate kernel
    model = _replace_pleiades(model, config)

    # Replace Conv3D layers with the appropriate BufferTempConv or Conv2D layer
    _squeeze_conv3D_layers(model, config)

    # Remove the temporal dimension from the model config
    _remove_temporal_dimension(model, config)

    # Remove ZeroPadding3D and ActivityRegularization layers
    _remove_zeropad3d_actregul(model, config)

    # Since layers were replaced, the built shapes are dropped to allow for a clean rebuild
    for layer_config in config["layers"]:
        layer_config.pop('build_config', None)

    # Reconstruct model from the config
    buffer_model = model.from_config(config)

    # Restore model weights
    _set_weights(model.get_weights(), buffer_model)

    # Reset the model
    reset_buffers(buffer_model)

    return buffer_model
