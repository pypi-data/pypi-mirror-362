from ...utilities import Resolver
from .ivfsparse import IVFSparse
from .pgsparse import PGSparse


class SparseANNFactory:
    """
    Methods to create Sparse VectoreIndex indexes.
    """

    @staticmethod
    def create(config):
        """
        Create an Sparse VectoreIndex.

        Args:
            config: index configuration parameters

        Returns:
            Sparse VectoreIndex
        """

        ann = None
        backend = config.get("backend", "ivfsparse")

        if backend == "ivfsparse":
            ann = IVFSparse(config)
        elif backend == "pgsparse":
            ann = PGSparse(config)
        else:
            ann = SparseANNFactory.resolve(backend, config)

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
            raise ImportError(f"Unable to resolve sparse ann backend: '{backend}'") from e
