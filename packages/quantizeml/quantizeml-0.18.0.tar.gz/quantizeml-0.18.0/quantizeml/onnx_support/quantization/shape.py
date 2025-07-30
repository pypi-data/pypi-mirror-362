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

__all__ = ["set_model_shape"]


import warnings

from .model import ONNXModel


def set_model_shape(model, samples=None, input_shape=None):
    """Set the model input shape by inferring from sample data or manually provided shape.
    If both `samples` and `input_shape` are provided, only `samples` will be used.

    Args:
        model (ONNXModel): The model whose input shape needs to be updated.
        samples (np.ndarray, optional): Sample input data used to infer the shape.
            If provided, the spatial dimensions (height and width) will be set from these samples.
            Defaults to None.
        input_shape (Iterable, optional): An iterable specifying the new model input shape
            in the format of (C, H, W) for 4D inputs or (C, T, H, W) for 5D inputs.
            Used only if `samples` is not provided. Defaults to None.

    Returns:
        The model with static shapes.
    """
    assert isinstance(model, ONNXModel)

    if len(model.get_non_initializer_inputs()) != 1:
        raise RuntimeError("Only single input models are supported.")

    model_input_dims = model.input[0].type.tensor_type.shape.dim
    if samples is None and input_shape is None and _is_dynamic_shape(model_input_dims):
        raise RuntimeError(
            "The model has a dynamic input shape, but neither 'samples' nor 'input_shape' "
            "was provided.")

    if samples is None and input_shape is None:
        # Nothing change when model has static shape and samples and input_shape are not provided
        return model

    if samples is not None:
        if input_shape is not None:
            warnings.warn(
                "Both 'samples' and 'input_shape' were provided. 'samples' will be used "
                "to infer the model shape, and 'input_shape' will be ignored.")

        # Exclude batch dimension
        input_shape = list(samples.shape[1:])
        if len(model_input_dims) == 5 and len(input_shape) == 3:
            # Add a dimension for the time (e.g for Conv3D (converted to BufferTempConv) nodes
            # that are calibrated with 4D samples.)
            input_shape.insert(1, 1)

    return _set_shape(model, input_shape)


def _is_dynamic_shape(input_dims):
    # Input shape is dynamic if any of height and width is dynamic
    return any([dim.dim_value == 0 for dim in input_dims[1:]])


def _set_shape(model, input_shape):
    input_dims = model.input[0].type.tensor_type.shape.dim

    if len(input_shape) != len(input_dims) - 1:
        raise ValueError(
            f"Expected input_shape to have same rank as model input shape "
            f"(excluding batch dimension). But got {input_shape} with {len(input_shape)} "
            f"elements instead of {len(input_dims) - 1}."
        )

    # Make batch dimension always dynamic
    model.input[0].type.tensor_type.shape.dim[0].ClearField("dim_value")
    model.input[0].type.tensor_type.shape.dim[0].dim_param = "N"

    # Update other dimensions
    for axis, shape in enumerate(input_shape, start=1):
        model.input[0].type.tensor_type.shape.dim[axis].dim_value = shape

    # Clear graph value info
    model.graph().ClearField("value_info")

    # Update output shape
    for output in model.output:
        output_dims = output.type.tensor_type.shape.dim
        for axis in range(len(output_dims)):
            output.type.tensor_type.shape.dim[axis].ClearField("dim_value")
            output.type.tensor_type.shape.dim[axis].ClearField("dim_param")

    # Check model and infer shapes
    model.check_model()
    return model
