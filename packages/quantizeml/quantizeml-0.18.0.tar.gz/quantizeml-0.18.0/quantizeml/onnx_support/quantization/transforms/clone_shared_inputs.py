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

__all__ = ["clone_shared_inputs"]

import copy

from ..model import ONNXModel


def clone_shared_inputs(model):
    """Clones inputs that are shared across multiple ONNX nodes to avoid conflicts.

    Args:
        model (ONNXModel): The ONNX model in which shared inputs should be duplicated.
    """
    assert isinstance(model, ONNXModel), (
        "Unsupported model type: expected ONNXModel "
        f"but got {type(model).__name__}"
    )
    input_name_to_nodes = model.input_name_to_nodes()
    initializers = list(model.initializer())
    for initializer in initializers:
        if len(input_name_to_nodes[initializer.name]) > 1:
            for rep, node in enumerate(input_name_to_nodes[initializer.name][1:]):
                new_initializer = copy.deepcopy(initializer)
                new_initializer.name = f"{initializer.name}_duplicate_{rep}"
                model.add_initializer(new_initializer)
                inputs = list(node.input)
                input_index = inputs.index(initializer.name)
                node.input[input_index] = new_initializer.name
    model.check_model()
