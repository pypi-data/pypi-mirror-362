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
