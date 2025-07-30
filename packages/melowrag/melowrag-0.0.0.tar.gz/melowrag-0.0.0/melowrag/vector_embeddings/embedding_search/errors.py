"""
This module provides the IndexNotFoundError exception for missing embedding indexes during queries.
"""


class IndexNotFoundError(Exception):
    """
    Exception raised when an embeddings query fails to locate an index.
    """
