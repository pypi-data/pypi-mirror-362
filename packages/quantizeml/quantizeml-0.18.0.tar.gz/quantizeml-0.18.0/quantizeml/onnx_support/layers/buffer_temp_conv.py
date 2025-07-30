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

__all__ = ["VariableRegistry", "FifoOp", "btc_function", "dwbtc_function",
           "QuantizedBufferTempConv", "QuantizedDepthwiseBufferTempConv",
           "get_qbtc", "get_qdbtc", "reset_buffers"]

import onnx
import numpy as np

from onnxruntime_extensions import onnx_op, PyCustomOpDef
from onnx import AttributeProto as AP, TensorProto as TP, NodeProto
from onnx.helper import make_node

from .base_layer import BRN_OPSET, ONNX_OPSET as op, OnnxLayer, register_node_format
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .set_weights import set_weights_on_qnode, set_range_max_on_qnode
from ..graph_tools import TENSOR_SHAPE, get_field, get_activation
from .compute_shapes import compute_onnx_btc_output
from ..quantization.core import quantize_to_qfloat, aligned_quantize, align_to, downscale
from ..quantization.model import ONNXModel
from .register import register_new_subgraph


class VariableRegistry():
    """A registry for storing and managing variables globally.

    It is used to store the fifo of BufferTempConv nodes.
    """
    variables = {}

    @staticmethod
    def get_variable(model_id, variable_id, default_value):
        models_vars = VariableRegistry.variables.get(model_id, {})
        return models_vars.get(variable_id, default_value)

    @staticmethod
    def set_variable(model_id, variable_id, value):
        if model_id not in VariableRegistry.variables:
            VariableRegistry.variables[model_id] = {}
        VariableRegistry.variables[model_id][variable_id] = value
        return value

    @staticmethod
    def clear(model_ids=None):
        """ Clear model ids from the registry.

        If ids are provided, only those models will be removed.

        Args:
            model_ids (list, optional): list of strings ids to clear. Defaults to None.
        """
        if model_ids is not None:
            for id in model_ids:
                VariableRegistry.variables.pop(id, None)
        else:
            VariableRegistry.variables.clear()


@onnx_op(op_type=f"{BRN_OPSET.domain}::FifoOp", inputs=[PyCustomOpDef.dt_float],
         attrs={"model_id": PyCustomOpDef.dt_string, "variable_id": PyCustomOpDef.dt_string,
                "fifo_size": PyCustomOpDef.dt_int64})
def FifoOp(x, model_id, variable_id, fifo_size):
    # The FifoOp operates on (B, C, H, W) tensors and uses the VariableRegistry to retrieve
    # buffers and storing them after a roll operation.
    if x.ndim != 4:
        raise RuntimeError("FifoOp only supports 4D tensors (B, C, H, W)")

    default_fifo = np.zeros((*x.shape[:2], fifo_size, *x.shape[2:]), dtype=x.dtype)
    fifo = VariableRegistry.get_variable(model_id, variable_id, default_fifo)

    # Check dimensions match with existing fifo
    if fifo.shape[:2] != x.shape[:2] or fifo.shape[3:] != x.shape[2:]:
        raise RuntimeError(f"Input dimensions {x.shape} do not match fifo dimensions {fifo.shape}")

    fifo = np.concatenate((fifo[:, :, 1:, :, :], np.expand_dims(x, 2)), axis=2)
    return VariableRegistry.set_variable(model_id, variable_id, fifo)


# The BufferTempConv operation is made of a FifoOp and a convolution:
#  - Reshape FIFO to perform a 2-D convolution: (B, C, T, H, W) -> (B, C * T, H, W)
#  - Perform convolution: (B, C * T, H, W) * (F, C * T, 1, 1) -> (B, F, H, W)
btc_function = onnx.parser.parse_function("""
    <opset_import: ["": {onnx_opset}, "{domain}": 1], domain:"{domain}">
    BufferTempConv <model_id: string, fifo_name: string, fifo_size: int>(X, W, B) => (Y)
     {{
        fifo = {domain}.FifoOp<model_id: string=@model_id, variable_id: string=@fifo_name,
                                          fifo_size: int=@fifo_size>(X)
        fifo_f32 = Cast<to=1>(fifo)
        fifo_transposed = Transpose<perm=[0, 3, 4, 1, 2]>(fifo_f32)
        target_shape = Constant<value_ints=[0, 0, 0, -1]>()
        fifo_reshaped = Reshape(fifo_transposed, target_shape)
        fifo_transposed_back = Transpose<perm=[0, 3, 1, 2]>(fifo_reshaped)
        Y = Conv(fifo_transposed_back, W, B)
     }}
    """.format(onnx_opset=op.version, domain=BRN_OPSET.domain))
