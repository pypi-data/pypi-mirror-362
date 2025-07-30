from ...utilities import Resolver
from .annoy import Annoy
from .faiss import Faiss
from .hnsw import HNSW
from .numpy import NumPy
from .pgvector import PGVector
from .sqlite import SQLite
from .torch import Torch


class ANNFactory:
    """
    Methods to create VectoreIndex indexes.
    """

    @staticmethod
    def create(config):
        """
        Create an VectoreIndex.

        Args:
            config: index configuration parameters

        Returns:
            VectoreIndex
        """

        ann = None
        backend = config.get("backend", "faiss")

        if backend == "annoy":
            ann = Annoy(config)
        elif backend == "faiss":
            ann = Faiss(config)
        elif backend == "hnsw":
            ann = HNSW(config)
        elif backend == "numpy":
            ann = NumPy(config)
        elif backend == "pgvector":
            ann = PGVector(config)
        elif backend == "sqlite":
            ann = SQLite(config)
        elif backend == "torch":
            ann = Torch(config)
        else:
            ann = ANNFactory.resolve(backend, config)

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
            raise ImportError(f"Unable to resolve ann backend: '{backend}'") from e
