from ..utilities import Resolver
from .hub import HuggingFaceHub
from .storage import LIBCLOUD, ObjectStorage


class CloudFactory:
    """
    Methods to create Cloud instances.
    """

    @staticmethod
    def create(config):
        """
        Creates a Cloud instance.

        Args:
            config: cloud configuration

        Returns:
            Cloud
        """

        cloud = None

        provider = config.get("provider", "")

        if provider.lower() == "huggingface-hub":
            cloud = HuggingFaceHub(config)

        elif ObjectStorage.isprovider(provider):
            cloud = ObjectStorage(config)

        elif provider:
            cloud = CloudFactory.resolve(provider, config)

        return cloud

    @staticmethod
    def resolve(backend, config):
        """
        Attempt to resolve a custom cloud backend.

        Args:
            backend: backend class
            config: configuration parameters

        Returns:
            Cloud
        """

        try:
            return Resolver()(backend)(config)

        except Exception as e:
            message = f'Unable to resolve cloud backend: "{backend}".'

            message += ' Cloud storage is not available - install "cloud" extra to enable' if not LIBCLOUD else ""

            raise ImportError(message) from e
