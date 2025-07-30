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
__all__ = ["DequantizerOnnxConverter"]

import akida

from .base_converter import OnnxConverter
from .weights import broadcast_and_set_variable
from .register import register_onnx_converter_target


@register_onnx_converter_target("Dequantizer")
class DequantizerOnnxConverter(OnnxConverter):
    """Convert Dequantizer node into an akida.Dequantizer.

    Args:
        node (NodeProto): the node to convert.
        model (ModelProto): the model that the node is.
    """

    def _additional_checks(self):
        # Num inputs in onnx node may be weights + one input
        if len(self._node.input) != len(self.weights) + 1:
            raise RuntimeError(f"Multi-inbounds in {self.name} is not supported.")

    def _parse_akida_layer(self):
        return akida.Dequantizer(name=self.name)

    def _set_akida_variables(self, ak_layer):
        broadcast_and_set_variable(ak_layer.variables, "scales", self.weights["scale"])
