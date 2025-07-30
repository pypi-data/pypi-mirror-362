import math

import numpy as np

try:
    from scipy.sparse import vstack
    from sklearn.cluster import MiniBatchKMeans
    from sklearn.metrics import pairwise_distances_argmin_min
    from sklearn.utils.extmath import safe_sparse_dot

    IVFSPARSE = True
except ImportError:
    IVFSPARSE = False

from ...serialization import SerializeFactory
from ...utilities import SparseArray
from ..base import VectoreIndex


class IVFSparse(VectoreIndex):
    """
    Inverted file (IVF) index with flat vector file storage and sparse array support.

    IVFSparse builds an IVF index and enables approximate nearest neighbor (VectoreIndex) search.

    This index is modeled after Faiss and supports many of the same parameters.

    See this link for more: https://github.com/facebookresearch/faiss/wiki/Faster-search
    """

    def __init__(self, config):
        super().__init__(config)

        if not IVFSPARSE:
            raise ImportError('IVFSparse is not available - install "ann" extra to enable')

        self.centroids = None

        self.ids = None

        self.blocks = None

        self.deletes = None

    def index(self, embeddings):
        train, sample = embeddings, self.setting("sample")
        if sample:
            rng = np.random.default_rng(0)
            indices = sorted(
                rng.choice(
                    train.shape[0],
                    int(sample * train.shape[0]),
                    replace=False,
                    shuffle=False,
                )
            )
            train = train[indices]

        clusters = self.nlist(embeddings.shape[0], train.shape[0])

        if clusters > 1:
            kmeans = MiniBatchKMeans(n_clusters=clusters, random_state=0, n_init="auto").fit(train)

            indices, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, train, metric="cosine")
            self.centroids = embeddings[np.unique(indices)]

        ids = self.aggregate(embeddings)

        self.ids = dict(sorted(ids.items(), key=lambda x: x[0]))

        self.blocks = {k: embeddings[v] for k, v in self.ids.items()}

        self.deletes = []

        self.config["offset"] = embeddings.shape[0]
        self.metadata({"clusters": clusters})

    def append(self, embeddings):
        offset = self.size()

        for cluster, ids in self.aggregate(embeddings).items():
            self.ids[cluster].extend([x + offset for x in ids])

            self.blocks[cluster] = vstack([self.blocks[cluster], embeddings[ids]])

        self.config["offset"] += embeddings.shape[0]
        self.metadata()

    def delete(self, ids):
        self.deletes.extend(ids)

    def search(self, queries, limit):
        results = []
        for query in queries:
            if self.centroids is not None:
                indices, _ = self.topn(query, self.centroids, self.nprobe())

                ids = np.concatenate([self.ids[x] for x in indices if x in self.ids])

                data = vstack([self.blocks[x] for x in indices if x in self.blocks])
            else:
                ids, data = np.array(self.ids[0]), self.blocks[0]

            deletes = np.argwhere(np.isin(ids, self.deletes)).ravel()

            indices, scores = self.topn(query, data, limit, deletes)

            results.append(list(zip(ids[indices].tolist(), scores.tolist(), strict=False)))

        return results

    def count(self):
        return self.size() - len(self.deletes)

    def load(self, path):
        serializer = SerializeFactory.create("msgpack", streaming=True, read_size=1)

        with open(path, "rb") as f:
            unpacker = serializer.loadstream(f)
            header = next(unpacker)

            self.centroids = SparseArray().load(f) if header["centroids"] else None

            self.ids = dict(next(unpacker))

            self.blocks = {}
            for key in self.ids:
                self.blocks[key] = SparseArray().load(f)

            self.deletes = next(unpacker)

    def save(self, path):
        serializer = SerializeFactory.create("msgpack")

        with open(path, "wb") as f:
            serializer.savestream(
                {
                    "centroids": self.centroids is not None,
                    "count": self.count(),
                    "blocks": len(self.blocks),
                },
                f,
            )

            if self.centroids is not None:
                SparseArray().save(f, self.centroids)

            serializer.savestream(list(self.ids.items()), f)

            for block in self.blocks.values():
                SparseArray().save(f, block)

            serializer.savestream(self.deletes, f)

    def aggregate(self, data):
        """
        Aggregates input data array into clusters. This method sorts each data element into the
        cluster with the highest cosine similarity centroid.

        Args:
            data: input data

        Returns:
            {cluster, ids}
        """

        if self.centroids is None:
            return {0: list(range(data.shape[0]))}

        indices, _ = pairwise_distances_argmin_min(data, self.centroids, metric="cosine")

        ids = {}
        for x, cluster in enumerate(indices.tolist()):
            if cluster not in ids:
                ids[cluster] = []

            ids[cluster].append(x)

        return ids

    def topn(self, query, data, limit, deletes=None):
        """
        Gets the top n most similar data elements for query.

        Args:
            query: input query array
            data: data array
            limit: top n
            deletes: optional list of deletes to filter from results

        Returns:
            list of matching (indices, scores)
        """

        scores = safe_sparse_dot(query, data.T, dense_output=True)

        if deletes is not None:
            scores[:, deletes] = 0

        indices = np.argpartition(-scores, limit if limit < scores.shape[0] else scores.shape[0] - 1)[:, :limit]
        scores = np.clip(np.take_along_axis(scores, indices, axis=1), 0.0, 1.0)

        return indices[0], scores[0]

    def nlist(self, count, train):
        """
        Calculates the number of clusters for this IVFSparse index. Note that the final number of clusters
        could be lower as duplicate cluster centroids are filtered out.

        Args:
            count: initial dataset size
            train: number of rows used to train

        Returns:
            number of clusters
        """

        default = 1 if count <= 5000 else self.cells(train)

        return self.setting("nlist", default)

    def nprobe(self):
        """
        Gets or derives the nprobe search parameter.

        Returns:
            nprobe setting
        """

        size = self.size()

        default = 6 if size <= 5000 else self.cells(size) // 64
        return self.setting("nprobe", default)

    def cells(self, count):
        """
        Calculates the number of IVF cells for an IVFSparse index.

        Args:
            count: number of rows

        Returns:
            number of IVF cells
        """

        return max(min(round(4 * math.sqrt(count)), int(count / 39)), 1)

    def size(self):
        """
        Gets the total size of this index including deletes.

        Returns:
            size
        """

        return sum(len(x) for x in self.ids.values())
