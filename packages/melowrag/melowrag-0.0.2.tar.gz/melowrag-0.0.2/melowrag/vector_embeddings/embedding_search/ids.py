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
This module provides the Ids class for resolving internal ids for lists of ids in embeddings.
"""


class Ids:
    """
    Resolves internal ids for lists of ids in embeddings.

    Args:
        embeddings (Embeddings): Embeddings instance to resolve ids from.
    """

    def __init__(self, embeddings):
        """
        Create a new ids action.

        Args:
            embeddings: embeddings instance
        """

        self.database = embeddings.database
        self.ids = embeddings.ids

    def __call__(self, ids):
        """
        Resolve internal ids.

        Args:
            ids: ids

        Returns:
            internal ids
        """

        results = self.database.ids(ids) if self.database else self.scan(ids)

        ids = {}
        for iid, uid in results:
            if uid not in ids:
                ids[uid] = []
            ids[uid].append(iid)

        return ids

    def scan(self, ids):
        """
        Scans embeddings ids array for matches when content is disabled.

        Args:
            ids: search ids

        Returns:
            internal ids
        """

        indices = []
        for uid in ids:
            indices.extend([(index, value) for index, value in enumerate(self.ids) if uid == value])

        return indices
