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
__all__ = ["QuantizedConv2DTranspose", "get_qconv_transpose", "QuantizedDepthwise2DTranspose"]

import numpy as np

from onnx import AttributeProto as AP, TensorProto as TP, NodeProto
from onnx.helper import make_node

from .base_layer import OnnxLayer, register_node_format
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops, get_lut_ops
from .compute_shapes import compute_onnx_conv_output
from .layer_compatibility import check_conv_depthwise_compatibility
from .set_weights import set_weights_on_qnode, set_max_value_on_qnode, set_range_max_on_qnode
from ..graph_tools import TENSOR_SHAPE, get_field, get_activation, to_field, check_node_attributes
from ..quantization.core import (quantize_to_qfloat, aligned_quantize, downscale,
                                 align_to, compute_lut_values)


def get_qconv_transpose(nodes, graph, tensor_ranges):
    conv_node = nodes[0]
    assert conv_node.op_type == 'ConvTranspose'

    # Check supported attributes
    valid_attr = {'auto_pad': ['NOTSET'], 'dilations': [[1, 1]]}
    check_node_attributes(conv_node, valid_attr)
    if bool(get_field(conv_node, 'output_padding', False)) or bool(
            get_field(conv_node, 'output_shape', False)):
        raise ValueError("Unsupported attributes output_padding or output_shape")
    act_node = get_activation(nodes) or NodeProto()

    # Retrieve attributes
    strides = get_field(conv_node, 'strides', (1, 1))
    group = get_field(conv_node, "group", 1)
    pads = get_field(conv_node, 'pads', (0, 0, 0, 0))
    activation = get_field(act_node, 'main_op_type', act_node.op_type)
    alpha = get_field(act_node, 'alpha', 0.01)
    if group == 1:
        qconv = QuantizedConv2DTranspose(strides=strides,
                                         pads=pads,
                                         name=conv_node.name,
                                         activation=activation,
                                         alpha=alpha)
    else:
        # need to check supported attributes
        check_conv_depthwise_compatibility(conv_node, graph)
        qconv = QuantizedDepthwise2DTranspose(strides=strides,
                                              pads=pads,
                                              name=conv_node.name,
                                              activation=activation,
                                              alpha=alpha)
    # Sets the weights to configure the operation chain
    set_weights_on_qnode(qconv, conv_node, graph)
    if act_node.op_type == "Clip":
        set_max_value_on_qnode(qconv, act_node, graph)

    # Set calibration ranges
    set_range_max_on_qnode(qconv, tensor_ranges[nodes[-1].output[0]])
    if act_node.op_type == "activation":
        act_range_max = tensor_ranges[act_node.input[0]]
        set_range_max_on_qnode(qconv, act_range_max, name="act_range_max", reduce=True)
    return qconv


