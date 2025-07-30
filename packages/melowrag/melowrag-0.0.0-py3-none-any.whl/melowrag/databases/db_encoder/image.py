from io import BytesIO

try:
    from PIL import Image

    PIL = True
except ImportError:
    PIL = False

from .base import Encoder


class ImageEncoder(Encoder):
    """
    Encodes and decodes Image objects as compressed binary content, using the original image's algorithm.
    """

    def __init__(self):
        """
        Creates a new ImageEncoder.
        """

        if not PIL:
            raise ImportError('ImageEncoder is not available - install "database" extra to enable')

    def encode(self, obj):
        output = BytesIO()

        obj.save(output, format=obj.format, quality="keep")

        return output.getvalue()

    def decode(self, data):
        return Image.open(BytesIO(data)) if data else None
