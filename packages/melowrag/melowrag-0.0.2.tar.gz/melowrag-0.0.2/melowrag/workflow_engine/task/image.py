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

import re

try:
    from PIL import Image

    PIL = True
except ImportError:
    PIL = False

from .file import FileTask


class ImageTask(FileTask):
    """
    Task that processes image file urls
    """

    def register(self):
        """
        Checks if required dependencies are installed.
        """

        if not PIL:
            raise ImportError('ImageTask is not available - install "workflow" extra to enable')

    def accept(self, element):
        return super().accept(element) and re.search(r"\.(gif|bmp|jpg|jpeg|png|webp)$", element.lower())

    def prepare(self, element):
        return Image.open(super().prepare(element))
