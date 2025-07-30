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

from queue import Queue
from threading import Thread

from ..vector_index import SparseANNFactory
from ..vector_processing import SparseVectorsFactory
from .base import Scoring


class Sparse(Scoring):
    """
    Sparse vector scoring.
    """

    COMPLETE = 1

    def __init__(self, config=None, models=None):
        super().__init__(config)

        config = {k: v for k, v in config.items() if k != "method"}
        if "vectormethod" in config:
            config["method"] = config["vectormethod"]

        self.model = SparseVectorsFactory.create(config, models)

        self.ann = None

        self.batch = self.config.get("batch", 1024)
        self.thread, self.queue, self.data = None, None, None

    def insert(self, documents, index=None, checkpoint=None):
        self.start(checkpoint)

        data = []
        for uid, document, tags in documents:
            if isinstance(document, dict):
                document = document.get(self.text, document.get(self.object))

            if document is not None:
                data.append((uid, " ".join(document) if isinstance(document, list) else document, tags))

        self.queue.put(data)

    def delete(self, ids):
        self.ann.delete(ids)

    def index(self, documents=None):
        if documents:
            self.insert(documents)

        embeddings = self.stop()
        if embeddings is not None:
            self.ann = SparseANNFactory.create(self.config)
            self.ann.index(embeddings)

    def upsert(self, documents=None):
        if documents:
            self.insert(documents)

        if self.ann:
            embeddings = self.stop()
            if embeddings is not None:
                self.ann.append(embeddings)
        else:
            self.index()

    def weights(self, tokens):
        return None

    def search(self, query, limit=3):
        return self.batchsearch([query], limit)[0]

    def batchsearch(self, queries, limit=3, threads=True):
        embeddings = self.model.batchtransform((None, query, None) for query in queries)

        return self.ann.search(embeddings, limit)

    def count(self):
        return self.ann.count()

    def load(self, path):
        self.ann = SparseANNFactory.create(self.config)
        self.ann.load(path)

    def save(self, path):
        if self.ann:
            self.ann.save(path)

    def close(self):
        if self.ann:
            self.ann.close()

        self.model, self.ann, self.thread, self.queue = None, None, None, None

    def issparse(self):
        return True

    def isnormalized(self):
        return True

    def start(self, checkpoint):
        """
        Starts an encoding processing thread.

        Args:
            checkpoint: checkpoint directory
        """

        if not self.thread:
            self.queue = Queue(5)
            self.thread = Thread(target=self.encode, args=(checkpoint,))
            self.thread.start()

    def stop(self):
        """
        Stops an encoding processing thread. Return processed results.

        Returns:
            results
        """

        results = None
        if self.thread:
            self.queue.put(Sparse.COMPLETE)

            self.thread.join()
            self.thread, self.queue = None, None

            results = self.data
            self.data = None

        return results

    def encode(self, checkpoint):
        """
        Encodes streaming data.

        Args:
            checkpoint: checkpoint directory
        """

        _, dimensions, self.data = self.model.vectors(self.stream(), self.batch, checkpoint)

        self.config["dimensions"] = dimensions

    def stream(self):
        """
        Streams data from an input queue until end of stream message received.
        """

        batch = self.queue.get()
        while batch != Sparse.COMPLETE:
            yield from batch
            batch = self.queue.get()
