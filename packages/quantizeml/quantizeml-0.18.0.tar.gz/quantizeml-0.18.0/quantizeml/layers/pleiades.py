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

__all__ = ["PleiadesLayer"]

from keras.layers import Conv3D
from keras.utils import register_keras_serializable
import tensorflow as tf
import numpy as np
from scipy.special import jacobi


def get_ortho_polynomials(length, degrees, alpha, beta):
    """ Generate the set of Jacobi orthogonal polynomials with shape (degrees + 1, length)

    Args:
        length (int): The length of the discretized temporal kernel,
            assuming the range [0, 1] for the polynomials.
        degrees (int): The maximum polynomial degree. Note that degrees + 1 polynomials
            will be generated (counting the constant).
        alpha (float): The alpha Jacobi parameter.
        beta (float): The beta Jacobi parameter.

    Returns:
        np.ndarray: shaped (degrees + 1, length)
    """
    coeffs = np.vstack([np.pad(np.flip(jacobi(degree, alpha, beta).coeffs), (0, degrees - degree))
                        for degree in range(degrees + 1)]).astype(np.float32)
    steps = np.linspace(0, 1, length + 1)
    X = np.stack([steps ** (i + 1) / (i + 1) for i in range(degrees + 1)])
    polynomials_integrated = coeffs @ X
    transform = np.diff(polynomials_integrated, 1, -1) * length
    return transform


@register_keras_serializable()
class PleiadesLayer(Conv3D):
    """A 3D convolutional layer utilizing orthogonal polynomials for kernel transformation.

    Inherits from `Conv3D` and modifies its kernel transformation before applying convolution.

    Args:
        filters (int): Number of output filters.
        kernel_size (tuple): Size of the convolution kernel.
        degrees (int): Degree of the orthogonal polynomials.
        alpha (float): Alpha parameter for the orthogonal polynomials.
        beta (float): Beta parameter for the orthogonal polynomials.
        **kwargs: Additional arguments passed to `Conv3D`.
    """
    def __init__(self, filters, kernel_size, degrees, alpha, beta, **kwargs):
        super().__init__(filters, kernel_size, **kwargs)

        self.degrees = degrees
        self.alpha = alpha
        self.beta = beta

    def build(self, input_shape):
        with tf.name_scope(self.name + '/'):
            super().build(input_shape)
            # Generate the transformation matrix
            transform = get_ortho_polynomials(self.kernel_size[0], self.degrees, self.alpha,
                                              self.beta)
            transform = tf.convert_to_tensor(transform, dtype=tf.float32)
            # Normalize transform based on input dimensions
            scale = tf.sqrt(tf.cast(input_shape[-1],
                                    tf.float32)) * tf.sqrt(tf.cast(self.kernel_size[0],
                                                                   tf.float32))
            self.transform = transform / scale
            new_kernel_shape = (self.kernel.shape[-2], self.filters, self.kernel_size[1],
                                self.kernel_size[2], self.degrees + 1)
            self.kernel = self.add_weight(shape=new_kernel_shape,
                                          initializer=self.kernel_initializer,
                                          trainable=True, name="kernel")

    def call(self, inputs):
        # Apply polynomial transformation to kernel
        kernel = tf.tensordot(self.kernel, self.transform, axes=[[4], [0]])
        kernel = tf.transpose(kernel, perm=[4, 2, 3, 0, 1])
        # Perform convolution with transformed kernel
        if self.groups > 1:
            # The '_jit_compiled_convolution_op' is a specialized operation that efficiently
            # handles grouped convolutions, addressing limitations in some TensorFlow versions
            # where grouped convolutions are not directly supported.
            conv_output = self._jit_compiled_convolution_op(inputs, kernel)
        else:
            conv_output = self.convolution_op(inputs, kernel)
        if self.use_bias:
            conv_output = tf.nn.bias_add(conv_output, self.bias)
        return conv_output

    def get_config(self):
        config = super().get_config()
        config.update({
            'degrees': self.degrees,
            'alpha': self.alpha,
            'beta': self.beta
        })
        return config
