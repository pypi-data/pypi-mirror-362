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
__all__ = ["QuantizedConv2D", "get_qconv"]

import numpy as np

from onnx import AttributeProto as AP, TensorProto as TP, NodeProto
from onnx.helper import make_node

from .base_layer import OnnxLayer, register_node_format
from .subgraph_ops import cast_tensors_to, get_pool_ops, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops, get_lut_ops
from .subgraph_ops.padding import get_padding_ops, transform_pads_into_array
from .compute_shapes import compute_onnx_conv_output
from .set_weights import set_weights_on_qnode, set_max_value_on_qnode, set_range_max_on_qnode
from ..graph_tools import (TENSOR_SHAPE, get_field, get_node, get_activation,
                           get_tensor_shape, check_node_attributes)
from ..quantization.core import (quantize_to_qfloat, aligned_quantize, fold_zero_point, align_to,
                                 downscale, compute_lut_values, dequantize)


def get_qconv(nodes, graph, tensor_ranges):
    conv_node = nodes[0]
    assert conv_node.op_type == 'Conv'

    # Check supported attributes
    valid_attr = {'auto_pad': ['NOTSET'], 'dilations': [[1, 1]], 'group': [1]}
    check_node_attributes(conv_node, valid_attr)

    # Retrieve attributes
    strides = get_field(conv_node, 'strides', (1, 1))
    pool_type = "none"
    pool_size = (2, 2)
    pool_strides = (1, 1)
    pool_node = get_node(nodes, 'MaxPool')
    pool_pads = [0, 0, 0, 0]
    if pool_node:
        pool_type = "max"
        # kernel_shape attribute is mandatory for MaxPool
        pool_size = get_field(pool_node, 'kernel_shape')
        pool_strides = get_field(pool_node, 'strides', pool_strides)
        pool_pads = get_field(pool_node, "pads", pool_pads)
    pool_node = get_node(nodes, 'GlobalAveragePool')
    if pool_node:
        pool_type = "gap"

    act_node = get_activation(nodes) or NodeProto()
    activation = get_field(act_node, 'main_op_type', act_node.op_type)
    alpha = get_field(act_node, 'alpha', 0.01)
    qconv = QuantizedConv2D(strides=strides,
                            pool_type=pool_type,
                            pool_size=pool_size,
                            pool_strides=pool_strides,
                            pool_pads=pool_pads,
                            activation=activation,
                            alpha=alpha,
                            name=conv_node.name)

    # Sets the weights to configure the operation chain
    set_weights_on_qnode(qconv, conv_node, graph)
    pads = get_field(conv_node, 'pads', False)
    if pads:
        qconv.set_weight("pads", transform_pads_into_array(pads))
    if act_node.op_type == "Clip":
        set_max_value_on_qnode(qconv, act_node, graph)

    # Set calibration ranges
    set_range_max_on_qnode(qconv, tensor_ranges[nodes[-1].output[0]])
    if act_node.op_type == "activation":
        act_range_max = tensor_ranges[act_node.input[0]]
        set_range_max_on_qnode(qconv, act_range_max, name="act_range_max", reduce=True)
    return qconv