onnx.checker.check_function(btc_function)


# The DepthwiseBufferTempConv operation is made of a FifoOp and a multiplication:
#   - Retrieve the FIFO
#   - Element-wise multiplication: (B, C, T, H, W) * (C, T, H=1, W=1) -> (B, C, T, H, W)
#   - Reduction sum along T dim: (B, C, T, H, W) -> (B, C, H, W)
dwbtc_function = onnx.parser.parse_function("""
    <opset_import: ["": {onnx_opset}, "{domain}": 1], domain:"{domain}">
    DepthwiseBufferTempConv <model_id: string, fifo_name: string, fifo_size: int>(X, W, B) => (Y)
     {{
        fifo = {domain}.FifoOp<model_id: string=@model_id, variable_id: string=@fifo_name,
                                            fifo_size: int=@fifo_size>(X)
        fifo_f32 = Cast<to=1>(fifo)
        Y1 = Mul(fifo_f32, W)
        axis = Constant<value_ints=[2]>()
        Y2 = ReduceSum<keepdims=0>(Y1, axis)
        Y = Add(Y2, B)
     }}
    """.format(onnx_opset=op.version, domain=BRN_OPSET.domain))
onnx.checker.check_function(dwbtc_function)


def reset_buffers(model):
    """ Resets all FIFO-buffer of (Depthwise)BufferTempConv layers within the model.

    Args:
        model (ModelProto or ONNXModel): the model to reset
    """
    if isinstance(model, onnx.ModelProto):
        model = ONNXModel(model)

    model_ids = set()
    for node in model.nodes():
        if any(x in node.op_type for x in ("BufferTempConv", "FifoOp")):
            model_id = onnx.helper.get_node_attr_value(node, "model_id").decode('utf-8')
            model_ids.add(model_id)
    VariableRegistry.clear(model_ids)


