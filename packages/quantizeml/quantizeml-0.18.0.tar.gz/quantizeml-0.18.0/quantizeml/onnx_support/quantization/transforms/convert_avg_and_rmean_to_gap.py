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

__all__ = ["convert_avg_and_rmean_to_gap"]

from onnxscript.rewriter import pattern, ir

from ..model import ONNXModel
from ...graph_tools import check_node_attributes


def _get_avg_rewrite_rule():
    def condition_fn(*_, x, y):
        node = ir.to_proto(y.producer())
        supported_attributes = {'auto_pad': ['NOTSET'],
                                'kernel_shape': [list(x.shape[2:])],
                                'pads': [2 * [0] * (len(x.shape) - 2)]}
        try:
            # Return True if node attributes match with supported ones
            check_node_attributes(node, supported_attributes)
            return True
        except ValueError:
            return False
    return pattern.RewriteRule(lambda op, x: op.AveragePool(x, _outputs=["y"]),
                               lambda op, x, **__: op.GlobalAveragePool(x),
                               condition_fn)


def _get_reduce_mean_rewrite_rule():
    def replacement_pattern(op, x, y, **__):
        ir_node = y.producer()
        y = op.GlobalAveragePool(x)
        # GAP output keeps the same shape as the input.
        # So we flatten it if the original ReduceMean had keepdims=False.
        if (keepdims := ir_node.attributes.get("keepdims", None)) and keepdims.value == 0:
            y = op.Flatten(y)
        return y

    def condition_fn(*_, x, axes, **__):
        if axes.const_value is None:
            return False
        x_rank = len(x.shape)
        # Convert each axis to a positive value.
        pos_axes = sorted([z if z >= 0 else x_rank + z for z in axes.const_value.numpy()])
        # Pattern is valid if reduction axes are all spatial dimensions.
        return pos_axes == list(range(2, x_rank))

    return pattern.RewriteRule(lambda op, x, axes: op.ReduceMean(x, axes, _outputs=["y"]),
                               replacement_pattern,
                               condition_fn)


def convert_avg_and_rmean_to_gap(model):
    """
    Converts AveragePool and ReduceMean node to GlobalAveragePool when equivalent.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    rules = [_get_avg_rewrite_rule(), _get_reduce_mean_rewrite_rule()]

    # Apply rewrites
    model.rewrite(rules)
