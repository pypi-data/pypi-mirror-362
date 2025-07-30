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

import os

from .documents import Documents


class Indexes:
    """
    Manages a collection of subindexes for an embeddings instance.
    """

    def __init__(self, embeddings, indexes):
        """
        Creates a new indexes instance.

        Args:
            embeddings: embeddings instance
            indexes: dict of subindexes to add
        """

        self.embeddings = embeddings
        self.indexes = indexes

        self.documents = None
        self.checkpoint = None

        columns = embeddings.config.get("columns", {})
        self.text = columns.get("text", "text")
        self.object = columns.get("object", "object")

        self.indexing = embeddings.model or embeddings.scoring

    def __contains__(self, name):
        """
        Returns True if name is in this instance, False otherwise.

        Returns:
            True if name is in this instance, False otherwise
        """

        return name in self.indexes

    def __getitem__(self, name):
        """
        Looks up an index by name.

        Args:
            name: index name

        Returns:
            index
        """

        return self.indexes[name]

    def __getattr__(self, name):
        """
        Looks up an index by attribute name.

        Args:
            name: index name

        Returns:
            index
        """

        try:
            return self.indexes[name]
        except Exception as e:
            raise AttributeError(e) from e

    def default(self):
        """
        Gets the default/first index.

        Returns:
            default index
        """

        return next(iter(self.indexes.keys()))

    def findmodel(self, index=None):
        """
        Finds a vector model. If index is empty, the first vector model is returned.

        Args:
            index: index name to match

        Returns:
            Vectors
        """

        matches = (
            [self.indexes[index].findmodel()]
            if index
            else [index.findmodel() for index in self.indexes.values() if index.findmodel()]
        )
        return matches[0] if matches else None

    def insert(self, documents, index=None, checkpoint=None):
        """
        Inserts a batch of documents into each subindex.

        Args:
            documents: list of (id, data, tags)
            index: indexid offset
            checkpoint: optional checkpoint directory, enables indexing restart
        """

        if not self.documents:
            self.documents = Documents()
            self.checkpoint = checkpoint

        batch = []
        for _, document, _ in documents:
            parent = document
            if isinstance(parent, dict):
                parent = parent.get(self.text, document.get(self.object))

            if parent is not None or not self.indexing:
                batch.append((index, document, None))
                index += 1

        self.documents.add(batch)

    def delete(self, ids):
        """
        Deletes ids from each subindex.

        Args:
            ids: list of ids to delete
        """

        for index in self.indexes.values():
            index.delete(ids)

    def index(self):
        """
        Builds each subindex.
        """

        for name, index in self.indexes.items():
            index.index(self.documents, checkpoint=f"{self.checkpoint}/{name}" if self.checkpoint else None)

        self.documents.close()
        self.documents = None
        self.checkpoint = None

    def upsert(self):
        """
        Runs upsert for each subindex.
        """

        for index in self.indexes.values():
            index.upsert(self.documents)

        self.documents.close()
        self.documents = None

    def load(self, path):
        """
        Loads each subindex from path.

        Args:
            path: directory path to load subindexes
        """

        for name, index in self.indexes.items():
            directory = os.path.join(path, name)
            if index.exists(directory):
                index.load(directory)

    def save(self, path):
        """
        Saves each subindex to path.

        Args:
            path: directory path to save subindexes
        """

        for name, index in self.indexes.items():
            index.save(os.path.join(path, name))

    def close(self):
        """
        Close and free resources used by this instance.
        """

        for index in self.indexes.values():
            index.close()
