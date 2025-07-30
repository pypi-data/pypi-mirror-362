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

import numpy as np

try:
    import litellm as api

    LITELLM = True
except ImportError:
    LITELLM = False

from ..base import Vectors


class LiteLLM(Vectors):
    """
    Builds vectors using an external embeddings API via LiteLLM.
    """

    @staticmethod
    def ismodel(path):
        """
        Checks if path is a LiteLLM model.

        Args:
            path: input path

        Returns:
            True if this is a LiteLLM model, False otherwise
        """

        # pylint: disable=W0702
        if isinstance(path, str) and LITELLM:
            debug = api.suppress_debug_info
            try:
                api.suppress_debug_info = True
                return api.get_llm_provider(path)
            except Exception:
                return False
            finally:
                api.suppress_debug_info = debug

        return False

    def __init__(self, config, scoring, models):
        if not LITELLM:
            raise ImportError('LiteLLM is not available - install "vectors" extra to enable')

        super().__init__(config, scoring, models)

    def loadmodel(self, path):
        return None

    def encode(self, data, category=None):
        response = api.embedding(model=self.config.get("path"), input=data, **self.config.get("vectors", {}))

        return np.array([x["embedding"] for x in response.data], dtype=np.float32)
