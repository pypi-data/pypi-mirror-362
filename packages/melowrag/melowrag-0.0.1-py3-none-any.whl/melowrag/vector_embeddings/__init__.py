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
vector_embeddings package provides classes and utilities for managing, indexing, and searching embeddings.

This package exposes the main Embeddings interface and related tools for embedding index management, search, and transformation.

Modules exported:
    - Embeddings: Main class for embedding management and search.
    - Action, AutoId, Configuration, Documents, Functions, Indexes, IndexIds, Reducer, Stream, Transform: Indexing and transformation utilities.
    - Explain, Ids, IndexNotFoundError, Query, Scan, Search, Terms: Search and query utilities.
"""

from .base import Embeddings
from .embedding_index import (
    Action,
    AutoId,
    Configuration,
    Documents,
    Functions,
    Indexes,
    IndexIds,
    Reducer,
    Stream,
    Transform,
)
from .embedding_search import Explain, Ids, IndexNotFoundError, Query, Scan, Search, Terms

__all__ = (
    "Action",
    "AutoId",
    "Configuration",
    "Documents",
    "Embeddings",
    "Explain",
    "Functions",
    "Ids",
    "IndexIds",
    "IndexNotFoundError",
    "Indexes",
    "Query",
    "Reducer",
    "Scan",
    "Search",
    "Stream",
    "Terms",
    "Transform",
)
