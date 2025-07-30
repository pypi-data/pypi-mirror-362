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

__all__ = ["reset_buffers"]

import keras
import onnx

from ..onnx_support.quantization.model import ONNXModel
from ..onnx_support.layers.buffer_temp_conv import reset_buffers as reset_buffers_onnx
from ..layers.buffer_temp_conv import reset_buffers as reset_buffers_keras


def reset_buffers(model):
    """Resets all FIFO-buffers of the given model.

    Args:
        model (ONNXModel or keras.Model): The model to reset.
    """
    assert isinstance(model, (onnx.ModelProto, ONNXModel, keras.Model)), (
        "Unsupported model type: expected onnx.ModelProto or ONNXModel or keras.Model, "
        f"but got {type(model).__name__}"
    )
    if isinstance(model, (onnx.ModelProto, ONNXModel)):
        reset_buffers_onnx(model)
    else:
        reset_buffers_keras(model)
