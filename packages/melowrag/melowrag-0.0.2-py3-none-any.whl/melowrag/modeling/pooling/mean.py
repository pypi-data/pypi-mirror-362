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

import torch

from .base import Pooling


class MeanPooling(Pooling):
    """
    Builds mean pooled vectors usings outputs from a transformers model.
    """

    def forward(self, **inputs):
        """
        Runs mean pooling on token embeddings taking the input mask into account.

        Args:
            inputs: model inputs

        Returns:
            mean pooled embeddings using output token embeddings (i.e. last hidden state)
        """

        tokens = super().forward(**inputs)
        mask = inputs["attention_mask"]

        # pylint: disable=E1101
        mask = mask.unsqueeze(-1).expand(tokens.size()).float()
        return torch.sum(tokens * mask, 1) / torch.clamp(mask.sum(1), min=1e-9)
