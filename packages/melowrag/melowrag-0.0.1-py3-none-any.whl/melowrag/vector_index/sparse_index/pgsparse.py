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

import os

try:
    from pgvector import SparseVector
    from pgvector.sqlalchemy import SPARSEVEC

    PGSPARSE = True
except ImportError:
    PGSPARSE = False

from ..dense_index import PGVector


class PGSparse(PGVector):
    """
    Builds a Sparse VectoreIndex index backed by a Postgres database.
    """

    def __init__(self, config):
        if not PGSPARSE:
            raise ImportError('PGSparse is not available - install "ann" extra to enable')

        super().__init__(config)

        self.qbits = None

    def defaulttable(self):
        return "svectors"

    def url(self):
        return self.setting("url", os.environ.get("SCORING_URL", os.environ.get("ANN_URL")))

    def column(self):
        return SPARSEVEC(self.config["dimensions"]), "sparsevec_ip_ops"

    def prepare(self, data):
        return SparseVector(data)
