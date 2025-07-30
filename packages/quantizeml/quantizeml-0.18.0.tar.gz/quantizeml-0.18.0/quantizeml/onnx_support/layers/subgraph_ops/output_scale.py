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
__all__ = ["get_scale_out_ops"]

from onnx.helper import make_node

from .cast import cast_tensors_to


def get_scale_out_ops(in_name, out_name, scale_name="Scale", shift_name="Shift", bitwidth=8):
    """Return the scale out operation chain, following the steps:

    1. Apply shift and scale to inputs,
    2. Perform Round(x) as Floor(x + 0.5) (to workaround banker's rounding),
    3. Clip in output range [-2**(bitwidth - 1), 2**(bitwidth - 1) - 1].

    Args:
        in_name (str): the input tensor name.
        out_name (str): the required output tensor name.
        scale_name (str, optional): the scale tensor name. Defaults to Scale.
        shift_name (str, optional): the shift tensor name. Defaults to Shift.
        bitwidth (int, optional): value defining the saturation range. Defaults to 8.

    Returns:
        list of NodeProto: the operation chain.
    """
    nodes = []
    # Cast scale and shift to float
    cast_nodes, (scale_name, shift_name) = cast_tensors_to([scale_name, shift_name])
    nodes += cast_nodes

    # Apply shift + scale
    # Note: We apply first shift to avoid (on float) the saturation due to the mantissa.
    nodes.append(make_node("Div", [in_name, shift_name], [f"{in_name}/scaled"]))
    if scale_name:
        nodes[-1].output[0] = f"{in_name}/div"
        nodes.append(make_node("Mul", [f"{in_name}/div", scale_name], [f"{in_name}/scaled"]))
    # Round as Floor(x + 0.5)
    # Note: for positive shift, the results being integer, the rounding has no effect.
    # We therefore apply the same operations for both shifts.
    nodes += [make_node("Constant", [], [f"{in_name}/OneHalf"], value_float=0.5),
              make_node("Add", [f"{in_name}/scaled", f"{in_name}/OneHalf"], [f"{in_name}/half"]),
              make_node("Floor", [f"{in_name}/half"], [f"{in_name}/q"])]
    # Clip in output range
    min_range, max_range = [-2.**(bitwidth - 1), 2.**(bitwidth - 1) - 1]
    nodes += get_saturate_ops(f"{in_name}/q", out_name, min_range, max_range)
    return nodes


def get_saturate_ops(in_name, out_name, min_range=-128.0, max_range=127.0):
    """Return the saturation operation chain.

    Args:
        in_name (str): the input tensor name.
        out_name (str): the required output tensor name.
        min_range (float, optional): the minimum value. Defaults to -128.
        max_range (float, optional): the maximum value. Defaults to 127.

    Returns:
        list of NodeProto: the operation chain.
    """
    min_range_name, max_range_name = f"{in_name}/min_range", f"{in_name}/max_range"
    nodes = [make_node("Constant", [], [min_range_name], value_float=min_range),
             make_node("Constant", [], [max_range_name], value_float=max_range),
             make_node("Clip", [in_name, min_range_name, max_range_name], [out_name])]
    return nodes
