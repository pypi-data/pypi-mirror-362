from ...utilities import Resolver
from .external import External
from .huggingface import HFVectors
from .litellm import LiteLLM
from .sbert import STVectors
from .words import WordVectors


class VectorsFactory:
    """
    Methods to create dense vector models.
    """

    @staticmethod
    def create(config, scoring=None, models=None):
        """
        Create a Vectors model instance.

        Args:
            config: vector configuration
            scoring: scoring instance
            models: models cache

        Returns:
            Vectors
        """

        method = VectorsFactory.method(config)

        if method == "external":
            return External(config, scoring, models)

        if method == "litellm":
            return LiteLLM(config, scoring, models)

        if method == "sentence-transformers":
            return STVectors(config, scoring, models) if config and config.get("path") else None

        if method == "words":
            return WordVectors(config, scoring, models)

        if HFVectors.ismethod(method):
            return HFVectors(config, scoring, models) if config and config.get("path") else None

        return VectorsFactory.resolve(method, config, scoring, models) if method else None

    @staticmethod
    def method(config):
        """
        Get or derive the vector method.

        Args:
            config: vector configuration

        Returns:
            vector method
        """

        method = config.get("method")
        path = config.get("path")

        if not method:
            if path:
                if LiteLLM.ismodel(path):
                    method = "litellm"
                elif WordVectors.ismodel(path):
                    method = "words"
                else:
                    method = "transformers"
            elif config.get("transform"):
                method = "external"

        return method

    @staticmethod
    def resolve(backend, config, scoring, models):
        """
        Attempt to resolve a custom backend.

        Args:
            backend: backend class
            config: vector configuration
            scoring: scoring instance
            models: models cache

        Returns:
            Vectors
        """

        try:
            return Resolver()(backend)(config, scoring, models)
        except Exception as e:
            raise ImportError(f"Unable to resolve vectors backend: '{backend}'") from e
