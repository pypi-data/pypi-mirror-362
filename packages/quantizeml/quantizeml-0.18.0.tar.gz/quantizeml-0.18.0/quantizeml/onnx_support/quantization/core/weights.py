#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
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
import numpy as np

from .numpy_helpers import align_to


def _compute_reduce_axes(x, axis):
    N = np.ndim(x)
    if isinstance(axis, int):
        axis = (axis,)
    elif axis is None:
        axis = tuple(range(N))
    # Convert axis in positive
    axis = tuple(i if i >= 0 else N + i for i in axis)
    # Return axes not in axis
    return tuple(i for i in range(N) if i not in axis)


def quantize_to_qfloat(x, bitwidth=8, signed=True, axis=0):
    # Transform axis into reduce_axes
    reduce_axes = _compute_reduce_axes(x, axis)
    # Absolute max value calculated over axis
    abs_max = np.max(np.abs(x), axis=reduce_axes, keepdims=True)
    # Clip absolute max value
    abs_max = np.maximum(abs_max, 2.**-16)
    # Calculate integer ranges
    if signed:
        int_max = 2. ** (bitwidth - 1) - 1
        int_min = -2. ** (bitwidth - 1)
    else:
        int_max = 2. ** bitwidth - 1
        int_min = 0
    # Compute the ideal float scale (in symmetrical range)
    scale = int_max / abs_max
    # Quantize x, projecting it in the ideal scale
    proj_x = x * scale
    qx = np.clip(np.round(proj_x), int_min, int_max).astype(np.int32)
    return qx, np.squeeze(scale)


def quantize_to_fixed_point(x, bitwidth, signed=True, clamp=False, axis=0):
    """Convert a number to a FixedPoint representation

    The representation is composed of a mantissa and an implicit exponent expressed as
    a number of fractional bits, so that:

    x ~= mantissa . 2 ** -frac_bits

    The mantissa is an integer whose bitwidth and signedness are specified as parameters.

    Args:
        x (np.ndarray): the source number or array
        bitwidth (np.ndarray): the desired bitwidth
        signed (bool, optional): when reserving a bit for the sign. Defaults to True.
        clamp (bool, optional): whether to clamp the scale.
            Defaults to False.
        axis (tuple, optional): axis over which the scale is computed. Defaults to 0.

    Returns:
        np.ndarray, np.ndarray: the mantissa and the power-of-two scale
    """
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if np.any(np.isinf(x)):
        raise ValueError(f"Infinite values are not supported. Receives: {x}")
    # Evaluate the number of bits available for the mantissa
    mantissa_bits = bitwidth - 1 if signed else bitwidth
    # Transform axis into reduce_axes
    reduce_axes = _compute_reduce_axes(x, axis)
    # Reduce x to compute a common frac_bits if needed it
    y = np.max(np.abs(x), axis=reduce_axes, keepdims=True)
    # Evaluate the number of bits required to represent the whole part of x
    # as the power of two enclosing the absolute value of x
    # Note that it can be negative if x < 0.5, as well as we force whole_bits = -1 when x is 0
    y = np.where(y == 0, 0.5, y)
    whole_bits = np.ceil(np.log2(y)).astype(np.int32)
    # In the case that x is a power of two, whole_bits is one less than the expected
    # (e.g for x = 8, whole_bits = np.log2(8) = 3, but we expected 4 to represent 8).
    # That is why we increase whole_bits by one when x is a power of two.
    # Note at this point whole_bits is 0 when x is 0
    whole_bits = np.where(y == 2.0 ** whole_bits, whole_bits + 1, whole_bits)
    # Deduce the number of bits required for the fractional part of x
    # Note that it can be negative if the whole part exceeds the mantissa
    frac_bits = mantissa_bits - whole_bits
    if clamp:
        frac_bits = np.minimum(frac_bits, mantissa_bits)
    # Evaluate the 'scale', which is the smallest value that can be represented (as 1)
    scale = 2. ** frac_bits
    # Evaluate the minimum and maximum values for the mantissa
    mantissa_min = -2 ** mantissa_bits if signed else 0
    mantissa_max = 2 ** mantissa_bits - 1
    # Evaluate the mantissa by quantizing x with the scale, clipping to the min and max
    mantissa = np.clip(np.round(x * scale), mantissa_min, mantissa_max).astype(np.int32)
    return mantissa, np.squeeze(scale)


def dequantize(mantissa, scale, axis=-1):
    return mantissa / align_to(scale, mantissa.ndim, axis)
