from ...serialization import SerializeFactory
from .base import Encoder


class SerializeEncoder(Encoder):
    """
    Encodes and decodes objects using the internal serialize package.
    """

    def __init__(self, method):
        super().__init__()

        self.serializer = SerializeFactory.create(method)

    def encode(self, obj):
        return self.serializer.savebytes(obj)

    def decode(self, data):
        return self.serializer.loadbytes(data)
