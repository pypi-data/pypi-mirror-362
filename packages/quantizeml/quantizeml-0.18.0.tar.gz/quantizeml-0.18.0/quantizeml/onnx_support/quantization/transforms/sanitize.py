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
__all__ = ['sanitize']

import os
import tempfile
import onnx
import warnings
from pathlib import Path

from onnxruntime.quantization.shape_inference import quant_pre_process

from .convert_avg_and_rmean_to_gap import convert_avg_and_rmean_to_gap
from .convert_conv_to_gemm import convert_conv_to_gemm
from .convert_even_to_odd_kernel import convert_even_to_odd_kernel
from .convert_matmul_to_gemm import convert_matmul_to_gemm
from .convert_min_max_to_clip import convert_min_max_to_clip
from .convert_resize_to_depthwise_transpose import convert_resize_to_depthwise_transpose
from .fuse_relu_clip_nodes import fuse_relu_clip_nodes
from .fold_batchnorms import fold_batchnorms
from .insert_rescaling import insert_rescaling
from .remove_pad_nodes import fold_pad_into_conv
from .remove_reshape import remove_reshape
from .squeeze_reshape_to_flatten import convert_squeeze_reshape_to_flatten
from .split_concat_and_sum_nodes import split_concat_and_sum_nodes
from .swap_pad_transpose import swap_pad_transpose
from .untranspose_gemm_weights import untranspose_gemm_weights
from .replace_activations import replace_activations
from .invert_activation_maxpool import invert_activation_maxpool
from .unify_pads_format import unify_pads_format
from .remove_pointless_ops import remove_pointless_ops
from .insert_identity_convs import insert_identity_convs
from .replace_conv3d import replace_conv3d
from .clone_shared_inputs import clone_shared_inputs
from ..model import ONNXModel
from ...layers import BRN_OPSET


def sanitize_base(model):
    """ Perform standard sanitizing steps.

    Args:
        model (ONNXModel): the input model
    """
    # Duplicate initializers that are used more than once
    clone_shared_inputs(model)

    # Swaps Pad and Transpose nodes when possible
    swap_pad_transpose(model)

    # Fold pad into conv when possible
    fold_pad_into_conv(model)

    # Replaces 3D convolution layers in an ONNX model with equivalent 2D convolutions
    # and removes the temporal dimension
    replace_conv3d(model)

    # Adds a Rescaling node to the model
    insert_rescaling(model)

    # Converts Resize nodes to DepthwiseConv2DTranpose when possible
    convert_resize_to_depthwise_transpose(model)

    # Unify pads format
    unify_pads_format(model)

    # Retranspose Gemm weights if they are transposed
    untranspose_gemm_weights(model)

    # Fold batchnorm node into previous nodes when possible
    fold_batchnorms(model)

    # Convert Squeeze/Reshape into Flatten when possible
    convert_squeeze_reshape_to_flatten(model)

    # Convert Min/Max into Clip
    convert_min_max_to_clip(model)

    # Convert AveragePool or ReduceMean to GAP when possible
    convert_avg_and_rmean_to_gap(model)

    # Remove pointless reshape nodes
    remove_reshape(model)

    # Convert Matmul to Gemm
    convert_matmul_to_gemm(model)

    # Convert Conv to Gemm when possible
    convert_conv_to_gemm(model)

    # Fuses ReLU/Clip nodes
    fuse_relu_clip_nodes(model)

    # Replace activations
    replace_activations(model)

    # Invert activation and maxpool
    invert_activation_maxpool(model)

    # Remove pointless operations
    remove_pointless_ops(model)


def sanitize_for_hardware(model):
    """ Perform sanitizing steps targetting hardware compatiblity.

    Akida hardware comes with some limitations that can be avoided by smart transformations on the
    model.

    Args:
        model (ONNXModel): the input model
    """
    # Split Concat nodes into multiple Concats with exactly two inputs when possible
    split_concat_and_sum_nodes(model)

    # Convert even to odd kernel for convolutional nodes when possible
    convert_even_to_odd_kernel(model)

    # Add an identity convolution after some patterns
    insert_identity_convs(model)


def sanitize(model):
    """Sanitize a model preparing it for quantization.

    This is a wrapping successive calls to several model transformations
    which aims at making the model quantization ready.

    Args:
        model(ONNXModel): the input model

    Returns:
        ONNXModel: the sanitized model
    """
    assert isinstance(model, ONNXModel)

    # Clone model to prevent modification of the original one
    model = model.clone()

    # Replace operations to match with current ONNX version
    model.update_model_version()

    # Clean inputs/outputs
    model.clean_graph_io()

    # Perform optimization only if model is not quantized
    if not any(node.domain == "com.brainchip" for node in model.nodes()):
        with tempfile.TemporaryDirectory(prefix="pre.quant.") as quant_tmp_dir:
            # To perfom ONNXRuntime optimization, we would like to use
            # onnxruntime.quantization.quant_pre_process, to optimize the model (when required)
            # and infer the intermediate shapes.
            # However, it always expects to read the model from a path. That is why we
            # save the input model if it is not a path.
            tmp_model_path = os.path.join(quant_tmp_dir, "model.onnx")
            model.save_model_to_file(tmp_model_path)

            # We employ onnxruntime preprocessing to implement optimization.
            # There are some issue in onnxruntime (e.g. Constant Node) that
            # raise exceptions when computing shapes using symbolic_shape_inference.
            # That is why we bypass the symbolic shape inference and apply first
            # an optimization that folds these constants, and then apply by shape inference.
            try:
                quant_pre_process(tmp_model_path, tmp_model_path, skip_symbolic_shape=True)
                quant_pre_process(tmp_model_path, tmp_model_path)
            except Exception:
                # Skip optimization and/or shape inference if it fails
                warnings.warn("ONNXRuntime optimization failed. "
                              "Skipping optimization and/or shape inference.")

            # Load the model
            model = onnx.load_model(Path(tmp_model_path))

            # If ONNXRuntime optimization fails, shapes will not be inferred.
            # Consequently we use ONNX shape inference module to TRY to ensure that shapes
            # will be inferred.
            model = ONNXModel(onnx.shape_inference.infer_shapes(model, check_type=True))

    sanitize_base(model)
    sanitize_for_hardware(model)

    # ONNXRuntime optimization will mess with BRN_OPSET.version setting it to 1000 which will cause
    # issues when manipulating models (merging during quantization). For that reason, the opset is
    # reset after all optimizations and sanitizing.
    if any(opset.domain == BRN_OPSET.domain for opset in model.opset_import()):
        model.set_opset_import(BRN_OPSET.domain, BRN_OPSET.version)
    return model
