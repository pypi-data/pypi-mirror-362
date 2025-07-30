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
"""
Sanitize to add an identity convolution after some patterns
"""

__all__ = ['insert_identity_convs']

import numpy as np
from onnxscript.rewriter import ir, pattern


def _insert_add_identity_relu_gap(model):
    # Adds an identity convolution after 'Add' in the {Add > Relu/Clip > GlobalAveragePool}
    # pattern
    def relu_pattern(op, x, y):
        add = op.Add(x, y, _outputs=["skip"])
        return op.GlobalAveragePool(op.Relu(add, _outputs=["act"]))

    def clip_pattern(op, x, y):
        add = op.Add(x, y, _outputs=["skip"])
        return op.GlobalAveragePool(op.Clip(add, _allow_other_inputs=True, _outputs=["act"]))

    def replacement_pattern(op, x, y, skip, act, **_):
        add = op.Add(x, y)
        # Insert a conv layer with identity weights
        w = ir.tensor(np.eye(skip.shape[1], dtype="float32")[..., None, None])
        conv = op.Conv(add, op.initializer(w, name=f"{skip.name}_identity_weights"))
        # Include the activation function
        ir_node = act.producer()
        activation = op.op(ir_node.op_type, inputs=[conv, *ir_node.inputs[1:]])
        # Finally, apply the GAP
        return op.GlobalAveragePool(activation)

    def validate_pattern(op, skip, **_):
        # This pattern is only used on Conv2D layers
        return len(skip.shape) == 4

    # Define transformation rules
    rules = [pattern.RewriteRule(relu_pattern, replacement_pattern, validate_pattern),
             pattern.RewriteRule(clip_pattern, replacement_pattern, validate_pattern)]

    # Apply rewrites
    model.rewrite(rules)


def _add_identity_after_skips(model):
    # Adds an identity convolution after a skip connection if next operator is not mappable in CNP.
    def add_pattern(op, x, y):
        return op.Add(x, y, _outputs=["skip"])

    def add_relu_pattern(op, x, y):
        return op.Relu(op.Add(x, y, _outputs=["skip"]))

    def concat_pattern(op, x, y):
        return op.Concat(x, y, _outputs=["skip"])

    def replacement_pattern(op, x, y, skip):
        node = skip.producer()
        z = op.op(node.op_type, inputs=[x, y], attributes=node.attributes, name=node.name)
        # Check if the node is an Add and if it has a Relu
        outbounds = skip.consumers()
        if node.op_type == "Add" and len(outbounds) == 1 and outbounds[0].op_type == "Relu":
            # Special case for Add: Relu is quantized inside the Add operator,
            # therefore identity conv should be added after the Relu
            z = op.Relu(z)
        # Create the identity convolution to insert
        w = ir.tensor(np.eye(skip.shape[1], dtype="float32")[..., None, None])
        return op.Conv(z, op.initializer(w, name=f"{skip.name}_identity_weights"))

    def validate_fn(*_, skip, **__):
        node = skip.producer()
        outbounds = skip.consumers()
        # Condition is checked in Relu outbounds
        if node.op_type == "Add" and len(outbounds) == 1 and outbounds[0].op_type == "Relu":
            skip = outbounds[0].outputs[0]
        # Apply transformation if:
        # * skip inputs are not initializers,
        # * no outbound is mappable in CNP and
        # * output is a 4D tensor
        return (all(x.const_value is None for x in node.inputs) and
                not any(onode.op_type in ["Conv", "ConvTranspose"] for onode in skip.consumers())
                and len(skip.shape) == 4)

    # Define transformation rules
    rules = [pattern.RewriteRule(add_relu_pattern, replacement_pattern, validate_fn),
             pattern.RewriteRule(add_pattern, replacement_pattern, validate_fn),
             pattern.RewriteRule(concat_pattern, replacement_pattern, validate_fn)]

    # Apply rewrites
    model.rewrite(rules)


