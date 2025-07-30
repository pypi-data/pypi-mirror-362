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
__all__ = ["compute_lut_values"]

import numpy as np

from .weights import quantize_to_qfloat, dequantize
from ...layers.subgraph_ops import activation


def compute_lut_values(op_type, scale, bitwidth=11, out_bitwidth=14, **activation_kwargs):
    # Sanitize check
    if np.size(scale) != 1:
        raise ValueError("Unsupported scale format: it must be a scalar.")

    # Generate inputs spread over [-int_max, int_max[
    # Note the order of the values: [0, int_max] + [-int_max, -1].
    # This ensures the lut operation through a gather with negative indices.
    int_max = 2**(bitwidth - 1)
    qinputs = np.array(list(range(int_max)) + list(range(-int_max, 0)))
    finputs = dequantize(qinputs, scale).astype("float32")

    # Compute the activation function
    foutputs = activation(finputs, op_type, **activation_kwargs)

    # Quantize outputs with a scale as a power-of-two
    values, out_scale = quantize_to_qfloat(foutputs, out_bitwidth, axis=())
    return values, out_scale