@register_node_format(requires_downscale=True)
class QuantizedConv2D(OnnxLayer):
    """Intermediate representation of QLinearConv() + MaxPool() + ReLU() as an exportable node.

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        pool_type (str, optional): the pool type, one of {"none", "max", "gap"}. Defaults to "none".
        pool_size (list of int, optional): the kernel pool shape.
            Ignore it when pool_type != "max". Defaults to (2, 2).
        pool_stride (list of int, optional): the kernel strides.
            Ignore it when pool_type != "max". Defaults to (2, 2).
        pool_pads (list of int, optional): the size of each padding dimension.
            Ignore it when pool_type != "max". Defaults to [0, 0, 0, 0].
        input_conv (bool, optional): whether it is extended the set of operations of
            the basic QuantizedConv2D, allowing to modify the padding value per input channel.
            Defaults to False.
        activation (str, optional): activation type to be applied. Defaults to "".
        alpha (float, optional): negative slope coefficient used by some activation
            (e.g. LeakyRelu). Defaults to 0.01.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self,
                 strides=[1, 1],
                 pool_type="none",
                 pool_size=(2, 2),
                 pool_strides=(2, 2),
                 pool_pads=[0, 0, 0, 0],
                 activation="",
                 alpha=0.01,
                 name=''):
        assert pool_type in ["none", "max", "gap"]
        super().__init__("QuantizedConv2D",
                         strides=strides,
                         pool_size=pool_size,
                         pool_strides=pool_strides,
                         pool_pads=pool_pads,
                         alpha=alpha,
                         name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["pool_type"] = pool_type
        self.serialize_attr["activation"] = activation
        self.serialize_attr["scale"] = True

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")
        self._add_weight("pads", dtype="int64")
        self._add_weight("range_max", 1.0)
        self._add_weight("act_range_max", 1.0)

    def __build__(self, input_ts, downscale=True):
        assert input_ts.dtype in (np.uint8, np.int8)
        assert downscale, f"{self.name} ({self.base_name}) does not support 32bit output"
        assert self.weights["kernel"].ndim == 4

        # The chain of operations is modified by the type of input:
        kernel_shape = self.weights["kernel"].shape
        if input_ts.dtype == np.uint8:
            self.base_name = "QuantizedInputConv2D"
            if self.weights["bias"].size == 0:
                # Bias is mandatory on this configuration
                filters = kernel_shape[0]
                self.set_weight("bias", np.zeros(filters, dtype="float32"))

        # Initialize weights
        if self.weights["pads"].size == 0:
            self.set_weight("pads", np.zeros(len(kernel_shape) * 2, dtype="int64"))

        # Compute output shape
        conv_output_shape = compute_onnx_conv_output(self, input_ts.shape)
        output_ts = TENSOR_SHAPE(conv_output_shape, np.dtype("int8"))
        return output_ts

    def __quantize__(self, qinput, force_fp=False):
        i_scale = qinput.weights["scale"]

        # Perform cross-layer equalization, i.e.: rescale weights with input scale.
        # To do that first reshape i_scale to put it into axis = 1 and be capable of broadcasting.
        assert i_scale.ndim <= 1
        kernel = self.weights["kernel"]
        kernel = kernel / align_to(i_scale, kernel.ndim, axis=1)
        # Quantize and set weights
        qweights, i_scale = quantize_to_qfloat(kernel)
        qweights = qweights.astype("int8")

        # Prepare tensors list with unique names
        conv_name = self.name
        prefix = conv_name + "_"
        weights_dict = {}
        bias = self.weights["bias"]
        if "InputConv" in self.op_type:
            # If calibration was done per tensor, repeat zero point over each channel
            zero_point = qinput.weights["zero_point"]
            if zero_point.size == 1:
                zero_point = np.repeat(zero_point, kernel.shape[1])
            weights_dict[prefix + "Xpad"] = zero_point
            # Fold zero point in bias
            # Note: Dequantize kernel instead to use the float to reduce quantization error
            kernel = dequantize(qweights, i_scale, axis=0)
            bias = fold_zero_point(bias, kernel, zero_point)
        weights_dict[prefix + "Wi"] = qweights
        if "Biased" in self.op_type:
            qbias = aligned_quantize(bias, i_scale)
            weights_dict[prefix + "B"] = qbias
        weights_dict[prefix + "pads"] = self.weights["pads"]

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

        # Compute spatial factor when GAP
        if "GlobalAvgPool" in self.op_type:
            input_shape = get_tensor_shape(self.input)
            input_shape = compute_onnx_conv_output(self, input_shape, apply_pool=False)
            i_scale *= input_shape[-2] * input_shape[-1]

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
        t_names = ["X", "", "W", ""]
        if "InputConv" in op_type:
            t_names[1] = "x_pad_value"
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Pad + convolution
        nodes += get_padding_ops(t_names[0], "Xi", t_names[1])
        conv_tensor_names = nodes[-1].output[:1] + t_names[2:]
        nodes.append(make_node("Conv", inputs=conv_tensor_names, outputs=["Yi"]))
        nodes[-1].attribute.append(AP(name="strides", ref_attr_name="strides", type=AP.INTS))

        # Maxpool (optional)
        if "MaxPool" in op_type:
            # Replace previous output as maxpool input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_pool_ops(nodes[-1].output[0], "Yi", pool_op_type="MaxPool")

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

        # AvgPool (optional)
        if "GlobalAvgPool" in op_type:
            # Replace previous output as maxpool input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_pool_ops(nodes[-1].output[0], "Yi", pool_op_type="GlobalAvgPool")

        # Scale out (with saturation) in float domain
        nodes += get_scale_out_ops("Yi", "Yscaled")
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes
