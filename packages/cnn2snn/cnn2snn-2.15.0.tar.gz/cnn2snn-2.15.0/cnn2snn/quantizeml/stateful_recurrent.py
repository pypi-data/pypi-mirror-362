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
"""Functions to convert QuantizedStatefulRecurrent to Akida.
"""
from akida import StatefulRecurrentLegacy, ActivationType
import quantizeml.layers as qlayers
import numpy as np

from .weights import broadcast_and_set_variable
from .outputs import set_output_v2_variables, parse_output_bits, parse_post_op_buffer_bits
from .block_converter import BlockConverter
from .blocks import get_block_out_quantizer
from .activations import set_relu_variables
from .conv_common import get_layer_by_type
from .layer_utils import get_inbound_layers

__all__ = ["StatefulRecurrentBlockConverter"]

_PATTERNS = [(qlayers.QuantizedDense, qlayers.QuantizedStatefulRecurrent,
              qlayers.QuantizedExtractToken, qlayers.QuantizedDense, qlayers.QuantizedReLU),
             (qlayers.QuantizedDense, qlayers.QuantizedStatefulRecurrent,
              qlayers.QuantizedExtractToken, qlayers.QuantizedDense)]


def _set_stateful_recurrent_variables(ak_layer, block):
    """Computes and sets the variables for an Akida StatefulRecurrentLegacy layer.

    This function converts the variables of a Keras layer and sets them into
    the corresponding variables of the equivalent Akida layer.

    Args:
        ak_layer (:obj:`akida.Layer`): the targeted akida layer.
        block (list(:obj:`tf.keras.Layer`)): the block of keras layers.
    """
    variables_ak = ak_layer.variables

    in_proj_dense = block[0]
    stateful_rec = block[1]
    out_proj_dense = block[3]

    assert isinstance(in_proj_dense.weight_quantizer, qlayers.WeightQuantizer)
    assert isinstance(out_proj_dense.weight_quantizer, qlayers.WeightQuantizer)
    assert isinstance(stateful_rec.a_quantizer, qlayers.WeightQuantizer)

    # Set StatefulRecurrentLegacy input_shift
    input_shift = getattr(in_proj_dense, 'input_shift', None)
    if input_shift is not None:
        broadcast_and_set_variable(variables_ak, "input_shift",
                                   input_shift.value.numpy().astype(np.uint8))
    # Set input_projection dense kernel
    in_proj_ak = in_proj_dense.weight_quantizer.qweights.value.fp.values.numpy()
    variables_ak["in_proj"] = in_proj_ak.astype(np.int8)

    # Set intermediate input_proj scale_out scale variable
    if hasattr(in_proj_dense.out_quantizer, 'qscales'):
        scales = in_proj_dense.out_quantizer.qscales.value.values
        output_scales = scales.numpy().astype(np.uint8)
        broadcast_and_set_variable(variables_ak, "in_proj_outputs_scales", output_scales)

    # Set intermediate input_proj scale_out shift variable.
    # Note that it's merged with the StatefulRecurrentLegacy input shifts variables.
    stateful_inputs_shift_ak = 0
    stateful_inputs_shift = getattr(stateful_rec, 'input_shift', None)
    if stateful_inputs_shift is not None:
        stateful_inputs_shift_ak = stateful_inputs_shift.value.numpy()
    stateful_inputs_shift_ak += stateful_rec.input_add_shift.value.numpy()
    stateful_inputs_shift_ak += in_proj_dense.out_quantizer.shift.value.numpy()
    broadcast_and_set_variable(variables_ak, "input_proj_to_stateful_shift",
                               stateful_inputs_shift_ak.astype(np.int8))

    # Set A weights variables
    A_real_ak = stateful_rec.a_quantizer(stateful_rec.A_real).values.numpy()
    variables_ak["A_real"] = A_real_ak.astype(np.int16)
    A_imag_ak = stateful_rec.a_quantizer(stateful_rec.A_imag).values.numpy()
    variables_ak["A_imag"] = A_imag_ak.astype(np.int16)

    # Set intermediate stateful_outputs_shift
    internal_state_shift = stateful_rec.out_quantizer.shift.value[0]
    assert np.all(internal_state_shift <= 0), "shift values should be negative"
    broadcast_and_set_variable(variables_ak, "internal_state_outputs_shift",
                               np.abs(internal_state_shift.numpy()).astype(np.uint8))

    # Set out_proj dense kernel variable
    out_proj_ak = out_proj_dense.weight_quantizer.qweights.value.fp.values.numpy()
    variables_ak["out_proj"] = out_proj_ak.astype(np.int8)

    if out_proj_dense.use_bias:
        bias_quantizer = out_proj_dense.bias_quantizer
        assert isinstance(bias_quantizer, qlayers.AlignedWeightQuantizer)
        # Set StatefuRecurrent layer bias variable and shift
        bias = bias_quantizer.qweights.value.values.numpy().astype(np.int32)
        bias_shift = bias_quantizer.shift.value.numpy().astype(np.uint8)
        variables_ak["bias"] = (bias >> bias_shift).astype(np.int8)
        broadcast_and_set_variable(variables_ak, "bias_shift", bias_shift)

    # Check if we have ReLU
    relu_layer = get_layer_by_type(block, qlayers.QuantizedReLU)
    if relu_layer:
        # Set ReLU variables
        set_relu_variables(ak_layer, relu_layer)

    out_quantizer = get_block_out_quantizer(block)
    if out_quantizer:
        set_output_v2_variables(ak_layer, out_quantizer)


