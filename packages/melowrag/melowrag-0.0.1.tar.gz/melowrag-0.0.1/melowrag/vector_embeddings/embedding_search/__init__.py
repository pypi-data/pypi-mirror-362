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

"""
embedding_search package provides classes for searching, explaining, scanning, and resolving queries and ids in embedding indexes.

Exports:
    - Search: Batch search actions over embedding indexes and/or databases.
    - Explain: Token importance analysis for queries.
    - Ids: Internal id resolution.
    - IndexNotFoundError: Exception for missing indexes.
    - Query: Query translation using transformer models.
    - Scan: Index scanning for query matches.
    - Terms: Query term extraction.
"""

from .base import Search
from .errors import IndexNotFoundError
from .explain import Explain
from .ids import Ids
from .query import Query
from .scan import Scan
from .terms import Terms

__all__ = ("Explain", "Ids", "IndexNotFoundError", "Query", "Scan", "Search", "Terms")