@register_node_format(requires_downscale=True)
class QuantizedBufferTempConv(OnnxLayer):
    """Intermediate representation of the BufferTempConv layer.

    Args:
        fifo_name (str): name of the FIFO buffer.
        fifo_size (int): length of the FIFO buffer.
        model_id (str) : name id of the model the layer belongs to.
        activation (str, optional): activation type to be applied. Defaults to "".
        name (str, optional): the node name. Defaults to ''.
    """
    def __init__(self,
                 fifo_name,
                 fifo_size,
                 model_id,
                 activation="",
                 name=''):
        super().__init__("QuantizedBufferTempConv",
                         fifo_name=fifo_name,
                         fifo_size=fifo_size,
                         model_id=model_id,
                         name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["activation"] = activation
        self.serialize_attr["scale"] = True

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")
        self._add_weight("range_max", 1.0)
        self._add_weight("act_range_max", 1.0)

    def __build__(self, input_ts, downscale=True):
        assert input_ts.dtype == np.int8
        assert downscale, f"{self.name} ({self.base_name}) does not support 32-bit output"

        # The chain of operations is modified if downscale is needed
        self.serialize_attr["scale"] = downscale

        # Compute output shape
        conv_output_shape = compute_onnx_btc_output(self, input_ts.shape)
        output_ts = TENSOR_SHAPE(conv_output_shape, np.dtype("int8"))
        return output_ts

    def __quantize__(self, qinput, force_fp=False):
        i_scale = qinput.weights["scale"]

        # Perform cross-layer equalization, i.e.: rescale weights with input scale.
        # To do that first reshape i_scale to put it into axis = 1 and be capable of broadcasting.
        assert i_scale.ndim <= 1
        kernel = self.weights["kernel"]
        if i_scale.size > 1:
            kernel = kernel / align_to(
                np.repeat(i_scale, kernel.shape[1] // i_scale.shape[0]), kernel.ndim, axis=1)
        else:
            kernel = kernel / align_to(np.repeat(i_scale, kernel.shape[1]), kernel.ndim, axis=1)
        # Quantize and set weights
        qweights, i_scale = quantize_to_qfloat(kernel)
        qweights = qweights.astype("int8")

        # Prepare tensors list with unique names
        conv_name = self.name
        prefix = conv_name + "_"
        weights_dict = {}
        weights_dict[prefix + "Wi"] = qweights
        bias = self.weights["bias"]
        if "Biased" in self.op_type:
            qbias = aligned_quantize(bias, i_scale)
            weights_dict[prefix + "B"] = qbias

        # Now consider calibrated output range
        range_max = self.weights["range_max"]
        scale, s_out, ocalib_scale = downscale(range_max, i_scale, force_fp=force_fp)
        weights_dict.update({prefix + "M": align_to(scale.astype("uint8"), qweights.ndim),
                             prefix + "S_out": align_to(s_out, qweights.ndim)})

        # Return quantized weights and ouput scale
        return weights_dict, ocalib_scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", ""]
        if "Biased" in op_type:
            t_names[-1] = "bias"

        nodes, t_names = cast_tensors_to(t_names)

        nodes.append(make_node("BufferTempConv", inputs=t_names, outputs=["Yi"],
                               domain=BRN_OPSET.domain))

        nodes[-1].attribute.append(AP(name="fifo_name", ref_attr_name="fifo_name", type=AP.STRING))
        nodes[-1].attribute.append(AP(name="fifo_size", ref_attr_name="fifo_size", type=AP.INTS))
        nodes[-1].attribute.append(AP(name="model_id", ref_attr_name="model_id", type=AP.STRING))

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Scale out (with saturation) in float domain
        nodes += get_scale_out_ops("Yi", "Yscaled")
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes

    def make_node(self, inputs, outputs):
        node = super().make_node(inputs, outputs, use_custom_op=True)
        register_new_subgraph(btc_function)
        return node


def get_qbtc(nodes, graph, tensor_ranges):
    btc_node = nodes[0]
    assert btc_node.op_type == 'BufferTempConv'
    fifo_name = get_field(btc_node, "fifo_name")
    fifo_size = get_field(btc_node, "fifo_size")
    model_id = get_field(btc_node, "model_id") + "_quantized"

    act_node = get_activation(nodes) or NodeProto()
    activation = act_node.op_type
    qconv = QuantizedBufferTempConv(fifo_name=fifo_name,
                                    fifo_size=fifo_size,
                                    model_id=model_id,
                                    activation=activation)

    set_weights_on_qnode(qconv, btc_node, graph)
    # Set calibration ranges
    set_range_max_on_qnode(qconv, tensor_ranges[nodes[-1].output[0]])
    if act_node.op_type == "activation":
        act_range_max = tensor_ranges[act_node.input[0]]
        set_range_max_on_qnode(qconv, act_range_max, name="act_range_max", reduce=True)
    return qconv


@register_node_format(requires_downscale=True)
class QuantizedDepthwiseBufferTempConv(OnnxLayer):
    """Intermediate representation of the DepthwiseBufferTempConv layer.

    Args:
        fifo_name (str): name of the FIFO buffer.
        fifo_size (int): length of the FIFO buffer.
        model_id (str) : name id of the model the layer belongs to.
        activation (str, optional): activation type to be applied. Defaults to "".
        name (str, optional): the node name. Defaults to ''.
    """
    def __init__(self,
                 fifo_name,
                 fifo_size,
                 model_id,
                 activation="",
                 name=''):
        super().__init__("QuantizedDepthwiseBufferTempConv",
                         fifo_name=fifo_name,
                         fifo_size=fifo_size,
                         model_id=model_id,
                         name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["activation"] = activation
        self.serialize_attr["scale"] = True

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")
        self._add_weight("range_max", 1.0)
        self._add_weight("act_range_max", 1.0)

    def __build__(self, input_ts, downscale=True):
        assert input_ts.dtype == np.int8
        assert downscale, f"{self.name} ({self.base_name}) does not support 32-bit output"
        assert self.weights["kernel"].ndim == 4

        if self.weights["bias"].size == 0:
            self.set_weight(
                "bias", np.zeros(shape=(self.weights["kernel"].shape[0], 1, 1), dtype=np.float32))

        self.serialize_attr["scale"] = downscale

        # Compute output shape
        conv_output_shape = compute_onnx_btc_output(self, input_ts.shape)
        output_ts = TENSOR_SHAPE(conv_output_shape, np.dtype("int8"))
        return output_ts

    def __quantize__(self, qinput, force_fp=False):
        i_scale = qinput.weights["scale"]

        # Perform cross-layer equalization, i.e.: rescale weights with input scale.
        # To do that first reshape i_scale to put it into axis = 1 and be capable of broadcasting.
        assert i_scale.ndim <= 1
        kernel = self.weights["kernel"]
        kernel = kernel / align_to(i_scale, kernel.ndim, axis=0)
        # Quantize and set weights
        qweights, i_scale = quantize_to_qfloat(kernel)
        qweights = qweights.astype("int8")

        # Prepare tensors list with unique names
        conv_name = self.name
        prefix = conv_name + "_"
        weights_dict = {}
        weights_dict[prefix + "Wi"] = qweights
        bias = self.weights["bias"]
        qbias = aligned_quantize(bias, align_to(i_scale, ndims=bias.ndim, axis=0))
        weights_dict[prefix + "B"] = qbias

        # Now consider calibrated output range
        range_max = self.weights["range_max"]
        scale, s_out, ocalib_scale = downscale(range_max, i_scale, force_fp=force_fp)
        weights_dict.update({prefix + "M": align_to(scale.astype("uint8"), qweights.ndim),
                             prefix + "S_out": align_to(s_out, qweights.ndim)})

        # Return quantized weights and ouput scale
        return weights_dict, ocalib_scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", "bias"]

        nodes, t_names = cast_tensors_to(t_names)

        nodes.append(make_node("DepthwiseBufferTempConv", inputs=t_names, outputs=["Yi"],
                               domain=BRN_OPSET.domain))

        nodes[-1].attribute.append(AP(name="fifo_name", ref_attr_name="fifo_name", type=AP.STRING))
        nodes[-1].attribute.append(AP(name="fifo_size", ref_attr_name="fifo_size", type=AP.INTS))
        nodes[-1].attribute.append(AP(name="model_id", ref_attr_name="model_id", type=AP.STRING))

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Scale out (with saturation) in float domain
        nodes += get_scale_out_ops("Yi", "Yscaled")
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes

    def make_node(self, inputs, outputs):
        node = super().make_node(inputs, outputs, use_custom_op=True)
        register_new_subgraph(dwbtc_function)
        return node


def get_qdbtc(nodes, graph, tensor_ranges):
    btc_node = nodes[0]
    assert btc_node.op_type == 'DepthwiseBufferTempConv'
    fifo_name = get_field(btc_node, "fifo_name")
    fifo_size = get_field(btc_node, "fifo_size")
    model_id = get_field(btc_node, "model_id") + "_quantized"

    act_node = get_activation(nodes) or NodeProto()
    activation = act_node.op_type

    qconv = QuantizedDepthwiseBufferTempConv(fifo_name=fifo_name,
                                             fifo_size=fifo_size,
                                             model_id=model_id,
                                             activation=activation)
    # Sets the weights to configure the operation chain
    set_weights_on_qnode(qconv, btc_node, graph)
    # Set calibration ranges
    set_range_max_on_qnode(qconv, tensor_ranges[nodes[-1].output[0]])
    if act_node.op_type == "activation":
        act_range_max = tensor_ranges[act_node.input[0]]
        set_range_max_on_qnode(qconv, act_range_max, name="act_range_max", reduce=True)
    return qconv
