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
__all__ = ["get_akida_padding", "compute_conv_transpose_same_pads"]

import math
import akida
from quantizeml.onnx_support.layers.compute_shapes import compute_conv_output


def compute_conv_same_pads(input_shape, kernel_shape, strides):
    """Compute pads values.

    Args:
        input_shape (tuple of ints): the input shape.
        kernel_shape (tuple of ints): the convolutional kernel shape.
        strides (tuple of ints): the convolutional strides.

    Returns:
        tuple of ints: the pads to apply.
    """
    x, y = input_shape
    filter_x, filter_y = kernel_shape
    stride_x, stride_y = strides

    if x % stride_x == 0:
        pad_along_x = max(filter_x - stride_x, 0)
    else:
        pad_along_x = max(filter_x - (x % stride_x), 0)
    if y % stride_y == 0:
        pad_along_y = max(filter_y - stride_y, 0)
    else:
        pad_along_y = max(filter_y - (y % stride_y), 0)
    pad_y1 = pad_along_y // 2
    pad_y2 = pad_along_y - pad_y1
    pad_x1 = pad_along_x // 2
    pad_x2 = pad_along_x - pad_x1
    return [pad_x1, pad_y1, pad_x2, pad_y2]


def compute_conv_transpose_same_pads(kernel_shape, strides):
    """Compute pads values for conv transpose
    See https://onnx.ai/onnx/operators/onnx__ConvTranspose.html#summary
    The Akida "SAME" padding corresponds to "SAME_LOWER" in ONNX.

    Args:
        kernel_shape (list or tuple of ints): the convolutional kernel shape.
        strides (list or tuple of ints): the convolutional strides.

    Returns:
        list of ints: the pads to apply.
    """
    filter_x, filter_y = kernel_shape
    stride_x, stride_y = strides

    total_padding_x = max(filter_x - stride_x, 0)
    total_padding_y = max(filter_y - stride_y, 0)

    pad_x2 = math.ceil(total_padding_x / 2)
    pad_x1 = total_padding_x - pad_x2

    pad_y2 = math.ceil(total_padding_y / 2)
    pad_y1 = total_padding_y - pad_y2

    return [pad_x1, pad_y1, pad_x2, pad_y2]


def get_akida_padding(converter):
    """Returns the akida padding

    Args:
        converter (OnnxConverter): the converter to extract the padding.

    Returns:
        akida.Padding: the padding
    """
    # Check pads are compatible with akida.Padding.Same
    kernel_shapes = converter.weights["W"].shape[-2:]
    # Initially assume padding corresponds to akida.Padding.Same
    exp_pads = compute_conv_same_pads(converter.input_shape[:2], kernel_shapes, converter.strides)
    ak_padding = akida.Padding.Same
    # Pads in FC dimensions have to be zero
    fc_pads = converter.pads[:2] + converter.pads[4:6]
    if any(fc_pads):
        raise ValueError(f"Unrecognized {converter.pads} pads in {converter.name}.")
    # Compare if convolutional padding produces same behavior than Akida
    convert_pads = converter.pads[2:4] + converter.pads[6:]
    if convert_pads != exp_pads:
        if all(x == 0 for x in convert_pads):
            # Force ak_padding to Valid, because no padding is supported as Valid in akida HW
            ak_padding = akida.Padding.Valid
            exp_pads = [0] * 2 * len(kernel_shapes)
        else:
            raise ValueError(f"Expect pads {exp_pads} (found {convert_pads}) in {converter.name}.")

    # Compare if max pool padding produces same behavior than Akida
    if converter.pool_type == akida.PoolType.Max:
        # Calculate convolutional output shape
        out_shape = compute_conv_output(converter.input_shape[:2],
                                        kernel_shapes,
                                        converter.strides,
                                        convert_pads)
        if ak_padding == akida.Padding.Same:
            exp_pool_pads = compute_conv_same_pads(out_shape,
                                                   converter.pool_size,
                                                   converter.pool_strides)
            if converter.pool_pads != exp_pool_pads and all(x == 0 for x in exp_pads):
                # Mismatch when padding Same. Try once again with a valid one,
                # given in this condition both padding are exchangable.
                ak_padding = akida.Padding.Valid
            else:
                exp_pads = exp_pool_pads
        if converter.pool_pads != exp_pads:
            raise ValueError(f"Expect pads {exp_pads} (found {converter.pool_pads}) "
                             f"in {converter.name} maxpool.")

    return ak_padding
