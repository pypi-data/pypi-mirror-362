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
__all__ = ["compute_conv_same_pads"]

import math


def compute_conv_same_pads(input_shape, kernel_shape, strides, mode="UPPER", transpose=False):
    """Compute pads values for convolution-type operations.

    Args:
        input_shape (tuple of ints): the spatial input shape.
        kernel_shape (tuple of ints): the convolutional kernel shape.
        strides (tuple of ints): the convolutional strides.
        mode (str, optional): the padding mode. Defaults to "UPPER".
        transpose (bool, optional): whether the operation is a transposed convolution.
            Defaults to False.

    Returns:
        list of ints: the pads to apply.
    """
    assert mode in ["UPPER", "LOWER"], f"Unsupported mode {mode}."
    bottom_pads, top_pads = [], []
    for x, k, s in zip(input_shape, kernel_shape, strides):
        # Compute the output shape and the total padding to apply
        if transpose:
            out_shape = x * s
            total_pads = max(0, (x - 1) * s + k - out_shape)
        else:
            out_shape = math.ceil(x / s)
            total_pads = max(0, (out_shape - 1) * s + k - x)

        # Depending of mode, apply the padding to the upper or lower part
        pad1 = total_pads // 2
        pad2 = total_pads - pad1
        if mode == "UPPER":
            bottom_pads.append(pad1)
            top_pads.append(pad2)
        else:
            top_pads.append(pad1)
            bottom_pads.append(pad2)
    return bottom_pads + top_pads