@register_node_format(requires_downscale=True)
class QuantizedConv2DTranspose(OnnxLayer):
    """Intermediate representation of the upsampling layer QuantizedConv2DTranspose().

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        activation (str, optional): activation type to be applied. Defaults to "".
        alpha (float, optional): negative slope coefficient used by some activation
            (e.g. LeakyRelu). Defaults to 0.01.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, strides=[1, 1], pads=[0, 0, 0, 0], activation="", alpha=0.01, name=''):
        super().__init__("QuantizedConv2DTranspose",
                         strides=strides,
                         pads=pads,
                         alpha=alpha,
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
        assert downscale, f"{self.name} ({self.base_name}) does not support 32bit output"
        assert self.weights["kernel"].ndim == 4
        # Compute output shape
        conv_output_shape = compute_onnx_conv_output(self, input_ts.shape,
                                                     apply_pool=False, transpose=True)
        output_ts = TENSOR_SHAPE(conv_output_shape, np.dtype("int8"))
        return output_ts

    def __quantize__(self, qinput, force_fp=False):
        i_scale = qinput.weights["scale"]

        # Perform cross-layer equalization, i.e.: rescale weights with input scale.
        # To do that first reshape i_scale to put it into axis = 0 and be capable of broadcasting.
        assert i_scale.ndim <= 1
        kernel = self.weights["kernel"]
        kernel = kernel / align_to(i_scale, kernel.ndim, axis=0)
        # Quantize and set weights over filters (axis=1).
        qweights, i_scale = quantize_to_qfloat(kernel, axis=1)
        qweights = qweights.astype("int8")

        # Prepare tensors list with unique names
        conv_name = self.name
        prefix = conv_name + "_"
        weights_dict = {}
        bias = self.weights["bias"]
        weights_dict[prefix + "Wi"] = qweights
        if "Biased" in self.op_type:
            qbias = aligned_quantize(bias, i_scale)
            weights_dict[prefix + "B"] = qbias

        # Quantize max value when there is an activation
        if "Clipped" in self.op_type:
            qmax_value = aligned_quantize(self.weights["max_value"], i_scale, signed=False)
            weights_dict[prefix + "max_value"] = align_to(qmax_value, qweights.ndim)

        # Quantize an activation via LUT
        if "LUT" in self.op_type:
            # LUT require a scalar power-of-two as input scale.
            # That is why we develop an intermediate downscale
            range_max = self.weights["act_range_max"]
            scale, s_out, i_scale = downscale(range_max, i_scale, bitwidth=11)
            weights_dict.update({prefix + "M_act": align_to(scale.astype("uint8"), qweights.ndim),
                                 prefix + "S_act": align_to(s_out, qweights.ndim)})
            # Compute lut values
            lut_values, i_scale = compute_lut_values(self.serialize_attr["activation"],
                                                     i_scale,
                                                     alpha=get_field(self, "alpha"))
            weights_dict.update({prefix + "LUT": lut_values.astype("int32")})

        # Now consider calibrated output range
        range_max = self.weights["range_max"]
        scale, s_out, ocalib_scale = downscale(range_max, i_scale, force_fp=force_fp)
        weights_dict.update({prefix + "M": align_to(scale.astype("uint8"), qweights.ndim),
                             prefix + "S_out": align_to(s_out, qweights.ndim)})

        # Return quantized weights and output scale
        return weights_dict, ocalib_scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", ""]
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Transpose convolution
        nodes.append(make_node("ConvTranspose", inputs=t_names, outputs=["Yi"]))
        nodes[-1].attribute.extend([AP(name="strides", ref_attr_name="strides", type=AP.INTS),
                                   AP(name="pads", ref_attr_name="pads", type=AP.INTS)])

        # LUT (optional)
        if "LUT" in op_type:
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            # Intermedial downscale
            nodes += get_scale_out_ops(nodes[-1].output[0], "Ys", scale_name="ActScale",
                                       shift_name="ActShift", bitwidth=11)
            # Main operation
            nodes += get_lut_ops("Ys", "Yi")

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


class QuantizedDepthwise2DTranspose(QuantizedConv2DTranspose):
    """ Intermediate representation of the upsampling layer QuantizedDepthwise2DTranspose.

    Inherits from QuantizedConv2DTranspose: only different attribute is group.

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        activation (str, optional): activation type to be applied. Defaults to "".
        alpha (float, optional): negative slope coefficient used by some activation
            (e.g. LeakyRelu). Defaults to 0.01.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, strides=[1, 1], pads=[0, 0, 0, 0], activation="", alpha=0.01, name=''):
        super().__init__(activation=activation, strides=strides, pads=pads, alpha=alpha, name=name)
        self.base_name = "QuantizedDepthwise2DTranspose"

    def __build__(self, input_ts, downscale=True):
        # ConvTranspose weights are (C,F,kH,kW)
        kernel_shape = self.weights["kernel"].shape
        expect_shape = (input_ts.shape[1], 1, *kernel_shape[-2:])
        if expect_shape != kernel_shape:
            raise ValueError("Kernel shape does not match with the following format: "
                             f"(input channels, 1, Kx, Ky). Receives: {kernel_shape} and "
                             f"expected: {expect_shape}")
        # Include group in node as attribute
        self.attribute.append(to_field("groups", expect_shape[0]))
        return super().__build__(input_ts, downscale=downscale)

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", ""]
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Transpose convolution
        nodes.append(make_node("ConvTranspose", inputs=t_names, outputs=["Yi"]))
        nodes[-1].attribute.extend([AP(name="strides", ref_attr_name="strides", type=AP.INTS),
                                    AP(name="group", ref_attr_name="groups", type=AP.INT),
                                    AP(name="pads", ref_attr_name="pads", type=AP.INTS)])

        # LUT (optional)
        if "LUT" in op_type:
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            # Intermedial downscale
            nodes += get_scale_out_ops(nodes[-1].output[0], "Ys", scale_name="ActScale",
                                       shift_name="ActShift", bitwidth=11)
            # Main operation
            nodes += get_lut_ops("Ys", "Yi")

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
