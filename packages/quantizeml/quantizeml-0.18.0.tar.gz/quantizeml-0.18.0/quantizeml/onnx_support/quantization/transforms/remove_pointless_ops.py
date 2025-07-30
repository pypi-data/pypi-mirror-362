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

__all__ = ["remove_pointless_ops"]

from onnxscript.rewriter import pattern, ir

from ..model import ONNXModel


def _remove_dropout_rewriter():
    def target_pattern(op, x):
        return op.Dropout(x, _allow_other_inputs=True, _outputs=["y"])

    def replacement_pattern(op, x, **__):
        # Avoid disconnected graph issues by replacing Dropout with Identity.
        return op.Identity(x)

    def condition_fn(*_, y, **__):
        ir_node = y.producer()
        try:
            # Check node contains training mode as input and it is disable.
            return not ir_node.inputs[2].const_value.numpy()
        except Exception:
            # In other case it is possible to remove Dropout,
            # since training_mode is False by default.
            return True

    return pattern.RewriteRule(target_pattern, replacement_pattern, condition_fn)


def remove_pointless_ops(model):
    assert isinstance(model, ONNXModel)

    # Apply rewrites
    rules = [_remove_dropout_rewriter()]
    model.rewrite(rules)
    ir_model = ir.from_proto(model.model)

    # Safely remove Identity nodes
    nodes_to_remove = []
    for ir_node in ir_model.graph:
        if ir_node.op_type == "Identity":
            ir.convenience.replace_all_uses_with(ir_node.outputs, ir_node.inputs)
            nodes_to_remove.append(ir_node)
    ir_model.graph.remove(nodes_to_remove, safe=True)

    # Come back to ONNX model
    model.model = ir.to_proto(ir_model)
    model.check_model(infer_shapes=False)
