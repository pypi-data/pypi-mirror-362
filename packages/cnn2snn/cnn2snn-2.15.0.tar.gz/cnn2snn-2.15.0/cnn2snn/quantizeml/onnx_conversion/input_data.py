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
__all__ = ["InputDataOnnxConverter"]

import akida

from .base_converter import OnnxConverter
from .register import register_onnx_converter_target


def get_next_neighbor_nodes(node, graph):
    # Get the nodes connected to the outputs
    outbounds = []
    for target_node in graph.node:
        for target_input in target_node.input:
            if target_input in node.output:
                outbounds.append(target_node)
    return outbounds


@register_onnx_converter_target("InputQuantizer")
class InputDataOnnxConverter(OnnxConverter):
    """Convert InputData node into an akida.InputData.

    Args:
        node (NodeProto): the node to convert.
        model (ModelProto): the model that the node is.
    """
    @property
    def is_input_layer(self):
        return True

    @property
    def input_name(self):
        return self._node.output[0]

    @property
    def func(self):
        return None

    def load_attributes(self, node):
        self.input_bits = 8

    def _additional_checks(self):
        assert len(self._node.output) == 1, "InputData must have exactly one output."
        # Check input data is connected to only one node
        outbound_nodes = get_next_neighbor_nodes(self._node, self._model.graph)
        if len(outbound_nodes) != 1:
            raise RuntimeError(f"{self.name} must be connected to only one node.")

    def _parse_akida_layer(self):
        return akida.InputData(input_shape=self.input_shape,
                               input_bits=self.input_bits,
                               name=self.name)

    def _set_akida_variables(self, ak_layer):
        # Nothing to do
        ...
