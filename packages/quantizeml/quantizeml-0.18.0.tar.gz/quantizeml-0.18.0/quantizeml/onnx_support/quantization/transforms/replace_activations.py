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
__all__ = ["replace_activations"]

import onnx
import numpy as np

from onnxscript import rewriter

from ..model import ONNXModel
from ...layers.base_layer import BRN_OPSET
from ...layers.subgraph_ops import activation
from ...graph_tools import get_field


def _extract_supported_activations(func=None):
    if func is None:
        # Parse activation function as a FunctionProto through onnxscript.to_function_proto API
        func = activation.to_function_proto()

    # Deduct the type of activations supported by 'func', knowing that:
    # * activation keys (string) are defined as 'Constant' nodes
    # * the definition of 'activation()' should be if...elif...elif...else,
    #   which is serialized by onnxscript through 'If' nodes.
    activations = []
    for node in func.node:
        if node.op_type == 'Constant':
            try:
                # Deserialize activation found in 'value' attribute
                if isinstance(act_name := get_field(node, 'value'), str):
                    activations.append(act_name)
            except Exception:
                ...
        elif node.op_type == 'If':
            # Look activations inside of 'then_branch' (elif cases)
            then_branch = node.attribute[1].g
            activations.extend(_extract_supported_activations(then_branch))
    return activations


ONNX_SUPPORTED_ACTIVATIONS = _extract_supported_activations()


def _rewrite_unfolded_ops(model):
    # Define transformation rules
    rules = [
        rewriter.pattern.RewriteRule(lambda op, x: x * op.Sigmoid(x), lambda op, x: op.Swish(x)),
        rewriter.pattern.RewriteRule(lambda op, x: x * op.HardSigmoid(x,
                                                                      alpha=0.1666666716337204,
                                                                      beta=0.5),
                                     lambda op, x: op.HardSwish(x))
    ]

    # Apply rewrites
    rewrite_rule_set = rewriter.pattern.RewriteRuleSet(rules, commute=True)
    model.rewrite(rewrite_rule_set, check=False)


def _rewrite_prelu_to_leaky_relu(model):
    def _check_prelu_equivalent_with_leaky_relu(ctx, slope, **_):
        if slope.const_value is None:
            # Slope is not an intializer
            return False
        slope_np = np.reshape(slope.const_value.numpy(), -1)
        return np.all(slope_np[0] == slope_np)

    def _prelu_to_leaky_relu_rewrite_pattern(op, x, slope):
        slope_np = np.reshape(slope.const_value.numpy(), -1)
        return op.LeakyRelu(x, alpha=slope_np[0].item())

    # Define transformation rules
    rules = [rewriter.pattern.RewriteRule(lambda op, x, slope: op.PRelu(x, slope),
                                          _prelu_to_leaky_relu_rewrite_pattern,
                                          _check_prelu_equivalent_with_leaky_relu)]

    # Apply rewrites
    rewrite_rule_set = rewriter.pattern.RewriteRuleSet(rules)
    model.rewrite(rewrite_rule_set, check=False)


def replace_activations(model):
    """Converts a set of operations into activation custom node.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    assert isinstance(model, ONNXModel)

    graph_updated = False

    # Rewrite unfolded activations into a single operator
    # Note we replace the model without checking it because some rules are not valid
    # until they are changed by Activation.
    _rewrite_unfolded_ops(model)

    # Rewrite equivalent activations
    _rewrite_prelu_to_leaky_relu(model)

    for node in model.nodes():
        if node.op_type in ONNX_SUPPORTED_ACTIVATIONS:
            graph_updated = True
            # Include legacy operator as an attribute
            node.attribute.append(onnx.AttributeProto(name="main_op_type",
                                                      type=onnx.AttributeProto.STRING,
                                                      s=node.op_type.encode()))
            # Update operator type and domain
            node.op_type = 'activation'
            node.domain = BRN_OPSET.domain

    # Set domain in model opset (model integrity)
    if graph_updated:
        model.set_opset_import(BRN_OPSET.domain, BRN_OPSET.version)
        model.add_function(activation.to_function_proto())

    model.check_model(infer_shapes=False)