def _insert_identity_conv_at(x, ir_model, postfix="", replace_all_uses=True):
    # Create a new tensor that will be the output of the conv identity.
    # Then, replace all node inputs with this new value
    y = ir.Value(name=f"{x.name}_identity_conv{postfix}", shape=x.shape, type=x.type)

    if replace_all_uses:
        ir.convenience.replace_all_uses_with(x, y)

    # Create the identity convolution to insert
    w = ir.tensor(np.eye(x.shape[1], dtype="float32")[..., None, None])
    w = ir.Value(name=f"{y.name}_weights", const_value=w)
    conv = ir.node("Conv", [x, w], outputs=[y], name=y.name)
    # Add the new node and its weights to the graph
    ir_model.graph.register_initializer(w)
    ir_model.graph.insert_after(x.producer(), conv)

    return y


def _add_input_conv_identity_split(model):
    # Adds an identity convolution after the first convolution if it has 2 outputs.
    ir_model = ir.from_proto(model.model)
    base_node = ir_model.graph.inputs[0].uses()

    # This sanitize does not support models with multiple inputs
    if not base_node or len(ir_model.graph.inputs) != 1:
        return

    # Skip rescaling nodes
    while len(base_node) == 1 and base_node[0].node.op_type in ["Mul", "Add", "Transpose"]:
        # Target nodes are considered as rescaling if at least one input is an initializer
        if all(x.const_value is not None for x in base_node[0].node.inputs):
            # Target node is a skip connection
            break
        base_node = base_node[0].node.outputs[0].uses()

    if not base_node:
        return

    # Check if the first node is an HRC Conv2D with 2 outputs
    conv_node = base_node[0].node
    if (len(base_node) != 1 or conv_node.op_type != "Conv" or
            conv_node.inputs[0].shape[1] not in [1, 3] or len(conv_node.inputs[0].shape) != 4):
        return

    # Candidate is optionally followed by an activation or MaxPool and with 2 outputs
    x = conv_node.outputs[0]
    while ((next_nodes := x.uses()) and len(next_nodes) == 1 and
           next_nodes[0].node.op_type in ["Relu", "Clip", "activation", "MaxPool"]):
        x = next_nodes[0].node.outputs[0]

    # Candidate must have multiple outputs
    if len(next_nodes) <= 1:
        return

    # Update the model with the identity conv
    _insert_identity_conv_at(x, ir_model)
    model.model = ir.to_proto(ir_model)
    model.check_model()


def _force_different_inbounds_for_skips(model):
    # Adds an identity convolution after 'Add/Concat' that are applied to the same input
    def target_pattern(op_type):
        def _pattern(op, x):
            if op_type == "Add":
                return op.Add(x, x, _outputs=["skip"])
            return op.Concat(x, x, _outputs=["skip"])
        return _pattern

    def replacement_pattern(op_type):
        def _pattern(op, x, skip):
            # Insert a conv node with identity weights
            w = ir.tensor(np.eye(x.shape[1], dtype="float32")[..., None, None])
            w_name = f"{x.name}_identity_weights"
            return op.op(op_type, inputs=[x, op.Conv(x, op.initializer(w, name=w_name))],
                         attributes=skip.producer().attributes)
        return _pattern

    def validate_pattern(*_, x, **__):
        # This pattern works only on 4D tensors
        return len(x.shape) == 4

    rules = []
    for op_type in ["Add", "Concat"]:
        rules.append(pattern.RewriteRule(target_pattern(op_type),
                                         replacement_pattern(op_type),
                                         validate_pattern))

    # Apply rewrites
    model.rewrite(rules)


def _force_two_outbounds(model):
    # Adds an identity convolution to force a node to have maximum 2 outbounds
    ir_model = ir.from_proto(model.model)

    for ir_node in ir_model.graph:
        node_output = ir_node.outputs[0]

        if len(node_output.shape) != 4:
            # This pattern works only on 4D tensors
            continue

        while len((children := node_output.uses())) > 2:
            conv_value = _insert_identity_conv_at(node_output, ir_model,
                                                  postfix=f"_{str(len(children))}",
                                                  replace_all_uses=False)

            # Last Two children will have Identity conv as parent
            # Find index of conv in the childs inputs
            children[-1].node.replace_input_with(children[-1].idx, conv_value)
            children[-2].node.replace_input_with(children[-2].idx, conv_value)

    model.model = ir.to_proto(ir_model)
    model.check_model()


def insert_identity_convs(model):
    """Adds an identity convolution after some patterns.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    _insert_add_identity_relu_gap(model)
    _add_identity_after_skips(model)
    _force_different_inbounds_for_skips(model)
    _add_input_conv_identity_split(model)
    _force_two_outbounds(model)
