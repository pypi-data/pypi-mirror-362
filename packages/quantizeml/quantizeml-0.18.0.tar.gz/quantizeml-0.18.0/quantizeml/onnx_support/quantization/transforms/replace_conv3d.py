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

__all__ = ["replace_conv3d"]

import onnx
import numpy as np
from onnxscript.rewriter import rewrite, pattern, ir
from hashlib import sha256

from ..model import ONNXModel
from ...layers import BRN_OPSET, ONNX_OPSET, btc_function, dwbtc_function
from ...graph_tools import get_field


def find_convs(op, x, w):
    return op.Conv(x, w, _allow_other_inputs=True, _outputs=["conv"])


def squeeze_to_conv2d(op, x, w, conv, **__):
    # Remove the temporal dimension of the kernel
    ir_node = conv.producer()
    new_w = ir.tensor(np.squeeze(w.const_value.numpy(), axis=2))
    # Modify attributes when required
    conv_attrs = ir_node.attributes
    if pads := conv_attrs.get("pads", None):
        pads.value = (*pads.value[1:3], *pads.value[4:])
    if strides := conv_attrs.get("strides", None):
        strides.value = strides.value[1:]
    if dilations := conv_attrs.get("dilations", None):
        dilations.value = dilations.value[1:]
    return op.Conv(x, op.initializer(new_w, name=w.name), *ir_node.inputs[2:], **conv_attrs)


def is_spatial_conv(*_, w, **__):
    # Weights are [C_out, C_in, T, H, W] and a 3D convolution is a 2D spatial convolution when T=1
    return len(w.shape) == 5 and w.shape[2] == 1


def squeeze_to_gemm(op, x, w, conv, **__):
    # Remove the temporal dimension of the kernel
    ir_node = conv.producer()
    new_w = ir.tensor(np.squeeze(w.const_value.numpy(), axis=2))
    return op.Gemm(x, op.initializer(new_w, name=w.name), *ir_node.inputs[2:], transB=1)


def is_conv1d(*_, w, conv, **__):
    pads = conv.producer().attributes.get('pads', ir.AttrInt64s('pads', [0, 0]))
    strides = conv.producer().attributes.get('strides', ir.AttrInt64s('strides', [1]))
    dilations = conv.producer().attributes.get('dilations', ir.AttrInt64s('dilations', [1]))
    group = conv.producer().attributes.get('group', ir.AttrInt64('group', 1))
    return len(w.shape) == 3 and w.shape[2] == 1 and pads.value == [0, 0] and \
        strides.value == dilations.value == [1] and group.value == 1


def is_temporal_conv(w, strides, dilations):
    # Weights are [C_out, C_in, T, H, W] and a 3D convolution is a 1D temporal convolution when:
    # T!=1, H=W=1 and groups is either 1 (standard) or the input channels (depthwise)
    return (strides.value == dilations.value == [1, 1, 1] and len(w.shape) == 5
            and w.shape[2] != 1 and w.shape[-2:] == (1, 1))


def is_causal_pad(w, pads):
    # FIFO compatible causal padding is when padding equal kernel dimension - 1 on dimension T (that
    # is first padding on 3rd dimension)
    if len(w.shape) < 3:
        return False
    expected_pads = [0] * (len(w.shape) + 1)
    expected_pads[0] = w.shape[2] - 1
    return pads == expected_pads


def is_standard_temporal_conv(*_, w, conv, **__):
    pads = conv.producer().attributes.get('pads', ir.AttrInt64s('pads', [0, 0, 0, 0, 0, 0]))
    strides = conv.producer().attributes.get('strides', ir.AttrInt64s('strides', [1, 1, 1]))
    dilations = conv.producer().attributes.get('dilations', ir.AttrInt64s('dilations', [1, 1, 1]))
    group = conv.producer().attributes.get('group', ir.AttrInt64('group', 1))
    return is_causal_pad(w, pads.value) and is_temporal_conv(w, strides, dilations) and \
        group.value == 1


def is_depthwise_temporal_conv(*_, w, conv, **__):
    pads = conv.producer().attributes.get('pads', ir.AttrInt64s('pads', [0, 0, 0, 0, 0, 0]))
    strides = conv.producer().attributes.get('strides', ir.AttrInt64s('strides', [1, 1, 1]))
    dilations = conv.producer().attributes.get('dilations', ir.AttrInt64s('dilations', [1, 1, 1]))
    group = conv.producer().attributes.get('group', ir.AttrInt64('group', 1))
    return is_causal_pad(w, pads.value) and is_temporal_conv(w, strides, dilations) and \
        group.value == w.shape[0] and w.shape[1] == 1


def to_standard_buffer_temp_conv(op, x, w, conv, **__):
    ir_node = conv.producer()
    # Merge T and C dims in standard kernels: (F, C, T, H=1, W=1) -> (F, C * T, H=1, W=1)
    F, C, T, H, W = w.shape
    kernel = ir.tensor(np.reshape(w.const_value.numpy(), (F, C * T, H, W)))
    # 'model_id' is a global variable defined in replace_conv3d
    return op.BufferTempConv(x, op.initializer(kernel, name=w.name), *ir_node.inputs[2:],
                             fifo_name=f'{x.name}_fifo', fifo_size=T,
                             model_id=model_id, _domain=BRN_OPSET.domain)


