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
    from scipy.sparse import csr_matrix, vstack
    from sklearn.preprocessing import normalize
    from sklearn.utils.extmath import safe_sparse_dot

    SPARSE = True
except ImportError:
    SPARSE = False

from ...utilities import SparseArray
from ..base import Vectors


# pylint: disable=W0223
class SparseVectors(Vectors):
    """
    Base class for sparse vector models. Vector models transform input content into sparse arrays.
    """

    def __init__(self, config, scoring, models):
        if not SPARSE:
            raise ImportError('SparseVectors is not available - install "vectors" extra to enable')

        super().__init__(config, scoring, models)

    def encode(self, data, category=None):
        embeddings = super().encode(data, category)

        embeddings = embeddings.cpu().coalesce()
        indices = embeddings.indices().numpy()
        values = embeddings.values().numpy()

        return csr_matrix((values, indices), shape=embeddings.size())

    def vectors(self, documents, batchsize=500, checkpoint=None, buffer=None, dtype=None):
        ids, dimensions, batches, stream = self.index(documents, batchsize, checkpoint)

        embeddings = None
        with open(stream, "rb") as queue:
            for _ in range(batches):
                data = self.loadembeddings(queue)
                embeddings = vstack((embeddings, data)) if embeddings is not None else data

        return (ids, dimensions, embeddings)

    def dot(self, queries, data):
        return safe_sparse_dot(queries, data.T, dense_output=True).tolist()

    def loadembeddings(self, f):
        return SparseArray().load(f)

    def saveembeddings(self, f, embeddings):
        SparseArray().save(f, embeddings)

    def truncate(self, embeddings):
        raise ValueError("Truncate is not supported for sparse vectors")

    def normalize(self, embeddings):
        return normalize(embeddings, copy=False)

    def quantize(self, embeddings):
        raise ValueError("Quantize is not supported for sparse vectors")
