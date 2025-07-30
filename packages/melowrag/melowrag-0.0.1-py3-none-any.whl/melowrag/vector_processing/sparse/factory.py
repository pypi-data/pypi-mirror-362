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

from ...utilities import Resolver
from .sbert import SparseSTVectors


class SparseVectorsFactory:
    """
    Methods to create sparse vector models.
    """

    @staticmethod
    def create(config, models=None):
        """
        Create a Vectors model instance.

        Args:
            config: vector configuration
            models: models cache

        Returns:
            Vectors
        """

        method = config.get("method", "sentence-transformers")

        if method == "sentence-transformers":
            return SparseSTVectors(config, None, models) if config and config.get("path") else None

        return SparseVectorsFactory.resolve(method, config, models) if method else None

    @staticmethod
    def resolve(backend, config, models):
        """
        Attempt to resolve a custom backend.

        Args:
            backend: backend class
            config: vector configuration
            models: models cache

        Returns:
            Vectors
        """

        try:
            return Resolver()(backend)(config, None, models)
        except Exception as e:
            raise ImportError(f"Unable to resolve sparse vectors backend: '{backend}'") from e
