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

from ..utilities import Resolver
from .bm25 import BM25
from .pgtext import PGText
from .sif import SIF
from .sparse import Sparse
from .tfidf import TFIDF


class ScoringFactory:
    """
    Methods to create Scoring indexes.
    """

    @staticmethod
    def create(config, models=None):
        """
        Factory method to construct a Scoring instance.

        Args:
            config: scoring configuration parameters
            models: models cache

        Returns:
            Scoring
        """

        scoring = None

        if isinstance(config, str):
            config = {"method": config}

        method = config.get("method", "bm25")

        if method == "bm25":
            scoring = BM25(config)
        elif method == "pgtext":
            scoring = PGText(config)
        elif method == "sif":
            scoring = SIF(config)
        elif method == "sparse":
            scoring = Sparse(config, models)
        elif method == "tfidf":
            scoring = TFIDF(config)
        else:
            scoring = ScoringFactory.resolve(method, config)

        config["method"] = method

        return scoring

    @staticmethod
    def issparse(config):
        """
        Checks if this scoring configuration builds a sparse index.

        Args:
            config: scoring configuration

        Returns:
            True if this config is for a sparse index
        """

        indexes = ["pgtext", "sparse"]

        return config and isinstance(config, dict) and (config.get("method") in indexes or config.get("terms"))

    @staticmethod
    def resolve(backend, config):
        """
        Attempt to resolve a custom backend.

        Args:
            backend: backend class
            config: index configuration parameters

        Returns:
            Scoring
        """

        try:
            return Resolver()(backend)(config)
        except Exception as e:
            raise ImportError(f"Unable to resolve scoring backend: '{backend}'") from e
