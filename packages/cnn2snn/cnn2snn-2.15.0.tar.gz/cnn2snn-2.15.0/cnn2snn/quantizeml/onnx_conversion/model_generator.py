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
__all__ = ["generate_onnx_model"]
import warnings

from onnx.utils import Extractor
from onnx.helper import make_node
from onnx.checker import check_model
from copy import deepcopy

import akida

from .base_converter import BRN_OPSET
from .register import map_node_to_converter


def get_convertible_model(model):
    """Return the candidated model to be converted.

    Args:
        model (ModelProto): the model to convert.

    Returns:
        ModelProto: the model to be converted.
    """
    extractor = Extractor(model)

    # Extract submodel from InputQuantizer output until Dequantizer output
    input_names = [x.name for x in model.graph.input]
    output_names = [x.name for x in model.graph.output]
    if len(model.graph.node) > 0 and model.graph.node[0].op_type == "InputQuantizer":
        input_names = model.graph.node[0].output
    min_num_layers = 1
    for idx, node in enumerate(model.graph.node):
        if node.op_type == "Dequantizer":
            output_names = node.output
            min_num_layers = 2
            break
    model_to_convert = extractor.extract_model(input_names, output_names)

    # Check model is not empty (at least one node to convert is required)
    if len(model_to_convert.graph.node) < min_num_layers:
        raise ValueError("Model is empty or does not have any node to convert.")

    # Prints a warning message with a summary of the skipped nodes
    skip_nodes = model.graph.node[idx + 1:]
    if len(skip_nodes) > 0:
        stop_layer_msg = " at node " + model.graph.node[idx - 1].name if idx > 0 else ""
        skip_layers_summary = "___________________________________________________\n"
        skip_layers_summary += "Node (type)\n"
        skip_layers_summary += "===================================================\n"
        for node in skip_nodes:
            skip_layers_summary += node.name + " (" + node.op_type + ")\n"
        skip_layers_summary += "===================================================\n"
        warnings.warn("Conversion stops" + stop_layer_msg + " because of a dequantizer. "
                      "The end of the graph is ignored:\n" + skip_layers_summary)

    # Insert a fake InputQuantizer if first layer is not an input layer
    first_layer = map_node_to_converter(model_to_convert.graph.node[0], model_to_convert)
    if not first_layer.is_input_layer:
        fake_iq = make_node("InputQuantizer", [], input_names, domain=BRN_OPSET.domain)
        model_to_convert.graph.node.insert(0, fake_iq)

    return model_to_convert


def generate_onnx_model(model):
    """Generates an Akida model based on an ONNX quantizeml model.

    Args:
        model (obj:`onnx.ModelProto`): a ONNX model to convert.

    Returns:
        akida.Model: the generated Akida model.
    """
    # Clone model to keep the original intact
    model = deepcopy(model)

    # Model must be compatible with ONNX
    check_model(model, full_check=True)

    # Checks over model
    assert len(model.graph.input) == 1, "Unsupported mode: it must have exactly one input."
    assert len(model.graph.output) == 1, "Unsupported mode: it must have exactly one output."

    # Now create akida model and iterate nodes to convert each one in an akida layer.
    model = get_convertible_model(model)
    akida_model = akida.Model()
    for node in model.graph.node:
        converter = map_node_to_converter(node, model)
        converter.convert(akida_model)
    return akida_model
