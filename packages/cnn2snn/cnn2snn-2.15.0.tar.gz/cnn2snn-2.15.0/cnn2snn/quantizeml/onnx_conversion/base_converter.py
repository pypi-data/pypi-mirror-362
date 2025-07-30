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
__all__ = ["OnnxConverter"]

import numpy as np

from onnxruntime.quantization.quant_utils import find_by_name
from quantizeml.onnx_support.layers.base_layer import BRN_OPSET

from . import onnx_graph_tools
from .layer_bounds import get_inbound_layers
from .weights import load_weights


def get_akida_input_model_shape(onnx_graph):
    shape = onnx_graph_tools.get_tensor_shape(onnx_graph.input[0])
    # Remove batch size as akida requires a 3D input shape
    akida_shape = shape[1:]
    if len(akida_shape) > 1:
        # Convert to channels last
        akida_shape = akida_shape[1:] + akida_shape[0:1]
    # Expand to have exactly three dimensions
    akida_shape = np.insert(akida_shape, [0] * (3 - len(akida_shape)), 1)
    return akida_shape


class OnnxConverter:
    """Abstract class that allows to convert a node into the corresponding Akida layer.

    Child should overwrite _additional_checks function (if extra checks are required)
    and implement convert() function.

    Args:
        node (NodeProto): the node to convert.
        model (ModelProto): the model that has the node in it.
    """

    def __init__(self, node, model):
        if node.domain != BRN_OPSET.domain:
            raise ValueError(f"Unrecognized {node.name}: it is not part of the domain.")
        self._node = node
        self._model = model
        self._input_shape = None

        # Parse attributes and weights from node (and initializer) into class
        self.weights = load_weights(node, model.graph.initializer, self.func)
        self.load_attributes(node)

        # Check special rules
        self._additional_checks()

    @property
    def name(self):
        return self._node.name

    @property
    def input_name(self):
        return self._node.input[0]

    @property
    def input_shape(self):
        if self.is_input_layer:
            return get_akida_input_model_shape(self._model.graph)
        assert self._input_shape is not None
        return self._input_shape

    @property
    def is_input_layer(self):
        # Default to False
        return False

    @property
    def func(self):
        func = find_by_name(self._node.op_type, self._model.functions)
        assert func, f"{self.name} does not have an associated function."
        return func

    def load_attributes(self, node):
        """Load node attributes into object.

        Args:
            node (NodeProto): the input node.
        """
        for attr in node.attribute:
            # Get attribute value
            value = onnx_graph_tools.get_field(node, attr.name)
            # Set value into class as an attribute
            setattr(self, attr.name, value)

    def _additional_checks(self):
        """Check node compatibility with Akida."""
        ...

    def _parse_akida_layer(self):
        raise NotImplementedError("Child must implement this function")

    def _set_akida_variables(self, ak_layer):
        raise NotImplementedError("Child must implement this function")

    def convert(self, ak_model):
        """Convert node into an Akida layer and append it into the model.

        Args:
            ak_model (akida.Model): the target Akida model.
        """
        if len(ak_model.layers) > 0 and self.is_input_layer:
            raise RuntimeError(f"Impossible to convert {self.name} into akida. "
                               "There can be no layers prior to it.")
        if len(ak_model.layers) == 0 and not self.is_input_layer:
            raise RuntimeError(f"Impossible to convert {self.name} into akida. "
                               "This node require an InputData.")

        # Retrieve the akida inbound layers
        inbound_layers_ak = get_inbound_layers(ak_model, self._node, self._model.graph)

        # Assign input shape
        input_shape = [x.output_dims for x in inbound_layers_ak]
        if len(input_shape) == 1:
            input_shape = input_shape[0]
        self._input_shape = input_shape

        # Declare akida layer to set variables
        ak_layer = self._parse_akida_layer()

        # Append new layer in akida mode
        ak_model.add(ak_layer, inbound_layers_ak)

        # Align akida layer name with convert one
        self._node.name = ak_layer.name

        # Set weights into akida layer
        try:
            self._set_akida_variables(ak_layer)
        except Exception as e:
            raise type(e)(f"Impossible to transfer variable in {self.name}. \nReason: " + str(e))
