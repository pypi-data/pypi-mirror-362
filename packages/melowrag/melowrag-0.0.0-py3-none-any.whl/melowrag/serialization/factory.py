from .messagepack import MessagePack
from .pickle import Pickle


class SerializeFactory:
    """
    Methods to create data serializers.
    """

    @staticmethod
    def create(method=None, **kwargs):
        """
        Creates a new Serialize instance.

        Args:
            method: serialization method
            kwargs: additional keyword arguments to pass to serialize instance
        """

        if method == "pickle":
            return Pickle(**kwargs)

        return MessagePack(**kwargs)
