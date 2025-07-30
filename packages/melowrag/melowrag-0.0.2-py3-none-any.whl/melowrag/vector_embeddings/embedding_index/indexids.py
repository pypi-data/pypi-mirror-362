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

"""
IndexIds module
"""

from ...serialization import Serializer


class IndexIds:
    """
    Stores index ids when content is disabled.
    """

    def __init__(self, embeddings, ids=None):
        """
        Creates an IndexIds instance.

        Args:
            embeddings: embeddings instance
            ids: ids to store
        """

        self.config = embeddings.config
        self.ids = ids

    def __iter__(self):
        yield from self.ids

    def __getitem__(self, index):
        return self.ids[index]

    def __setitem__(self, index, value):
        self.ids[index] = value

    def __add__(self, ids):
        return self.ids + ids

    def load(self, path):
        """
        Loads IndexIds from path.

        Args:
            path: path to load
        """

        if "ids" in self.config:
            self.ids = self.config.pop("ids")
        else:
            self.ids = Serializer.load(path)

    def save(self, path):
        """
        Saves IndexIds to path.

        Args:
            path: path to save
        """

        Serializer.save(self.ids, path)
