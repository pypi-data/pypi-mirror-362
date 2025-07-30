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
"""Utility function to convert layer to akida.
"""

from quantizeml import layers as qlayers


def get_inbound_layers(ak_model, k_layer):
    """Returns a list of Akida layers in an Akida model that correspond to the inbound
    layers of a Keras layer. The list will be built by traversing the Keras model graph.

    Args:
        ak_model (:obj:`Model`): the model where to find the inbounds layers.
        k_layer (:obj:`tf.keras.Layer`): the source layer.

    Returns:
        :list: the inbounds layers names.
    """

    # The list of supported Keras layers not represented in Akida
    skippable_layers = (qlayers.QuantizedDropout, qlayers.QuantizedFlatten,
                        qlayers.QuantizedReshape, qlayers.QuantizedRescaling,
                        qlayers.QuantizedReLU, qlayers.QuantizedMaxPool2D,
                        qlayers.QuantizedGlobalAveragePooling2D,
                        qlayers.QuantizedActivation)

    # Get inbound layers names
    in_node = k_layer.inbound_nodes[0]
    inbound_layers = in_node.inbound_layers
    if not isinstance(inbound_layers, list):
        inbound_layers = [inbound_layers]
    non_skippable_inbounds = []
    for layer in inbound_layers:
        if type(layer) in skippable_layers:
            # All skippable layers have one inbound layer, so this can be
            # easily resolved.
            while type(layer) in skippable_layers:
                layer = layer.inbound_nodes[0].inbound_layers
        non_skippable_inbounds.append(layer)
    return [ak_model.get_layer(ly.name) for ly in non_skippable_inbounds]
