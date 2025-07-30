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
__all__ = ["get_activation_ops", "activation", "get_lut_ops"]

from onnx import TensorProto
from onnx.helper import make_node
from onnxscript import script

from ..base_layer import BRN_OPSET, ONNX_OPSET as op


def get_activation_ops(in_name, out_name, clip=False):
    """Return the activation operation chain.

    Args:
        in_name (str): the input tensor name.
        out_name (str): the required output tensor name.
        clip (bool, optional): whether to include max_value. Defaults to False.

    Returns:
        list of NodeProto: the operation chain.
    """
    nodes = [make_node("Relu", [in_name], [out_name])]
    if clip:
        nodes[0].output[0] = f"{in_name}/relu"
        # Compute bounded activation as Min(input, max_value)
        nodes += [make_node("Cast", ["max_value"], ["max_value/cast"], to=TensorProto.FLOAT),
                  make_node("Min", [nodes[0].output[0], "max_value/cast"], [out_name])]
    return nodes


@script(BRN_OPSET, default_opset=op)
def activation(x, main_op_type: str = "Identity", alpha: float = 0.01):
    if main_op_type == "Gelu":
        y = 0.5 * x * (1.0 + op.Erf(x / op.Sqrt(2.)))
    elif main_op_type == "Swish":
        y = x * op.Sigmoid(x)
    elif main_op_type == "HardSwish":
        y = op.HardSwish(x)
    elif main_op_type == "LeakyRelu":
        y = op.LeakyRelu(x, alpha=alpha)
    else:
        y = x
    return y


def get_lut_ops(in_name, out_name):
    cast_iname = f"{in_name}/input_cast"
    cast_oname = f"{in_name}/output_cast"
    return [make_node("Cast", [in_name], [cast_iname], to=TensorProto.INT32),
            make_node("Gather", ["LUT_values", cast_iname], [cast_oname]),
            make_node("Cast", [cast_oname], [out_name], to=TensorProto.FLOAT)]
