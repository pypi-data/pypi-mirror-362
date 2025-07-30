from ..utilities import Resolver
from .networkx import NetworkX
from .rdbms import RDBMS


class GraphFactory:
    """
    Methods to create graphs.
    """

    @staticmethod
    def create(config):
        """
        Create a Graph.

        Args:
            config: graph configuration

        Returns:
            Graph
        """

        graph = None
        backend = config.get("backend", "networkx")

        if backend == "networkx":
            graph = NetworkX(config)
        elif backend == "rdbms":
            graph = RDBMS(config)
        else:
            graph = GraphFactory.resolve(backend, config)

        config["backend"] = backend

        return graph

    @staticmethod
    def resolve(backend, config):
        """
        Attempt to resolve a custom backend.

        Args:
            backend: backend class
            config: index configuration parameters

        Returns:
            Graph
        """

        try:
            return Resolver()(backend)(config)
        except Exception as e:
            raise ImportError(f"Unable to resolve graph backend: '{backend}'") from e
