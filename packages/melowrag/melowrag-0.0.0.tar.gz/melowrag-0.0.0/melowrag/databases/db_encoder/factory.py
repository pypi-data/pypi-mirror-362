from ...utilities import Resolver
from .base import Encoder
from .serialize import SerializeEncoder


class EncoderFactory:
    """
    Encoder factory. Creates new Encoder instances.
    """

    @staticmethod
    def get(encoder):
        """
        Gets a new instance of encoder class.

        Args:
            encoder: Encoder instance class

        Returns:
            Encoder class
        """

        if "." not in encoder:
            encoder = ".".join(__name__.split(".")[:-1]) + "." + encoder.capitalize() + "Encoder"

        return Resolver()(encoder)

    @staticmethod
    def create(encoder):
        """
        Creates a new Encoder instance.

        Args:
            encoder: Encoder instance class

        Returns:
            Encoder
        """

        if encoder is True:
            return Encoder()

        if encoder in ["messagepack", "pickle"]:
            return SerializeEncoder(encoder)

        return EncoderFactory.get(encoder)()