def to_depthwise_buffer_temp_conv(op, x, w, conv, **__):
    ir_node = conv.producer()
    kernel = ir.tensor(np.squeeze(w.const_value.numpy(), axis=1))
    if len(ir_node.inputs) > 2:
        # Extend bias dims for manual addition (C) -> (C, 1, 1)
        bias = ir.tensor(ir_node.inputs[2].const_value.numpy()[..., None, None])
        bias = op.initializer(bias, name=ir_node.inputs[2].name)
    else:
        bias = ir.tensor(np.zeros((w.shape[0], 1, 1), dtype=np.float32))
        bias = op.initializer(bias, name=ir_node.outputs[0].name + "/bias")
    # 'model_id' is a global variable defined in replace_conv3d
    return op.DepthwiseBufferTempConv(x, op.initializer(kernel, name=w.name), bias,
                                      fifo_name=f'{x.name}_fifo', fifo_size=w.shape[2],
                                      model_id=model_id, _domain=BRN_OPSET.domain)


def remove_temporal_dimension(model):
    # Store a copy of the graph that will be used to get intermediates shapes. This cannot be done
    # on the original model because shape are updated along the way
    ir_model = ir.from_proto(model.model).graph
    for n, node in enumerate(model.nodes()):
        # Get the shapes from the original model
        input_shape = next((list(info.shape.dims)
                           for info in ir_model[n].inputs if info.name == node.input[0]))
        output_shape = next((list(info.shape.dims)
                            for info in ir_model[n].outputs if info.name == node.output[0]))

        # Get the model proto to be updated
        input_proto = model.find_value_info_by_name(node.input[0])

        if len(input_shape) == len(output_shape) and len(input_shape) >= 3:
            if node.op_type == 'AveragePool' and get_field(node, "kernel_shape")[0] != 1 or \
               node.op_type == 'GlobalAveragePool' and input_shape[2] != 1 or \
               node.op_type == 'ReduceMean' and 2 in model.get_variable(node.input[1]):
                raise RuntimeError(f"Node {node.name} {node.op_type} operates on temporal "
                                   "dimension which is not supported.")
            input_proto.type.tensor_type.shape.dim.pop(2)
        elif len(input_shape) != len(output_shape):
            if node.op_type in ['Reshape']:
                if input_shape[2] != output_shape[2]:
                    raise RuntimeError(f"Node {node.name} {node.op_type} operates on temporal "
                                       "dimension which is not supported.")
                input_proto.type.tensor_type.shape.dim.pop(2)
            elif node.op_type == 'ReduceMean':
                if 2 in (axes := model.get_variable(node.input[1])):
                    raise RuntimeError(f"Node {node.name} {node.op_type} operates on temporal "
                                       "dimension which is not supported.")
                axes_tp = onnx.numpy_helper.from_array(
                    np.array([dim if dim < 2 else dim - 1 for dim in axes]), node.input[1])
                model.graph().initializer.remove(model.get_initializer(node.input[1]))
                model.graph().initializer.extend([axes_tp])
                input_proto.type.tensor_type.shape.dim.pop(2)
            else:
                raise RuntimeError(f"Node {node.name} {node.op_type} I/O rank is different and is "
                                   "not a supported op_type.")
    del model.output[0].type.tensor_type.shape.dim[2]


def replace_conv3d(model):
    """Replaces 2+1D convolution layers in an ONNX model with equivalent 2D convolutions + custom
    temporal convolutions.

    Args:
        model (ONNXModel): the input model
    """
    assert isinstance(model, ONNXModel)

    # model_id is defined as a global variable to be used in to_standard_buffer_temp_conv
    # and to_depthwise_buffer_temp_conv
    global model_id
    model_id = sha256(model.serialized).hexdigest()

    if len(model.input[0].type.tensor_type.shape.dim) != 5:
        return model

    unsupported_ops = ["Add", "Concat", "Sum"]
    if any(node.op_type in unsupported_ops for node in model.nodes()):
        raise RuntimeError(f"Unsupported operation found. Operations {unsupported_ops} are not "
                           "supported for 5-dimensional models.")

    rules = [
        pattern.RewriteRule(find_convs, squeeze_to_conv2d, is_spatial_conv),
        pattern.RewriteRule(find_convs, squeeze_to_gemm, is_conv1d),
        pattern.RewriteRule(find_convs, to_standard_buffer_temp_conv, is_standard_temporal_conv),
        pattern.RewriteRule(find_convs, to_depthwise_buffer_temp_conv, is_depthwise_temporal_conv)
    ]

    # Apply rewrites
    model.model = rewrite(model.model, pattern_rewrite_rules=rules)
    model.add_function(btc_function)
    model.add_function(dwbtc_function)

    # After rewrite, if any of the remainining conv node still are 3D, then this model cannot be
    # properly sanitized and quantized
    for node in model.nodes():
        if node.op_type == "Conv":
            if len(model.get_variable(node.input[1]).shape) in [3, 5]:
                raise RuntimeError(f"Node '{node.name}' could not be replaced. The model "
                                   "cannot be sanitized or quantized.")

    # Remove the temporal dimension T from (B, C, T, H, W) inputs and outputs
    remove_temporal_dimension(model)

    # Update opset for custom functions
    model.set_opset_import(BRN_OPSET.domain, BRN_OPSET.version)
    model.set_opset_import(ONNX_OPSET.domain, ONNX_OPSET.version)
    model.check_model(infer_shapes=False)
