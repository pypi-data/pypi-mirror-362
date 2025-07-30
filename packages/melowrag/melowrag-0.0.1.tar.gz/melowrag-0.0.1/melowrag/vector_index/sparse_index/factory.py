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
from .ivfsparse import IVFSparse
from .pgsparse import PGSparse


class SparseANNFactory:
    """
    Methods to create Sparse VectoreIndex indexes.
    """

    @staticmethod
    def create(config):
        """
        Create an Sparse VectoreIndex.

        Args:
            config: index configuration parameters

        Returns:
            Sparse VectoreIndex
        """

        ann = None
        backend = config.get("backend", "ivfsparse")

        if backend == "ivfsparse":
            ann = IVFSparse(config)
        elif backend == "pgsparse":
            ann = PGSparse(config)
        else:
            ann = SparseANNFactory.resolve(backend, config)

        config["backend"] = backend

        return ann

    @staticmethod
    def resolve(backend, config):
        """
        Attempt to resolve a custom backend.

        Args:
            backend: backend class
            config: index configuration parameters

        Returns:
            VectoreIndex
        """

        try:
            return Resolver()(backend)(config)
        except Exception as e:
            raise ImportError(f"Unable to resolve sparse ann backend: '{backend}'") from e
