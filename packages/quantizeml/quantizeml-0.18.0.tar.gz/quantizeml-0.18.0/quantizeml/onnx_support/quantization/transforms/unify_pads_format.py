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

__all__ = ["unify_pads_format"]

from onnxscript import ir

from ..model import ONNXModel
from .utils import compute_conv_same_pads


def _get_conv_parameters(ir_node):
    parameters = {}

    # Get kernel shape
    if kernel_shape := ir_node.attributes.get("kernel_shape", None):
        parameters["kernel_shape"] = kernel_shape.value
    else:
        # Deduce kernel shape from weights
        weights = ir_node.inputs[1].const_value
        assert weights is not None, "Kernel shape must be provided or weights must be constant."
        parameters["kernel_shape"] = weights.shape[2:]

    # Get strides
    if strides := ir_node.attributes.get("strides", None):
        parameters["strides"] = strides.value
    else:
        parameters["strides"] = [1] * len(parameters["kernel_shape"])

    return parameters


def unify_pads_format(model):
    assert isinstance(model, ONNXModel)

    # Parse model to IR
    ir_model = ir.from_proto(model.model)
    for ir_node in ir_model.graph:
        # Search and drop 'auto_pad' attribute: after the sanitizer,
        # this attribute will be "NOTSET" (default value) and the pads attribute will be set
        if (auto_pad := ir_node.attributes.pop("auto_pad", None)):
            # Nothing to do if auto_pad was already "NOTSET"
            if auto_pad.value == "NOTSET":
                continue
            # Compute pads following auto_pad mode
            spatial_input_shape = ir_node.inputs[0].shape[2:]
            if auto_pad.value == "VALID":
                pads = 2 * [0] * len(spatial_input_shape)
            else:
                # compute_conv_same_pads is only valid when dilations are 1.
                if ((dilations := ir_node.attributes.get("dilations", None)) and
                        any(d != 1 for d in dilations.value)):
                    raise ValueError(f"{ir_node.name} ({ir_node.op_type}) is supported with "
                                     f"default dilations, not {dilations.value}.")
                pads = compute_conv_same_pads(spatial_input_shape,
                                              mode=auto_pad.value.replace("SAME_", ""),
                                              transpose=ir_node.op_type in ["ConvTranspose"],
                                              **_get_conv_parameters(ir_node))
            # Modify pads attribute
            ir_node.attributes["pads"] = ir.AttrInt64s("pads", pads)

    # Update model with modified graph
    model.model = ir.to_proto(ir_model)
    model.check_model(infer_shapes=False)
