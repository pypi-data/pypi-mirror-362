import numpy as np

try:
    # pylint: disable=E0611
    from hnswlib import Index

    HNSWLIB = True
except ImportError:
    HNSWLIB = False

from ..base import VectoreIndex


class HNSW(VectoreIndex):
    """
    Builds an VectoreIndex index using the hnswlib library.
    """

    def __init__(self, config):
        super().__init__(config)

        if not HNSWLIB:
            raise ImportError('HNSW is not available - install "ann" extra to enable')

    def load(self, path):
        self.backend = Index(dim=self.config["dimensions"], space=self.config["metric"])
        self.backend.load_index(path)

    def index(self, embeddings):
        self.config["metric"] = "ip"

        efconstruction = self.setting("efconstruction", 200)
        m = self.setting("m", 16)
        seed = self.setting("randomseed", 100)

        self.backend = Index(dim=self.config["dimensions"], space=self.config["metric"])
        self.backend.init_index(max_elements=embeddings.shape[0], ef_construction=efconstruction, M=m, random_seed=seed)

        self.backend.add_items(embeddings, np.arange(embeddings.shape[0], dtype=np.int64))

        self.config["offset"] = embeddings.shape[0]
        self.config["deletes"] = 0
        self.metadata({"efconstruction": efconstruction, "m": m, "seed": seed})

    def append(self, embeddings):
        new = embeddings.shape[0]

        self.backend.resize_index(self.config["offset"] + new)

        self.backend.add_items(embeddings, np.arange(self.config["offset"], self.config["offset"] + new, dtype=np.int64))

        self.config["offset"] += new
        self.metadata()

    def delete(self, ids):
        for uid in ids:
            try:
                self.backend.mark_deleted(uid)
                self.config["deletes"] += 1
            except RuntimeError:
                continue

    def search(self, queries, limit):
        ef = self.setting("efsearch")
        if ef:
            self.backend.set_ef(ef)

        ids, distances = self.backend.knn_query(queries, k=limit)

        results = []
        for x, distance in enumerate(distances):
            scores = [1 - d for d in distance.tolist()]

            results.append(list(zip(ids[x].tolist(), scores, strict=False)))

        return results

    def count(self):
        return self.backend.get_current_count() - self.config["deletes"]

    def save(self, path):
        self.backend.save_index(path)
