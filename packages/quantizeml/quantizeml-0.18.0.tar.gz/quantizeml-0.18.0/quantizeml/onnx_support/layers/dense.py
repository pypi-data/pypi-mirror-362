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
__all__ = ["QuantizedDense1D", "get_qgemm"]

import numpy as np
from onnx import TensorProto as TP, NodeProto
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .set_weights import set_weights_on_qnode, set_max_value_on_qnode, set_range_max_on_qnode
from ..graph_tools import (TENSOR_SHAPE, get_node, get_activation, get_tensor_shape,
                           check_node_attributes)
from ..quantization.core import quantize_to_qfloat, aligned_quantize, align_to, downscale


def get_qgemm(nodes, graph, tensor_ranges):
    gemm_node = get_node(nodes, 'Gemm')
    assert gemm_node is not None

    # Check supported attributes
    check_node_attributes(gemm_node, {'alpha': [1.0], 'beta': [1.0], 'transA': [0], 'transB': [1]})

    # Retrieve attributes
    flatten = bool(get_node(nodes, 'Flatten'))
    act_node = get_activation(nodes) or NodeProto()
    qgemm = QuantizedDense1D(flatten=flatten, activation=act_node.op_type, name=gemm_node.name)

    # Sets the weights to configure the operation chain
    set_weights_on_qnode(qgemm, gemm_node, graph)
    if act_node.op_type == "Clip":
        set_max_value_on_qnode(qgemm, act_node, graph)

    # Set calibration ranges
    set_range_max_on_qnode(qgemm, tensor_ranges[nodes[-1].output[0]])
    return qgemm


class QuantizedDense1D(OnnxLayer):
    """Intermediate representation of Flatten() + QGemm() + ReLU() as an exportable node.

    Args:
        flatten (bool, optional): whether to flatten the inputs. Defaults to False.
        activation (str, optional): activation type to be applied. Defaults to "".
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, flatten=False, activation="", name=''):
        super().__init__("QuantizedDense1D", name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["flatten"] = flatten
        self.serialize_attr["activation"] = activation

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")
        self._add_weight("range_max", 1.0)

    def __build__(self, input_ts, downscale=True):
        assert input_ts.dtype == np.int8
        assert self.weights["kernel"].ndim == 2
        filters = self.weights["kernel"].shape[0]

        # The chain of operations is modified if downscale is needed
        self.serialize_attr["scale"] = downscale

        # Compute output shape
        output_type = "int8" if downscale else "int32"
        output_ts = TENSOR_SHAPE((input_ts.shape[0], filters), np.dtype(output_type))
        return output_ts

    def __quantize__(self, qinput, force_fp=False):
        i_scale = qinput.weights["scale"]
        kernel = self.weights["kernel"]
        filters, channels = kernel.shape

        # Rescale kernel according to input scale. This operation is different if
        # pattern contain a Flatten.
        assert i_scale.ndim <= 1
        if 'Flatten' in self.op_type:
            # If flatten is there, we need to reshape weights to apply input scale
            _, c, x, y = get_tensor_shape(self.input)
            # Unroll first flattened inputs
            kernel = np.reshape(kernel, (filters, c, x, y))
            # Divide kernel by input shape (that has shape of c)
            kernel = kernel / align_to(i_scale, kernel.ndim)
            # Reshape back to original shape
            kernel = np.reshape(kernel, (filters, channels))
        else:
            kernel = kernel / align_to(i_scale, kernel.ndim)
        # Quantize and set weights
        qweights, i_scale = quantize_to_qfloat(kernel)
        qweights = qweights.astype("int8")

        # Prepare tensors list with unique names
        gemm_name = self.name
        prefix = gemm_name + "_"
        weights_dict = {prefix + "Wi": qweights}
        if "Biased" in self.op_type:
            qbias = aligned_quantize(self.weights["bias"], i_scale)
            weights_dict[prefix + "B"] = qbias

        # Quantize max value when there is an activation
        if "Clipped" in self.op_type:
            qmax_value = aligned_quantize(self.weights["max_value"], i_scale, signed=False)
            weights_dict[prefix + "max_value"] = align_to(qmax_value, qweights.ndim)

        output_scale = i_scale
        if "Scaled" in self.op_type:
            # Now consider calibrated output range
            range_max = self.weights["range_max"]
            scale, s_out, output_scale = downscale(range_max, output_scale, force_fp=force_fp)
            # Add scale out inputs and weights
            weights_dict[prefix + "M"] = align_to(scale.astype("uint8"), qweights.ndim)
            weights_dict[prefix + "S_out"] = align_to(s_out, qweights.ndim)

        # Return quantized weights and ouput scale
        return weights_dict, output_scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", ""]
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Flatten (optional)
        if "Flatten" in op_type:
            nodes.append(make_node("Flatten", inputs=t_names[:1], outputs=["Xflat"]))
            t_names[0] = "Xflat"

        # Gemm
        nodes.append(make_node("Gemm", inputs=t_names, outputs=["Yi"], transB=1))

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Apply final scale (with saturation) (optional)
        if "Scaled" in op_type:
            nodes += get_scale_out_ops("Yi", "Yscaled")
            nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        else:
            nodes.append(make_node("Cast", ["Yi"], ["Y"], to=TP.INT32))
        return nodes
