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
Sanitize to fold batchnorm nodes into previous nodes
"""
__all__ = ['fold_batchnorms']

import numpy as np
from onnxscript.rewriter import ir, pattern

from ..core import align_to


def fold_batchnorms(model):
    """Folds BatchNorm nodes into previous nodes.

        Args:
            model (ONNXModel): The ONNX model to be processed.
    """
    def target_pattern(op_type):
        def _pattern(op, x):
            if op_type == "Gemm":
                y = op.Gemm(x, transB=1, _allow_other_inputs=True, _outputs=["inbound_out"])
            else:
                y = op.ConvTranspose(x, _allow_other_inputs=True, _outputs=["inbound_out"])

            return op.BatchNormalization(y, _allow_other_inputs=True, _outputs=["batchnorm"])

        return _pattern

    def replacement_pattern(op_type):
        def _pattern(op, x, inbound_out, batchnorm):
            batchnorm_node = batchnorm.producer()
            # Get BatchNorm parameters
            gamma, beta, input_mean, input_var = [inp.const_value.numpy() for inp
                                                  in batchnorm_node.inputs[1:]]

            # 1e-5 is the default value for epsilon according to
            # https://onnx.ai/onnx/operators/onnx__BatchNormalization.html#attributes
            default_eps = ir.convenience.convert_attribute("epsilon", 1e-5, ir.AttributeType.FLOAT)
            eps = batchnorm_node.attributes.get("epsilon", default_eps).as_float()

            # Compute the scale_factor to update the convtranspose weights and bias
            scale_factor = gamma / np.sqrt(input_var + eps)

            # Update convtranspose weights
            inbound_node = inbound_out.producer()
            weights = inbound_node.inputs[1].const_value.numpy()
            # Reshape scale factor so it is broadcastable
            axis = 0 if op_type == "Gemm" else 1
            fused_weights = ir.tensor(weights * align_to(scale_factor, weights.ndim, axis=axis))

            # Update bias
            if len(inbound_node.inputs) > 2:
                original_bias = inbound_node.inputs[2].const_value.numpy()
                bias_name = inbound_node.inputs[2].name
            else:
                original_bias = np.zeros_like(input_mean)
                bias_name = x.name + "_bias"

            fused_bias = ir.tensor((original_bias - input_mean) * scale_factor + beta)
            return op.op(op_type,
                         inputs=[x, op.initializer(fused_weights, name=inbound_node.inputs[1].name),
                                 op.initializer(fused_bias, name=bias_name)],
                         attributes=inbound_node.attributes)
        return _pattern

    # Define transformation rules
    rules = []
    for op_type in ["Gemm", 'ConvTranspose']:
        rules.append(pattern.RewriteRule(target_pattern(op_type),
                                         replacement_pattern(op_type)))

    # Apply rewrites
    model.rewrite(rules)
