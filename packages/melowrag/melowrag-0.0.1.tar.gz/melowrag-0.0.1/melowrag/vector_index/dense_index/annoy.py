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

try:
    from annoy import AnnoyIndex

    ANNOY = True
except ImportError:
    ANNOY = False

from ..base import VectoreIndex


# pylint: disable=W0223
class Annoy(VectoreIndex):
    """
    Builds an VectoreIndex index using the Annoy library.
    """

    def __init__(self, config):
        super().__init__(config)

        if not ANNOY:
            raise ImportError('Annoy is not available - install "ann" extra to enable')

    def load(self, path):
        self.backend = AnnoyIndex(self.config["dimensions"], self.config["metric"])
        self.backend.load(path)

    def index(self, embeddings):
        self.config["metric"] = "dot"

        self.backend = AnnoyIndex(self.config["dimensions"], self.config["metric"])

        for x in range(embeddings.shape[0]):
            self.backend.add_item(x, embeddings[x])

        ntrees = self.setting("ntrees", 10)
        self.backend.build(ntrees)

        self.metadata({"ntrees": ntrees})

    def search(self, queries, limit):
        searchk = self.setting("searchk", -1)

        results = []
        for query in queries:
            ids, scores = self.backend.get_nns_by_vector(query, n=limit, search_k=searchk, include_distances=True)

            results.append(list(zip(ids, scores, strict=False)))

        return results

    def count(self):
        return self.backend.get_n_items()

    def save(self, path):
        self.backend.save(path)
