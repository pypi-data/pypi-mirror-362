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
