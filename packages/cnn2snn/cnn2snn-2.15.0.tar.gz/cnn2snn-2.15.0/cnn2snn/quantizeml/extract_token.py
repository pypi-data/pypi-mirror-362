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
"""Functions to convert QuantizedExtractToken to Akida.
"""
from akida import ExtractToken
import quantizeml.layers as qlayers

from .layer_utils import get_inbound_layers
from .block_converter import BlockConverter, register_conversion_patterns
from ..akida_versions import AkidaVersion


__all__ = ["ExtractTokenBlockConverter"]

_PATTERNS = [(qlayers.QuantizedExtractToken,)]


def _get_layer_token_range(layer):
    """Helper to extract the layer token range.

    Args:
        layer (:obj:`tf.keras.Layer`): the quantizeml QuantizedExtractToken layer.

    Returns:
        tuple, list: token range of the layer in the following format ((begin, end), token_range).
    """
    assert isinstance(layer, qlayers.QuantizedExtractToken)
    # Akida is capable of supporting only a given combination of token
    if isinstance(layer.token, int):
        token_range = [layer.token]
    else:
        token_range = [*layer.token]
    begin = min(token_range)
    end = max(token_range) + 1

    return (begin, end), token_range


def _create_extract_token(block):
    """Parses a quantizeml QuantizedExtractToken layer and returns the
    params to create the corresponding Akida v2 ExtractToken layer.

    Args:
        block (list(:obj:`tf.keras.Layer`)): the block of keras layers.

    Returns:
        :obj:`akida.ExtractToken`: The created akida layer.
    """
    (begin, end), _ = _get_layer_token_range(block[0])

    extract_token = ExtractToken(begin=begin,
                                 end=end,
                                 name=block[0].name)
    return extract_token


def convert_extract_token(model_ak, block):
    """Converts QuantizedExtractToken layer and adds it to the Akida's model.

    Args:
        model_ak (:obj:`akida.Model`): the Akida model where the model will be
            added.
        block (list(:obj:`tf.keras.Layer`)): the block of keras layers.

    Returns:
        bool: Returns True for a successful conversion.
    """

    # Retrieve the akida inbound layers
    inbound_layers_ak = get_inbound_layers(model_ak, block[0])
    # Create and add layer to the akida model
    # It is quite simple because there are no variables or params to be set.
    layer_ak = _create_extract_token(block)
    model_ak.add(layer_ak, inbound_layers_ak)
    return True


class ExtractTokenBlockConverter(BlockConverter):
    """Main class that should be used to check if the extract token layer block is compatible to an
    Akida v2 conversion and provides a method to convert it in an equivalent Akida ExtractToken
    layer.

    Args:
        block (list): list of quantizeml quantized layers.
    """

    def __init__(self, block):
        super().__init__(block)
        self._extract_token_additional_checks()

    def _extract_token_additional_checks(self):
        layer = self._block[0]
        (begin, end), token_range = _get_layer_token_range(layer)
        # Check range is continuous
        continuous = sorted(token_range) == list(range(begin, end))
        if not continuous:
            raise ValueError(f"Argument token in {layer.name} should contain a "
                             "continuous range")

    def convert(self, model_ak):
        return convert_extract_token(model_ak, self._block)


# Register the valid extract token block pattern for Akida v2
register_conversion_patterns(AkidaVersion.v2, _PATTERNS, ExtractTokenBlockConverter)
