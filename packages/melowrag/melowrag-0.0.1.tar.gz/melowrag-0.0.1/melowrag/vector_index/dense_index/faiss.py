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

import math
import platform

import numpy as np
from faiss import (
    IO_FLAG_MMAP,
    METRIC_INNER_PRODUCT,
    IndexBinaryIDMap,
    index_binary_factory,
    index_factory,
    omp_set_num_threads,
    read_index,
    read_index_binary,
    write_index,
    write_index_binary,
)

from ..base import VectoreIndex

if platform.system() == "Darwin":
    omp_set_num_threads(1)


class Faiss(VectoreIndex):
    """
    Builds an VectoreIndex index using the Faiss library.
    """

    def __init__(self, config):
        super().__init__(config)

        quantize = self.config.get("quantize")
        self.qbits = quantize if quantize and isinstance(quantize, int) and not isinstance(quantize, bool) else None

    def load(self, path):
        readindex = read_index_binary if self.qbits else read_index

        self.backend = readindex(path, IO_FLAG_MMAP if self.setting("mmap") is True else 0)

    def index(self, embeddings):
        train, sample = embeddings, self.setting("sample")
        if sample:
            rng = np.random.default_rng(0)
            indices = sorted(rng.choice(train.shape[0], int(sample * train.shape[0]), replace=False, shuffle=False))
            train = train[indices]

        params = self.configure(embeddings.shape[0], train.shape[0])

        self.backend = self.create(embeddings, params)

        self.backend.train(train)

        self.backend.add_with_ids(embeddings, np.arange(embeddings.shape[0], dtype=np.int64))

        self.config["offset"] = embeddings.shape[0]
        self.metadata({"components": params})

    def append(self, embeddings):
        new = embeddings.shape[0]

        self.backend.add_with_ids(
            embeddings, np.arange(self.config["offset"], self.config["offset"] + new, dtype=np.int64)
        )

        self.config["offset"] += new
        self.metadata()

    def delete(self, ids):
        self.backend.remove_ids(np.array(ids, dtype=np.int64))

    def search(self, queries, limit):
        self.backend.nprobe = self.nprobe()
        self.backend.nflip = self.setting("nflip", self.backend.nprobe)

        scores, ids = self.backend.search(queries, limit)

        results = []
        for x, score in enumerate(scores):
            results.append(list(zip(ids[x].tolist(), self.scores(score), strict=False)))

        return results

    def count(self):
        return self.backend.ntotal

    def save(self, path):
        writeindex = write_index_binary if self.qbits else write_index

        writeindex(self.backend, path)

    def configure(self, count, train):
        """
        Configures settings for a new index.

        Args:
            count: initial number of embeddings rows
            train: number of rows selected for model training

        Returns:
            user-specified or generated components setting
        """

        components = self.setting("components")

        if components:
            return self.components(components, train)

        quantize = self.setting("quantize", self.config.get("quantize"))
        quantize = 8 if isinstance(quantize, bool) else quantize

        storage = f"SQ{quantize}" if quantize else "Flat"

        if count <= 5000:
            return "BFlat" if self.qbits else f"IDMap,{storage}"

        x = self.cells(train)
        components = f"BIVF{x}" if self.qbits else f"IVF{x},{storage}"

        return components

    def create(self, embeddings, params):
        """
        Creates a new index.

        Args:
            embeddings: embeddings to index
            params: index parameters

        Returns:
            new index
        """

        if self.qbits:
            index = index_binary_factory(embeddings.shape[1] * 8, params)

            if any(x in params for x in ["BFlat", "BHNSW"]):
                index = IndexBinaryIDMap(index)

            return index

        return index_factory(embeddings.shape[1], params, METRIC_INNER_PRODUCT)

    def cells(self, count):
        """
        Calculates the number of IVF cells for an IVF index.

        Args:
            count: number of embeddings rows

        Returns:
            number of IVF cells
        """

        return max(min(round(4 * math.sqrt(count)), int(count / 39)), 1)

    def components(self, components, train):
        """
        Formats a components string. This method automatically calculates the optimal number of IVF cells, if omitted.

        Args:
            components: input components string
            train: number of rows selected for model training

        Returns:
            formatted components string
        """

        x = self.cells(train)

        components = [f"IVF{x}" if component == "IVF" else component for component in components.split(",")]

        return ",".join(components)

    def nprobe(self):
        """
        Gets or derives the nprobe search parameter.

        Returns:
            nprobe setting
        """

        count = self.count()

        default = 6 if count <= 5000 else round(self.cells(count) / 16)
        return self.setting("nprobe", default)

    def scores(self, scores):
        """
        Calculates the index score from the input score. This method returns the hamming score
        (1.0 - (hamming distance / total number of bits)) for binary indexes and the input
        scores otherwise.

        Args:
            scores: input scores

        Returns:
            index scores
        """

        if self.qbits:
            return np.clip(1.0 - (scores / (self.config["dimensions"] * 8)), 0.0, 1.0).tolist()

        return scores.tolist()
