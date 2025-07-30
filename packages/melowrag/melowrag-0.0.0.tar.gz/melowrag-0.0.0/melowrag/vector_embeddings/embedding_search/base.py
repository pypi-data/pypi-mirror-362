"""
This module provides the Search class for executing batch search actions over embedding indexes and/or databases.
It supports dense, sparse, and hybrid search, as well as subindex and graph-based search.
"""

import logging
from collections import namedtuple

from .errors import IndexNotFoundError
from .scan import Scan

SearchResult = namedtuple("SearchResult", ["index", "score"])

logger = logging.getLogger(__name__)


class Search:
    """
    Executes batch search actions over embedding indexes and/or databases.

    The Search class supports dense, sparse, and hybrid search, as well as subindex and graph-based search.

    Args:
        embeddings (Embeddings): Embeddings instance to search over.
        indexids (bool, optional): If True, searches return index ids. Defaults to False.
        indexonly (bool, optional): If True, always runs an index search even when a database is available. Defaults to False.
    """

    def __init__(self, embeddings, indexids=False, indexonly=False):
        """
        Initializes a new Search action.

        Args:
            embeddings (Embeddings): Embeddings instance to search over.
            indexids (bool, optional): If True, searches return index ids. Defaults to False.
            indexonly (bool, optional): If True, always runs an index search even when a database is available. Defaults to False.
        """

        self.embeddings = embeddings
        self.indexids = indexids or indexonly
        self.indexonly = indexonly

        self.ann = embeddings.ann
        self.batchtransform = embeddings.batchtransform
        self.database = embeddings.database
        self.ids = embeddings.ids
        self.indexes = embeddings.indexes
        self.graph = embeddings.graph
        self.query = embeddings.query
        self.scoring = embeddings.scoring if embeddings.issparse() else None

    def __call__(self, queries, limit=None, weights=None, index=None, parameters=None):
        """
        Executes a batch search for queries.
        Runs either an index search or an index + database search depending on configuration and query.

        Args:
            queries (list): List of queries.
            limit (int, optional): Maximum number of results per query.
            weights (Any, optional): Hybrid score weights.
            index (str, optional): Index name.
            parameters (list, optional): List of dicts of named parameters to bind to placeholders.

        Returns:
            list: List of (id, score) per query for index search, list of dict per query for index + database search, or list of graph results for a graph index search.
        """

        limit = limit if limit else 3
        weights = weights if weights is not None else 0.5

        if not self.ann and not self.scoring and not self.indexes and not self.database:
            return [[]] * len(queries)

        if not index and not self.ann and not self.scoring and self.indexes:
            index = self.indexes.default()

        if self.graph and self.graph.isquery(queries):
            return self.graphsearch(queries, limit, weights, index)

        if not self.indexonly and self.database:
            return self.dbsearch(queries, limit, weights, index, parameters)

        return self.search(queries, limit, weights, index)

    def search(self, queries, limit, weights, index):
        """
        Executes an index search. When only a sparse index is enabled, this is a a keyword search. When only
        a dense index is enabled, this is an ann search. When both are enabled, this is a hybrid search.

        This method will also query subindexes, if available.

        Args:
            queries: list of queries
            limit: maximum results
            weights: hybrid score weights
            index: index name

        Returns:
            list of (id, score) per query
        """

        if index:
            return self.subindex(queries, limit, weights, index)

        hybrid = self.ann and self.scoring
        dense = self.dense(queries, limit * 10 if hybrid else limit) if self.ann else None
        sparse = self.sparse(queries, limit * 10 if hybrid else limit) if self.scoring else None

        if hybrid:
            if isinstance(weights, int | float):
                weights = [weights, 1 - weights]

            results = []
            for vectors in zip(dense, sparse, strict=False):
                uids = {}
                for v, scores in enumerate(vectors):
                    for r, (uid, score) in enumerate(scores if weights[v] > 0 else []):
                        if uid not in uids:
                            uids[uid] = 0.0

                        if self.scoring.isnormalized():
                            uids[uid] += score * weights[v]
                        else:
                            uids[uid] += (1.0 / (r + 1)) * weights[v]

                results.append(
                    [
                        SearchResult(index=uid, score=score)
                        for uid, score in sorted(uids.items(), key=lambda x: x[1], reverse=True)[:limit]
                    ]
                )

            return results

        if not sparse and not dense:
            raise IndexNotFoundError("No indexes available")

        # Convert (index, score) tuples to SearchResult namedtuples
        result_set = dense if dense else sparse
        return [[SearchResult(index=uid, score=score) for uid, score in r] for r in result_set]

    def subindex(self, queries, limit, weights, index):
        """
        Executes a subindex search.

        Args:
            queries: list of queries
            limit: maximum results
            weights: hybrid score weights
            index: index name

        Returns:
            list of (id, score) per query
        """

        if not self.indexes or index not in self.indexes:
            raise IndexNotFoundError(f"Index '{index}' not found")

        results = self.indexes[index].batchsearch(queries, limit, weights)
        return self.resolve(results)

    def dense(self, queries, limit):
        """
        Executes an dense vector search with an approximate nearest neighbor index.

        Args:
            queries: list of queries
            limit: maximum results

        Returns:
            list of (id, score) per query
        """

        embeddings = self.batchtransform((None, query, None) for query in queries)

        results = self.ann.search(embeddings, limit)

        results = [[(i, score) for i, score in r if score > 0] for r in results]

        return self.resolve(results)

    def sparse(self, queries, limit):
        """
        Executes a sparse vector search with a term frequency sparse array.

        Args:
            queries: list of queries
            limit: maximum results

        Returns:
            list of (id, score) per query
        """

        return self.resolve(self.scoring.batchsearch(queries, limit))

    def resolve(self, results):
        """
        Resolves index ids. This is only executed when content is disabled.

        Args:
            results: results

        Returns:
            results with resolved ids
        """

        if not self.indexids and self.ids:
            return [[SearchResult(index=self.ids[i], score=score) for i, score in r] for r in results]

        return results

    def dbsearch(self, queries, limit, weights, index, parameters):
        """
        Executes an index + database search.

        Args:
            queries: list of queries
            limit: maximum results
            weights: default hybrid score weights
            index: default index name
            parameters: list of dicts of named parameters to bind to placeholders

        Returns:
            list of dict per query
        """

        queries = self.parse(queries)

        limit = max(limit, self.limit(queries))

        scan = Scan(self.search, limit, weights, index)(queries, parameters)

        results = []
        for x, query in enumerate(queries):
            result = self.database.search(
                query,
                [r for y, r in scan if x == y],
                limit,
                parameters[x] if parameters and parameters[x] else None,
                self.indexids,
            )
            results.append(result)

        return results

    def parse(self, queries):
        """
        Parses a list of database queries.

        Args:
            queries: list of queries

        Returns:
            parsed queries
        """

        parsed = []

        for query in queries:
            parse = self.database.parse(query)

            if self.query and "select" not in parse:
                query = self.query(query)
                logger.debug(query)

                parse = self.database.parse(query)

            parsed.append(parse)

        return parsed

    def limit(self, queries):
        """
        Parses the largest LIMIT clause from queries.

        Args:
            queries: list of queries

        Returns:
            largest limit number or 0 if not found
        """

        qlimit = 0
        for query in queries:
            le = query.get("limit")
            if le and le.isdigit():
                le = int(le)

            qlimit = le if le and le > qlimit else qlimit

        return qlimit

    def graphsearch(self, queries, limit, weights, index):
        """
        Executes an index + graph search.

        Args:
            queries: list of queries
            limit: maximum results
            weights: default hybrid score weights
            index: default index name

        Returns:
            graph search results
        """

        queries = [self.graph.parse(query) for query in queries]

        limit = max(limit, self.limit(queries))

        scan = Scan(self.search, limit, weights, index)(queries, None)

        for x, query in enumerate(queries):
            query["results"] = [r for y, r in scan if x == y]

        return self.graph.batchsearch(queries, limit, self.indexids)
