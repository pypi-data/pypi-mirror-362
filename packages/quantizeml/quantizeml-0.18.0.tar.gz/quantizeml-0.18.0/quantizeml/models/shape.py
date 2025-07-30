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

import numpy as np
import tensorflow as tf


def set_model_shape(model, samples=None, input_shape=None):
    """Set the model input shape by inferring from sample data or manually provided shape.
    If both `samples` and `input_shape` are provided, only `samples` will be used.

    Args:
        model (keras.Model): The model whose input shape needs to be set.
        samples (tf.Dataset, tf.Tensor or np.array, optional): Sample input data used to
            infer the shape. If provided, the model input shape will be updated from these samples.
            (excluding batch size). Defaults to None.
        input_shape (list or tuple, optional): Specifies the new input shape for the model.
            in the format of (H, W, C) for 4D inputs or (T, H, W, C) for 5D inputs.
            Used only if `samples` is not provided. Defaults to None.

    Returns:
        keras.Model: The model with static shapes (the original model when shapes are not dynamic)
    """
    def shape_from_samples(samples):
        if not isinstance(samples, (np.ndarray, tf.Tensor, tf.data.Dataset)):
            raise ValueError(
                "'samples' must be either a NumPy ndarray, tf.Tensor or a tf.data.Dataset. "
                f"Received {type(samples).__name__} instead."
            )

        if isinstance(samples, tf.data.Dataset):
            samples = samples.element_spec

            if isinstance(samples, tuple):
                samples = samples[0]
            elif isinstance(samples, dict):
                key = model.input.name
                try:
                    samples = samples[key]
                except KeyError:
                    raise ValueError(f"Missing data for input {key}. You passed samples "
                                     f"with keys {list(samples.keys())}. Expected the following "
                                     f"key: {key}.")

        return list(samples.shape[1:])

    if not model.built:
        if samples is None and input_shape is None:
            raise RuntimeError("Expecting a built model or"
                               " input_shape/samples to set the model shape.")
        if samples is not None:
            model.build((None, *shape_from_samples(samples)))
        else:
            model.build((None, *input_shape))

    if isinstance(model.input_shape, list):
        raise RuntimeError("Only single input models are supported.")

    if samples is None and input_shape is None and _is_dynamic_shape(model):
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
        input_shape = shape_from_samples(samples)

        # Insert time dimension if needed (e.g. for Conv3D -> BufferTempConv)
        if len(model.input_shape) == 5 and len(input_shape) == 3:
            input_shape.insert(0, 1)

    return _set_shape(model, input_shape)


def _is_dynamic_shape(model):
    # Input shape is dynamic if any of its dimension (except for batch) is dynamic
    return any([shape is None for shape in model.input_shape[1:]])


def _set_shape(model, input_shape):
    if len(input_shape) != len(model.input_shape) - 1:
        raise ValueError(
            f"Expected 'input_shape' to have same rank as model input shape "
            f"(excluding batch dimension). But got {input_shape} with {len(input_shape)} "
            f"elements instead of {len(model.input_shape) - 1}."
        )

    config = model.get_config()
    config['layers'][0]['config']['batch_input_shape'] = (None, *input_shape)
    for layer_config in config["layers"]:
        layer_config.pop('build_config', None)

    # Rebuild model and transfer weights
    updated_model = model.from_config(config)
    updated_model.set_weights(model.get_weights())

    return updated_model
