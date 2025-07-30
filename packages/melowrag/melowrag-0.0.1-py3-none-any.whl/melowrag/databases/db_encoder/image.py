# Copyright 2025 The MelowRAG Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
