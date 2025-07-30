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
__all__ = ["invert_activation_maxpool"]

from onnxscript.rewriter import pattern

from ...layers.base_layer import BRN_OPSET
from ..model import ONNXModel


def _target_pattern(op_type):
    def _pattern(op, x):
        # Create the target pattern, as an activation followed by a MaxPool
        if op_type == "Clip":
            y = op.Clip(x, _allow_other_inputs=True, _outputs=["activation"])
        elif op_type == "Relu":
            y = op.Relu(x, _outputs=["activation"])
        elif op_type == "activation":
            y = op.activation(x, _outputs=["activation"], _domain=BRN_OPSET.domain)
        else:
            raise ValueError(f"Unknown op_type: {op_type}")
        return op.MaxPool(y, _outputs=["maxpool"])
    return _pattern


def _replacement_pattern(op, x, maxpool, activation):
    # Swap the MaxPool and activation nodes
    # Note we include the inputs and attributes from the original nodes
    maxpool_node = maxpool.producer()
    activation_node = activation.producer()
    y = op.MaxPool(x, **maxpool_node.attributes)
    return op.op(activation_node.op_type,
                 inputs=[y, *activation_node.inputs[1:]],
                 attributes=activation_node.attributes,
                 domain=activation_node.domain)


def _act_condition(op, activation, **_):
    # Swap is only valid for monotonic increasing activations
    act_node = activation.producer()
    return act_node.attributes['main_op_type'].value in ["LeakyRelu"]


def invert_activation_maxpool(model):
    """Inverts Relu/Clip/Activation and MaxPool nodes in a model to have MaxPool first.

    This transformation produces a strictly equivalent model.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    # Define transformation rules
    rules = [
        pattern.RewriteRule(_target_pattern("Relu"), _replacement_pattern),
        pattern.RewriteRule(_target_pattern("Clip"), _replacement_pattern),
        pattern.RewriteRule(_target_pattern("activation"), _replacement_pattern, _act_condition),
    ]

    # Apply rewrites
    model.rewrite(rules)
