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
__all__ = ["set_output_scale_variables"]

import numpy as np

from .weights import broadcast_and_set_variable


def set_output_scale_variables(ak_layer, scale=1, shift=1, prefix='output'):
    """Set output scale into akida variables.

    Args:
        ak_layer (akida.Layer): the akida layer to set variables.
        scale (np.ndarray): the scale. Defaults to 1.
        shift (np.ndarray): the power of two that represent the shift. Defaults to 1.
        prefix (str, optional): the akida variable prefix. Defaults to 'output'.
    """
    scale_name = f"{prefix}_scales"
    if scale_name in ak_layer.variables.names:
        broadcast_and_set_variable(ak_layer.variables, scale_name, scale)

    # Shift integrity check
    ak_shift = np.array(np.round(np.log2(shift)), "int8")
    if np.any(2.0**ak_shift != shift) or np.any(shift == 0):
        raise ValueError(f"Error found when setting shift in {ak_layer.name}:",
                         f"{shift} is not a power of two.")

    # In akida, shift is applied as left shift (when positive) or right shift (otherwise).
    # However, in onnx scale out, shift was performed through one division.
    # It explains the minus sign.
    broadcast_and_set_variable(ak_layer.variables, f"{prefix}_shift", -ak_shift)
