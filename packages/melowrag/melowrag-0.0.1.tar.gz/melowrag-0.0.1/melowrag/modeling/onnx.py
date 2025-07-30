# Copyright 2025 The MelowRAG Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import onnxruntime as ort

    ONNX_RUNTIME = True
except ImportError:
    ONNX_RUNTIME = False

import numpy as np
import torch
from transformers import AutoConfig
from transformers.configuration_utils import PretrainedConfig
from transformers.modeling_outputs import SequenceClassifierOutput
from transformers.modeling_utils import PreTrainedModel

from .registry import Registry


# pylint: disable=W0223
class OnnxModel(PreTrainedModel):
    """
    Provides a Transformers/PyTorch compatible interface for ONNX models. Handles casting inputs
    and outputs with minimal to no copying of data.
    """

    def __init__(self, model, config=None):
        """
        Creates a new OnnxModel.

        Args:
            model: path to model or InferenceSession
            config: path to model configuration
        """

        if not ONNX_RUNTIME:
            raise ImportError('onnxruntime is not available - install "model" extra to enable')

        super().__init__(AutoConfig.from_pretrained(config) if config else OnnxConfig())

        self.model = ort.InferenceSession(model, ort.SessionOptions(), self.providers())

        Registry.register(self)

    @property
    def device(self):
        """
        Returns model device id.

        Returns:
            model device id
        """

        return -1

    def providers(self):
        """
        Returns a list of available and usable providers.

        Returns:
            list of available and usable providers
        """

        if torch.cuda.is_available() and "CUDAExecutionProvider" in ort.get_available_providers():
            return ["CUDAExecutionProvider", "CPUExecutionProvider"]

        return ["CPUExecutionProvider"]

    def forward(self, **inputs):
        """
        Runs inputs through an ONNX model and returns outputs. This method handles casting inputs
        and outputs between torch tensors and numpy arrays as shared memory (no copy).

        Args:
            inputs: model inputs

        Returns:
            model outputs
        """

        inputs = self.parse(inputs)

        results = self.model.run(None, inputs)

        # pylint: disable=E1101
        if any(x.name for x in self.model.get_outputs() if x.name == "logits"):
            return SequenceClassifierOutput(logits=torch.from_numpy(np.array(results[0])))

        return torch.from_numpy(np.array(results))

    def parse(self, inputs):
        """
        Parse model inputs and handle converting to ONNX compatible inputs.

        Args:
            inputs: model inputs

        Returns:
            ONNX compatible model inputs
        """

        features = {}

        for key in ["input_ids", "attention_mask", "token_type_ids"]:
            if key in inputs:
                value = inputs[key]

                if hasattr(value, "cpu"):
                    value = value.cpu().numpy()

                features[key] = np.asarray(value)

        return features


class OnnxConfig(PretrainedConfig):
    """
    Configuration for ONNX models.
    """
