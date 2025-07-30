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

from ...modeling import Models, PoolingFactory
from ..base import Vectors


class HFVectors(Vectors):
    """
    Builds vectors using the Hugging Face transformers library.
    """

    @staticmethod
    def ismethod(method):
        """
        Checks if this method uses local transformers-based models.

        Args:
            method: input method

        Returns:
            True if this is a local transformers-based model, False otherwise
        """

        return method in ("transformers", "pooling", "clspooling", "meanpooling")

    def loadmodel(self, path):
        return PoolingFactory.create(
            {
                "method": self.config.get("method"),
                "path": path,
                "device": Models.deviceid(self.config.get("gpu", True)),
                "tokenizer": self.config.get("tokenizer"),
                "maxlength": self.config.get("maxlength"),
                "modelargs": self.config.get("vectors", {}),
            }
        )

    def encode(self, data, category=None):
        return self.model.encode(data, batch=self.encodebatch)