def _create_stateful_recurrent(block):
    """Parses a quantizeml quantized StatefulRecurrent layers block and returns the
    params to create the corresponding Akida StatefulRecurrentLegacy layer.

    Args:
        block (list(:obj:`tf.keras.Layer`)): list of quantizeml quantized layers.

    Returns:
        :obj:`akida.StatefulRecurrentLegacy`: The created akida layer.
    """
    input_proj_dense = block[0]
    stateful_rec = block[1]
    out_proj_dense = block[3]
    if out_proj_dense.buffer_bitwidth != block[0].buffer_bitwidth:
        raise ValueError("in_proj and out_proj should have the same buffer_bitwidth")
    relu_layer = get_layer_by_type(block, qlayers.QuantizedReLU)
    # In quantizeml one bit is reserved automatically for the sign, but in
    # akida this is rather checked during the clipping operations.
    activation = ActivationType.ReLU if relu_layer else ActivationType.NoActivation
    block_params = {"buffer_bits": out_proj_dense.buffer_bitwidth + 1,
                    "stateful_buffer_bits": stateful_rec.buffer_bitwidth + 1,
                    "subsample_ratio": stateful_rec.subsample_ratio,
                    "stateful_channels": input_proj_dense.units,
                    "out_channels": out_proj_dense.units,
                    "activation": activation}

    # parse the block output bits
    parse_output_bits(block, block_params)
    # parse the block post op buffer bits
    parse_post_op_buffer_bits(block, block_params)

    return StatefulRecurrentLegacy(**block_params, name=out_proj_dense.name)


def convert_quantized_statefulrec(model_ak, block):
    """Converts QuantizedLayerStatefulRecurrent layers block and its variables and adds
    it to the Akida's model.

    Args:
        model_ak (:obj:`akida.Model`): the Akida model where the model will be added.
        block (list(:obj:`tf.keras.Layer`)): list of quantizeml quantized layers.

    Returns:
        bool: Returns True for a successful conversion.
    """
    # Retrieve the akida inbound layers
    inbound_layers_ak = get_inbound_layers(model_ak, block[0])
    # Create and add layer to the akida model
    layer_ak = _create_stateful_recurrent(block)
    model_ak.add(layer_ak, inbound_layers_ak)
    # Set the akida layer converted variables
    _set_stateful_recurrent_variables(layer_ak, block)
    return True


class StatefulRecurrentBlockConverter(BlockConverter):
    """Main class that should be used to check if the stateful recurrent layer block is compatible
    to an Akida v2 conversion and provides a method to convert it in an equivalent Akida v2
    StatefulRecurrent layer.

    Args:
        block (list): list of quantizeml quantized layers.
    """

    def convert(self, model_ak):
        return convert_quantized_statefulrec(model_ak, self._block)


# Register the valid stateful recurrent block pattern for Akida v2
# TODO: disabled while the StatefulRecurrent definition is being updated
# register_conversion_patterns(AkidaVersion.v2, _PATTERNS, StatefulRecurrentBlockConverter)
