#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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

__all__ = ["ExtractToken", "QuantizedExtractToken"]

import keras
import tensorflow as tf

from .layers_base import (register_quantize_target, register_no_output_quantizer,
                          tensor_inputs, register_aligned_inputs, QuantizedLayer)
from ..tensors import FixedPoint


@keras.saving.register_keras_serializable()
class ExtractToken(keras.layers.Layer):
    """ Wrapper class of `tf.gather` operation that allows to extract a Token.

    Args:
        token (int): the indice of the token to extract.
        axis (int, optional): axis over which the user gather the token. Defaults to 1.

    """

    def __init__(self, *args, token, axis=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.axis = axis

    def call(self, inputs):
        return tf.gather(inputs, self.token, axis=self.axis)

    def get_config(self):
        config = super().get_config()
        config.update({"token": self.token})
        config.update({"axis": self.axis})
        return config


@register_quantize_target(ExtractToken)
@register_no_output_quantizer
@register_aligned_inputs
@keras.saving.register_keras_serializable()
class QuantizedExtractToken(QuantizedLayer, ExtractToken):
    """ Quantized version of the ExtractToken layer. Accepts only FixedPoint inputs.
    """

    @tensor_inputs([FixedPoint])
    def call(self, inputs):
        return tf.gather(inputs, self.token, axis=self.axis)

    def get_config(self):
        return ExtractToken.get_config(self)
