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
from onnxruntime.quantization.calibrate import TensorData

from .input_scale import input_scale_no_zp
from .weights import quantize_to_fixed_point


def downscale(range_max, i_scale, force_fp=False, bitwidth=8, scale_bits=8):
    """Calculates the scale that should be applied to an integer tensor
    with i_scale to project it to a desired bitwidth.

    The following set of operations must be applied to the tensor to project it
    into the output scale:

    >>> out_tensor = tensor * scale
    >>> out_tensor = out_tensor >> log2(shift)

    Args:
        range_max (np.ndarray): the maximum calibration range
        i_scale (np.ndarray): the input scale
        force_fp (bool, optional): whether to force output scale as a power-of-two.
            Defaults to False.
        bitwidth (int, optional): the desired output bitwidth. Defaults to 8.
        scale_bits (int, optional): the bitwidth to use when quantizing output scales.
            Defaults to 8.

    Returns:
        np.ndarray, np.ndarray, np.ndarray: the integer scale/shift and the new float scale
    """
    if force_fp:
        # The multi-input layers supported in akida (such as Add) do not include a scale-in
        # operation but only a shift-in. In consequence output must be downscaled as a fixed-point.
        return downscale_fp(range_max, i_scale, bitwidth=bitwidth, scale_bits=scale_bits)
    return downscale_qf(range_max, i_scale, bitwidth, scale_bits=scale_bits)


def downscale_qf(range_max, i_scale, bitwidth=8, scale_bits=8):
    # Compute the ideal output scale
    ocalib_scale = input_scale_no_zp(TensorData(lowest=-range_max, highest=range_max), bitwidth)
    # Divide o_calib_scale by i_scale in the same axis to obtain output scale:
    # this will consider the input scale into account.
    o_scale = ocalib_scale / i_scale
    # Quantize o_scale to fit in scale + shift at 8 bit
    scale, s_out = quantize_to_fixed_point(o_scale, bitwidth=scale_bits, signed=False)
    return scale, np.array(s_out, "float32"), np.array(ocalib_scale, "float64")


def downscale_fp(range_max, i_scale, bitwidth=8, scale_bits=8):
    # Dequantize inputs in integer domain (apply scale out), multiplying by the inverse scale
    scale, in_shift = quantize_to_fixed_point(1.0 / i_scale, bitwidth=scale_bits, signed=False)
    # Compute output shift and output scale
    shift, o_scale = downshift(range_max, in_shift, bitwidth=bitwidth)
    return scale, shift, o_scale


def downshift(range_max, i_scale, bitwidth=8):
    def _round_log2(x):
        return 2.0**np.round(np.log2(x))

    # This operation is feasible if and only if input scale is a power-of-two
    np.testing.assert_array_equal(i_scale, _round_log2(i_scale), "Required a power-of-two")
    # Compute the required output shift to come out in bitwidth
    _, out_shift = quantize_to_fixed_point(range_max, bitwidth=bitwidth, signed=True, clamp=True)
    # Compute shift to go from in_shift to out_shift in the same axis
    # The shift can be positive (left-shift) or negative (rounded right-shift)
    shift = out_shift / i_scale
    # A positive shift exceeding the target bitwidth always leads to a saturation
    np.testing.assert_array_less(shift, 2.0**bitwidth,
                                 f"Cannot rescale inputs to {bitwidth} as it will saturate.")
    # In ONNX output shift is done as division (against to akida: a left shift)
    shift = np.array(1.0 / shift, dtype=np.float32)
    return shift, np.array(out_shift, "float64")


def round_to_nearest_pow2(x):
    """Round a number to the nearest power of two.

    Args:
        x (float): A number.

    Returns:
        float: The nearest power of two for the given number.
    """
    safe_abs = np.where(x == 0, 1.0, np.abs(x))

    # nearest integer exponent for every element
    exponent = np.round(np.log2(safe_abs))

    # reconstruct ±2**exponent
    y = np.sign(x) * np.power(2.0, exponent)

    return y
