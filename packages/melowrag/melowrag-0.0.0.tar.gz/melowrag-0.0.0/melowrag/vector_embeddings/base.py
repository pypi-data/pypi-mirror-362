import json
import os
import tempfile

from ..compression import ArchiveFactory
from ..databases import DatabaseFactory
from ..graph_algorithms import GraphFactory
from ..remote_storage import CloudFactory
from ..score_functions import ScoringFactory
from ..vector_index import ANNFactory
from ..vector_processing import VectorsFactory
from .embedding_index import Action, Configuration, Functions, Indexes, IndexIds, Reducer, Stream, Transform
from .embedding_search import Explain, Ids, Query, Search, Terms
from .embedding_search.base import SearchResult

# pylint: disable=C0302,R0904
"""
This module provides the Embeddings class, which manages semantic search and vector indexing for text and other data.
It supports building, updating, searching, and maintaining embedding indexes using various backends and algorithms.
"""


class Embeddings:
    """
    Manages embeddings databases for semantic search and vector indexing.

    The Embeddings class transforms data into embedding vectors, builds and maintains indexes, and enables semantic search
    where similar concepts yield similar vectors. It supports dense and sparse vector models, multiple backends, and
    advanced features like upsert, reindex, and graph-based search.

    Attributes:
        config (dict): Embeddings configuration.
        models (Any): Optional models cache for sharing between embeddings.
        reducer, model, ann, ids, database, functions, graph, scoring, query, archive, indexes: Internal components for processing and indexing.
    """

    # pylint: disable = W0231
    def __init__(self, config=None, models=None, **kwargs):
        """
        Initializes a new Embeddings index.

        Embeddings indexes are thread-safe for read operations, but writes must be synchronized externally.

        Args:
            config (dict, optional): Embeddings configuration dictionary.
            models (Any, optional): Models cache for sharing between embeddings instances.
            **kwargs: Additional configuration parameters.
        """

        self.config = None
        self.reducer = None
        self.model = None
        self.ann = None
        self.ids = None
        self.database = None
        self.functions = None
        self.graph = None
        self.scoring = None
        self.query = None
        self.archive = None
        self.indexes = None
        self.models = models
        config = {**config, **kwargs} if config and kwargs else kwargs if kwargs else config
        self.configure(config)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def score(self, documents):
        """
        Builds a term weighting scoring index. Only used by word vector models.

        Args:
            documents (Iterable): Iterable of (id, data, tags), (id, data), or data.
        """

        if self.isweighted():
            self.scoring.index(Stream(self)(documents))

    def index(self, documents, reindex=False, checkpoint=None):
        """
        Builds an embeddings index, overwriting any existing index.

        Args:
            documents (Iterable): Iterable of (id, data, tags), (id, data), or data.
            reindex (bool, optional): If True, performs a reindex operation and skips database creation. Defaults to False.
            checkpoint (str, optional): Optional checkpoint directory to enable indexing restart.
        """

        self.initindex(reindex)

        transform = Transform(self, Action.REINDEX if reindex else Action.INDEX, checkpoint)
        stream = Stream(self, Action.REINDEX if reindex else Action.INDEX)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".npy") as buffer:
            ids, dimensions, embeddings = transform(stream(documents), buffer)
            if embeddings is not None:
                if self.config.get("pca"):
                    self.reducer = Reducer(embeddings, self.config["pca"])
                    self.reducer(embeddings)

                self.config["dimensions"] = dimensions

                self.ann = self.createann()

                self.ann.index(embeddings)

            if ids and not reindex and not self.database:
                self.ids = self.createids(ids)

        if self.issparse():
            self.scoring.index()

        if self.indexes:
            self.indexes.index()

        if self.graph:
            self.graph.index(Search(self, indexonly=True), Ids(self), self.batchsimilarity)

    def upsert(self, documents, checkpoint=None):
        """
        Runs an embeddings upsert operation. Appends new data or updates existing data in the index.
        If the index does not exist, performs a standard index operation.

        Args:
            documents (Iterable): Iterable of (id, data, tags), (id, data), or data.
            checkpoint (str, optional): Optional checkpoint directory to enable indexing restart.
        """

        if not self.count():
            self.index(documents, checkpoint=checkpoint)
            return

        transform = Transform(self, Action.UPSERT, checkpoint=checkpoint)
        stream = Stream(self, Action.UPSERT)

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".npy") as buffer:
            ids, _, embeddings = transform(stream(documents), buffer)
            if embeddings is not None:
                if self.reducer:
                    self.reducer(embeddings)

                self.ann.append(embeddings)

            if ids and not self.database:
                self.ids = self.createids(self.ids + ids)

        if self.issparse():
            self.scoring.upsert()

        if self.indexes:
            self.indexes.upsert()

        if self.graph:
            self.graph.upsert(Search(self, indexonly=True), Ids(self), self.batchsimilarity)

    def delete(self, ids):
        """
        Deletes entries from the embeddings index.

        Args:
            ids (List): List of ids to delete.

        Returns:
            List: List of ids that were deleted.
        """

        indices = []

        deletes = []

        if self.database:
            ids = self.database.ids(ids)

            indices = [i for i, _ in ids]
            deletes = sorted(set(uid for _, uid in ids))

            self.database.delete(deletes)
        elif self.ann or self.scoring:
            for uid in ids:
                indices.extend([index for index, value in enumerate(self.ids) if uid == value])

            for index in indices:
                deletes.append(self.ids[index])
                self.ids[index] = None

        if indices:
            if self.isdense():
                self.ann.delete(indices)

            if self.issparse():
                self.scoring.delete(indices)

            if self.indexes:
                self.indexes.delete(indices)

            if self.graph:
                self.graph.delete(indices)

        return deletes

    def reindex(self, config=None, function=None, **kwargs):
        """
        Recreates the embeddings index using a new configuration.
        Only works if document content storage is enabled.

        Args:
            config (dict, optional): New configuration for the embeddings index.
            function (Callable, optional): Optional function to prepare content for indexing.
            **kwargs: Additional configuration parameters.
        """

        if self.database:
            config = {**config, **kwargs} if config and kwargs else config if config else kwargs

            config["content"] = self.config["content"]
            if "objects" in self.config:
                config["objects"] = self.config["objects"]

            self.configure(config)

            if self.functions:
                self.functions.reset()

            if function:
                self.index(function(self.database.reindex(self.config)), True)
            else:
                self.index(self.database.reindex(self.config), True)

    def transform(self, document, category=None, index=None):
        """
        Transforms a document into an embeddings vector.

        Args:
            document (Any): Single document to transform (id, data, tags), (id, data), or data.
            category (str, optional): Category for instruction-based embeddings.
            index (str, optional): Index name, if applicable.

        Returns:
            Any: Embeddings vector for the document.
        """

        return self.batchtransform([document], category, index)[0]

    def batchtransform(self, documents, category=None, index=None):
        """
        Transforms multiple documents into embeddings vectors.

        Args:
            documents (Iterable): Iterable of (id, data, tags), (id, data), or data.
            category (str, optional): Category for instruction-based embeddings.
            index (str, optional): Index name, if applicable.

        Returns:
            Any: Embeddings vectors for the documents.
        """

        self.defaults()

        model = self.findmodel(index)

        embeddings = model.batchtransform(Stream(self)(documents), category)

        if self.reducer:
            self.reducer(embeddings)

        return embeddings

    def count(self):
        """
        Returns the total number of elements in this embeddings index.

        Returns:
            int: Number of elements in this embeddings index.
        """

        if self.ann:
            return self.ann.count()
        if self.scoring:
            return self.scoring.count()
        if self.database:
            return self.database.count()
        if self.ids:
            return len([uid for uid in self.ids if uid is not None])

        return 0

    def search(self, query, limit=None, weights=None, index=None, parameters=None, graph=False):
        """
        Finds documents most similar to the input query.
        Runs an index search, index + database search, or a graph search depending on configuration and query.

        Args:
            query (Any): Input query.
            limit (int, optional): Maximum number of results.
            weights (Any, optional): Hybrid score weights, if applicable.
            index (str, optional): Index name, if applicable.
            parameters (dict, optional): Named parameters to bind to placeholders.
            graph (bool, optional): If True, return graph results.

        Returns:
            list: List of (id, score) for index search, list of dict for index + database search, or graph if graph is True.
        """

        results = self.batchsearch([query], limit, weights, index, [parameters], graph)
        return results[0] if results else results

    def batchsearch(self, queries, limit=None, weights=None, index=None, parameters=None, graph=False):
        """
        Finds documents most similar to the input queries.
        Runs an index search, index + database search, or a graph search depending on configuration and query.

        Args:
            queries (Iterable): Input queries.
            limit (int, optional): Maximum number of results per query.
            weights (Any, optional): Hybrid score weights, if applicable.
            index (str, optional): Index name, if applicable.
            parameters (list, optional): List of dicts of named parameters to bind to placeholders.
            graph (bool, optional): If True, return graph results.

        Returns:
            list: List of (id, score) per query for index search, list of dict per query for index + database search, or list of graphs if graph is True.
        """

        graph = graph if self.graph else False

        results = Search(self, indexids=graph)(queries, limit, weights, index, parameters)

        return [self.graph.filter(x) if isinstance(x, list) else x for x in results] if graph else results

    def similarity(self, query, data):
        """
        Computes the similarity between query and list of data. Returns a list of
        SearchResult(index, score) sorted by highest score, where index is the index in data.

        Args:
            query: input query
            data: list of data

        Returns:
            list of SearchResult(index, score)
        """

        return self.batchsimilarity([query], data)[0]

    def batchsimilarity(self, queries, data):
        """
        Computes the similarity between list of queries and list of data. Returns a list
        of SearchResult(index, score) sorted by highest score per query, where index is the index in data.

        Args:
            queries: input queries
            data: list of data

        Returns:
            list of SearchResult(index, score) per query
        """

        queries = self.batchtransform(((None, query, None) for query in queries), "query")
        data = self.batchtransform(((None, row, None) for row in data), "data")

        model = self.findmodel()

        scores = model.dot(queries, data)

        return [
            [SearchResult(index=i, score=s) for i, s in sorted(enumerate(score), key=lambda x: x[1], reverse=True)]
            for score in scores
        ]

    def explain(self, query, texts=None, limit=None):
        """
        Explains the importance of each input token in text for a query. This method requires
        either content to be enabled or texts to be provided.

        Args:
            query: input query
            texts: optional list of (text|list of tokens), otherwise runs search query
            limit: optional limit if texts is None

        Returns:
            list of dict per input text where a higher token scores represents higher importance relative to the query
        """

        results = self.batchexplain([query], texts, limit)
        return results[0] if results else results

    def batchexplain(self, queries, texts=None, limit=None):
        """
        Explains the importance of each input token in text for a list of queries.
        This method requires either content to be enabled or texts to be provided.

        Args:
            queries: input queries
            texts: optional list of (text|list of tokens), otherwise runs search queries
            limit: optional limit if texts is None

        Returns:
            list of dict per input text per query where a higher token scores represents
            higher importance relative to the query
        """

        return Explain(self)(queries, texts, limit)

    def terms(self, query):
        """
        Extracts keyword terms from a query.

        Args:
            query: input query

        Returns:
            query reduced down to keyword terms
        """

        return self.batchterms([query])[0]

    def batchterms(self, queries):
        """
        Extracts keyword terms from a list of queries.

        Args:
            queries: list of queries

        Returns:
            list of queries reduced down to keyword term strings
        """

        return Terms(self)(queries)

    def exists(self, path=None, cloud=None, **kwargs):
        """
        Checks if an index exists at path.

        Args:
            path: input path
            cloud: cloud storage configuration
            kwargs: additional configuration as keyword args

        Returns:
            True if index exists, False otherwise
        """

        cloud = self.createcloud(cloud=cloud, **kwargs)
        if cloud:
            return cloud.exists(path)

        path, apath = self.checkarchive(path)
        if apath:
            return os.path.exists(apath)

        return (
            path
            and (os.path.exists(f"{path}/config.json") or os.path.exists(f"{path}/config"))
            and "offset" in Configuration().load(path)
        )

    def load(self, path=None, cloud=None, config=None, **kwargs):
        """
        Loads an existing index from path.

        Args:
            path: input path
            cloud: cloud storage configuration
            config: configuration overrides
            kwargs: additional configuration as keyword args

        Returns:
            Embeddings
        """

        cloud = self.createcloud(cloud=cloud, **kwargs)
        if cloud:
            path = cloud.load(path)

        path, apath = self.checkarchive(path)
        if apath:
            self.archive.load(apath)

        self.config = Configuration().load(path)

        self.config = {**self.config, **config} if config else self.config

        self.ann = self.createann()
        if self.ann:
            self.ann.load(f"{path}/embeddings")

        if self.config.get("pca"):
            self.reducer = Reducer()
            self.reducer.load(f"{path}/lsa")

        self.ids = self.createids()
        if self.ids:
            self.ids.load(f"{path}/ids")

        self.database = self.createdatabase()
        if self.database:
            self.database.load(f"{path}/documents")

        self.scoring = self.createscoring()
        if self.scoring:
            self.scoring.load(f"{path}/scoring")

        self.indexes = self.createindexes()
        if self.indexes:
            self.indexes.load(f"{path}/indexes")

        self.graph = self.creategraph()
        if self.graph:
            self.graph.load(f"{path}/graph")

        self.model = self.loadvectors()

        self.query = self.loadquery()

        return self

    def save(self, path, cloud=None, **kwargs):
        """
        Saves an index in a directory at path unless path ends with tar.gz, tar.bz2, tar.xz or zip.
        In those cases, the index is stored as a compressed file.

        Args:
            path: output path
            cloud: cloud storage configuration
            kwargs: additional configuration as keyword args
        """

        if self.config:
            path, apath = self.checkarchive(path)
            os.makedirs(path, exist_ok=True)
            Configuration().save(self.config, path)
            if self.ann:
                self.ann.save(f"{path}/embeddings")
            if self.reducer:
                self.reducer.save(f"{path}/lsa")
            if self.ids:
                self.ids.save(f"{path}/ids")
            if self.database:
                self.database.save(f"{path}/documents")
            if self.scoring:
                self.scoring.save(f"{path}/scoring")
            if self.indexes:
                self.indexes.save(f"{path}/indexes")
            if self.graph:
                self.graph.save(f"{path}/graph")
            if apath:
                self.archive.save(apath)
            cloud = self.createcloud(cloud=cloud, **kwargs)
            if cloud:
                cloud.save(apath if apath else path)

    def close(self):
        """
        Closes this embeddings index and frees all resources.
        """
        self.config, self.archive = None, None
        self.reducer, self.query = None, None
        self.ids = None
        if self.ann:
            self.ann.close()
            self.ann = None
        if self.database:
            self.database.close()
            self.database, self.functions = None, None
        if self.scoring:
            self.scoring.close()
            self.scoring = None
        if self.graph:
            self.graph.close()
            self.graph = None
        if self.indexes:
            self.indexes.close()
            self.indexes = None
        if self.model:
            self.model.close()
            self.model = None
        self.models = None

    def info(self):
        """
        Prints the current embeddings index configuration.
        """

        if self.config:
            print(json.dumps(self.config, sort_keys=True, default=str, indent=2))

    def issparse(self):
        """
        Checks if this instance has an associated sparse keyword or sparse vectors scoring index.

        Returns:
            True if scoring has an associated sparse keyword/vector index, False otherwise
        """

        return self.scoring and self.scoring.issparse()

    def isdense(self):
        """
        Checks if this instance has an associated VectoreIndex instance.

        Returns:
            True if this instance has an associated VectoreIndex, False otherwise
        """

        return self.ann is not None

    def isweighted(self):
        """
        Checks if this instance has an associated scoring instance with term weighting enabled.

        Returns:
            True if term weighting is enabled, False otherwise
        """

        return self.scoring and self.scoring.isweighted()

    def findmodel(self, index=None):
        """
        Finds the primary vector model used by this instance.

        Returns:
            Vectors
        """

        return (
            self.indexes.findmodel(index)
            if index and self.indexes
            else (
                self.model
                if self.model
                else self.scoring.findmodel()
                if self.scoring and self.scoring.findmodel()
                else self.indexes.findmodel()
                if self.indexes
                else None
            )
        )

    def configure(self, config):
        """
        Sets the configuration for this embeddings index and loads config-driven models.

        Args:
            config: embeddings configuration
        """

        self.config = config

        self.reducer = None

        scoring = self.config.get("scoring") if self.config else None
        self.scoring = self.createscoring() if scoring and not self.hassparse() else None

        self.model = self.loadvectors() if self.config else None

        self.query = self.loadquery() if self.config else None

    def initindex(self, reindex):
        """
        Initialize new index.

        Args:
            reindex: if this is a reindex operation in which case database creation is skipped, defaults to False
        """

        self.defaults()

        self.ids = None

        if not reindex:
            self.database = self.createdatabase()

            self.archive = None

        if self.ann:
            self.ann.close()

        self.ann = None

        if self.hassparse():
            self.scoring = self.createscoring()

        self.indexes = self.createindexes()

        self.graph = self.creategraph()

    def defaults(self):
        """
        Apply default parameters to current configuration.

        Returns:
            configuration with default parameters set
        """

        self.config = self.config if self.config else {}

        if not self.config.get("scoring") and any(self.config.get(key) for key in ["keyword", "sparse", "hybrid"]):
            self.defaultsparse()

        if self.config.get("graph") is True:
            self.config["graph"] = {}

        if not self.model and (self.defaultallowed() or self.config.get("dense")):
            self.config["path"] = "sentence-transformers/all-MiniLM-L6-v2"

            self.model = self.loadvectors()

    def defaultsparse(self):
        """
        Logic to derive default sparse index configuration.
        """

        method = None
        for x in ["keyword", "hybrid"]:
            value = self.config.get(x)
            if value:
                method = value if isinstance(value, str) else "bm25"

                if x == "hybrid":
                    self.config["dense"] = True

        sparse = self.config.get("sparse", {})
        if sparse or method == "sparse":
            sparse = (
                {"path": self.config.get("sparse")}
                if isinstance(sparse, str)
                else {}
                if isinstance(sparse, bool)
                else sparse
            )
            sparse["path"] = sparse.get("path", "prithivida/Splade_PP_en_v2")

            self.config["scoring"] = {**{"method": "sparse"}, **sparse}

        elif method:
            self.config["scoring"] = {"method": method, "terms": True, "normalize": True}

    def defaultallowed(self):
        """
        Tests if this embeddings instance can use a default model if not otherwise provided.

        Returns:
            True if a default model is allowed, False otherwise
        """

        params = [("keyword", False), ("sparse", False), ("defaults", True)]
        return all(self.config.get(key, default) == default for key, default in params)

    def loadvectors(self):
        """
        Loads a vector model set in config.

        Returns:
            vector model
        """

        if "indexes" in self.config and self.models is None:
            self.models = {}

        dense = self.config.get("dense")
        if not self.config.get("path") and dense and isinstance(dense, str):
            self.config["path"] = dense

        return VectorsFactory.create(self.config, self.scoring, self.models)

    def loadquery(self):
        """
        Loads a query model set in config.

        Returns:
            query model
        """

        if "query" in self.config:
            return Query(**self.config["query"])

        return None

    def checkarchive(self, path):
        """
        Checks if path is an archive file.

        Args:
            path: path to check

        Returns:
            (working directory, current path) if this is an archive, original path otherwise
        """
        self.archive = ArchiveFactory.create()
        if self.archive.isarchive(path):
            return self.archive.path(), path
        return path, None

    def createcloud(self, **cloud):
        """
        Creates a cloud instance from config.

        Args:
            cloud: cloud configuration
        """

        config = cloud
        if config.get("cloud"):
            config.update(config.pop("cloud"))

        return CloudFactory.create(config) if config else None

    def createann(self):
        """
        Creates an VectoreIndex from config.

        Returns:
            new VectoreIndex, if enabled in config
        """

        if self.ann:
            self.ann.close()

        return ANNFactory.create(self.config) if self.config.get("path") or self.defaultallowed() else None

    def createdatabase(self):
        """
        Creates a database from config. This method will also close any existing database connection.

        Returns:
            new database, if enabled in config
        """

        if self.database:
            self.database.close()

        config = self.config.copy()

        self.functions = Functions(self) if "functions" in config else None
        if self.functions:
            config["functions"] = self.functions(config)

        return DatabaseFactory.create(config)

    def creategraph(self):
        """
        Creates a graph from config.

        Returns:
            new graph, if enabled in config
        """

        if self.graph:
            self.graph.close()

        if "graph" in self.config:
            config = self.config["graph"] if "graph" in self.config else {}

            config = self.columns(config)
            return GraphFactory.create(config)

        return None

    def createids(self, ids=None):
        """
        Creates indexids when content is disabled.

        Args:
            ids: optional ids to add

        Returns:
            new indexids, if content disabled
        """

        return IndexIds(self, ids) if not self.config.get("content") else None

    def createindexes(self):
        """
        Creates subindexes from config.

        Returns:
            list of subindexes
        """

        if self.indexes:
            self.indexes.close()

        if "indexes" in self.config:
            indexes = {}
            for index, config in self.config["indexes"].items():
                indexes[index] = Embeddings(config, models=self.models)

            return Indexes(self, indexes)

        return None

    def createscoring(self):
        """
        Creates a scoring from config.

        Returns:
            new scoring, if enabled in config
        """

        if self.scoring:
            self.scoring.close()

        if "scoring" in self.config:
            config = self.config["scoring"]
            config = config if isinstance(config, dict) else {"method": config}

            config = self.columns(config)
            return ScoringFactory.create(config, self.models)

        return None

    def hassparse(self):
        """
        Checks is this embeddings database has an associated sparse index.

        Returns:
            True if this embeddings has an associated scoring index
        """

        return ScoringFactory.issparse(self.config.get("scoring"))

    def columns(self, config):
        """
        Adds custom text/object column information if it's provided.

        Args:
            config: input configuration

        Returns:
            config with column information added
        """

        if "columns" in self.config:
            config = config.copy()

            config["columns"] = self.config["columns"]

        return config
