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
__all__ = ["set_weights_on_qnode", "set_max_value_on_qnode", "set_range_max_on_qnode"]

import numpy as np

from ..graph_tools import get_variable
from .layer_compatibility import check_clip_relu_compatibility


def set_weights_on_qnode(qnode, onnx_node, graph):
    kernel = get_variable(onnx_node.input[1], graph)
    qnode.set_weight("kernel", kernel)
    # If third attribute is there and it is not empty, then there is a bias
    if len(onnx_node.input) == 3 and onnx_node.input[2]:
        qnode.set_weight("bias", get_variable(onnx_node.input[2], graph))


def set_max_value_on_qnode(qnode, clip_node, graph):
    check_clip_relu_compatibility(clip_node, graph)
    qnode.set_weight("max_value", get_variable(clip_node.input[2], graph))


def set_range_max_on_qnode(qnode, out_ranges, name="range_max", reduce=False):
    range_max = np.maximum(np.abs(out_ranges.lowest), np.abs(out_ranges.highest))
    if reduce:
        range_max = np.array(np.max(range_max), range_max.dtype)
    qnode.set_weight(name, range_max)
