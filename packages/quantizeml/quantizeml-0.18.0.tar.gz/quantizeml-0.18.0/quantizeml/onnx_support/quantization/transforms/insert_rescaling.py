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

__all__ = ["insert_rescaling"]

import uuid
import numpy as np
import onnx.numpy_helper
from onnx.helper import make_node

from ...graph_tools import get_field
from ...layers import BRN_OPSET
from ..model import ONNXModel


def _add_rescale_node(onnx_model, input_name, output_name, scale=1.0, offset=0.0, perm=[]):
    """Creates a custom Rescale node as the sequence of (Tranpose) -> Mul -> (Add) operations

    Args:
        onnx_model (ONNXModel): The ONNX model to which the rescale node will be added.
        input_name (str): The name of the input tensor for the rescale operation.
        output_name (str): The name of the output tensor for the rescale operation.
        scale (float or list, optional): The scaling factors to apply to the model inputs.
            Defaults to 1.0.
        offset (float or list, optional): The offset values to apply after scaling the model
            inputs. Defaults to 0.0.
        perm (list, optional): The permutation to apply to the dimensions of the rescale
            node inputs. Defaults to [].
    """
    def _format_weight(x):
        x = np.array(x, dtype="float32")
        if np.size(x) == 1:
            x = np.squeeze(x)
        return x

    nodes, weights = [], []
    inode = input_name
    unique_id = str(uuid.uuid4())

    # Create a Transpose node if permutation changes the order of inputs
    needs_to_tranpose = any(x != idx for idx, x in enumerate(perm))
    if needs_to_tranpose:
        nodes.append(make_node('Transpose',
                               inputs=[inode],
                               outputs=[f"{input_name}/transposed_{unique_id}"],
                               perm=perm))
        inode = nodes[-1].output[0]

    # Create a Scale node
    # Note we need to permute scale since transpose is applied as first operation
    nodes.append(make_node("Mul",
                           inputs=[inode, f"{input_name}/input_scale_{unique_id}"],
                           outputs=[f"{input_name}/scaled_{unique_id}"]))
    weights.append(onnx.numpy_helper.from_array(_format_weight(scale), nodes[-1].input[1]))
    inode = nodes[-1].output[0]

    # Create an Offset node if needed
    # Note we need to permute scale since transpose is applied as first operation
    if np.any(offset != 0.0):
        nodes.append(make_node("Add",
                               inputs=[inode, f"{input_name}/input_offset_{unique_id}"],
                               outputs=[f"{input_name}/shifted_{unique_id}"]))
        weights.append(onnx.numpy_helper.from_array(_format_weight(offset), nodes[-1].input[1]))

    # Replace last name if there are at least one node to append
    if len(nodes) > 0:
        nodes[-1].output[0] = output_name

    # Add nodes to onnx/weights to model
    onnx_model.initializer_extend(weights)
    onnx_model.add_nodes(nodes)


def insert_rescaling(model):
    """Insert a Custom Rescaling node in the model which applies a scaling factor,
    offset, and optional transposes the inputs.

    Args:
        model (ONNXModel): The ONNX model to be processed.
    """
    def _get_variables(node):
        values = []
        for inode in node.input:
            try:
                values.append(model.get_variable(inode))
            except AssertionError:
                values.append(None)
        return values

    assert isinstance(model, ONNXModel)
    assert len(model.input) == 1, "Only a single input is supported"

    # Start with the first node only if the input is connected to one node
    # Otherwise, create a fake node to skip main loop
    first_nodes = model.input_name_to_nodes()[model.input[0].name]
    node = first_nodes[0] if len(first_nodes) == 1 else onnx.NodeProto()

    # We don't add rescaling node if the model is quantized
    if node.op_type in ("InputQuantizer") and node.domain == BRN_OPSET.domain:
        return

    # Default Rescale parameters
    rank = len(model.get_input_shape(model.input[0].name))
    scale, offset, perm = np.ones([1] * rank), np.zeros([1] * rank), list(range(rank))
    nodes_to_remove = []

    # Main loop
    while node.op_type in ("Mul", "Add", "Sub", "Transpose", "Div"):
        variables = _get_variables(node)
        if node.op_type != "Transpose" and all(x is None for x in variables):
            # Nothing to do if there is no initializer in math ops
            break

        # Apply transformation to current values
        # Note that it does not make sense for both inputs
        # to be initializers (the graph would be disconnected).
        new_value = next((x for x in variables if x is not None), None)
        if node.op_type == "Mul":
            # Scale and offset are both multiplied by the Mul scale
            scale = scale * new_value
            offset = offset * new_value
        elif node.op_type == "Div":
            if variables[1] is None:
                # When input is in the second position, rescaling is no longer compatible.
                break
            # Update scale
            scale = scale / new_value
        elif node.op_type == "Add":
            offset = offset + new_value
        elif node.op_type == "Sub":
            # The operation changes according to the position of the initializer
            if variables[0] is None:
                # y = (scale*X + offset) - new_value = scale*X + offset - new_value
                offset = offset - new_value
            else:
                # y = new_value - (scale*X + offset) = -scale*X + new_value - offset
                offset = new_value - offset
                scale = -1 * scale
        elif node.op_type == "Transpose":
            next_perm = get_field(node, "perm", default=list(range(rank))[::-1])
            # transpose rescale parameters
            scale = np.transpose(scale, next_perm)
            offset = np.transpose(offset, next_perm)
            perm = [next_perm[x] for x in perm]

        nodes_to_remove.append(node)

        # Break loop if current node has multiple outbounds
        outbounds = model.get_children(node)
        if len(outbounds) != 1:
            break

        # Get next node
        node = outbounds[0]

    # If no nodes to remove are found, we create a new value info.
    # This value info will be the output of the rescale node, as the input
    # of the first node is the graph's input and will be redirected to the rescale node.
    if nodes_to_remove == []:
        rescale_output_name = f"{model.input[0].name}/rescaled"
        rescale_output_value_info = model.find_value_info_by_name(
            model.input[0].name).__deepcopy__()
        rescale_output_value_info.name = rescale_output_name
        model.graph().value_info.append(rescale_output_value_info)
        model.replace_input_of_all_nodes(model.input[0].name, rescale_output_name)
    else:
        rescale_output_name = nodes_to_remove[-1].output[0]

    # Add the rescale node as a sequence of (Transpose) + (Mul) + (Add)
    rescale_input_name = model.input[0].name
    _add_rescale_node(model, rescale_input_name, rescale_output_name, scale, offset, perm)
    model.remove_nodes(nodes_to_remove)

    # As we add new nodes, we need to topologically sort the model graph
    model.topological_sort()
    model.clean_initializers()
    model.check_model()
