import numpy as np

from ...serialization import SerializeFactory
from ..base import VectoreIndex


class NumPy(VectoreIndex):
    """
    Builds an VectoreIndex index backed by a NumPy array.
    """

    def __init__(self, config):
        super().__init__(config)

        self.all, self.cat, self.dot, self.zeros = np.all, np.concatenate, np.dot, np.zeros
        self.argsort, self.xor, self.clip = np.argsort, np.bitwise_xor, np.clip

        quantize = self.config.get("quantize")
        self.qbits = quantize if quantize and isinstance(quantize, int) and not isinstance(quantize, bool) else None

    def load(self, path):
        try:
            self.backend = self.tensor(np.load(path, allow_pickle=False))
        except ValueError:
            self.backend = self.tensor(SerializeFactory.create("pickle").load(path))

    def index(self, embeddings):
        self.backend = self.tensor(embeddings)

        self.config["offset"] = embeddings.shape[0]
        self.metadata(self.settings())

    def append(self, embeddings):
        self.backend = self.cat((self.backend, self.tensor(embeddings)), axis=0)

        self.config["offset"] += embeddings.shape[0]
        self.metadata()

    def delete(self, ids):
        ids = [x for x in ids if x < self.backend.shape[0]]

        self.backend[ids] = self.tensor(self.zeros((len(ids), self.backend.shape[1])))

    def search(self, queries, limit):
        if self.qbits:
            scores = self.hammingscore(queries)
        else:
            scores = self.dot(self.tensor(queries), self.backend.T)

        ids = self.argsort(-scores)[:, :limit]

        results = []
        for x, score in enumerate(scores):
            results.append(list(zip(ids[x].tolist(), score[ids[x]].tolist(), strict=False)))

        return results

    def count(self):
        return self.backend[~self.all(self.backend == 0, axis=1)].shape[0]

    def save(self, path):
        with open(path, "wb") as handle:
            np.save(handle, self.numpy(self.backend), allow_pickle=False)

    def tensor(self, array):
        """
        Handles backend-specific code such as loading to a GPU device.

        Args:
            array: data array

        Returns:
            array with backend-specific logic applied
        """

        return array

    def numpy(self, array):
        """
        Handles backend-specific code to convert an array to numpy

        Args:
            array: data array

        Returns:
            numpy array
        """

        return array

    def totype(self, array, dtype):
        """
        Casts array to dtype.

        Args:
            array: input array
            dtype: dtype

        Returns:
            array cast as dtype
        """

        return np.int64(array) if dtype == np.int64 else array

    def settings(self):
        """
        Returns settings for this array.

        Returns:
            dict
        """

        return {"numpy": np.__version__}

    def hammingscore(self, queries):
        """
        Calculates a hamming distance score.

        This is defined as:

            score = 1.0 - (hamming distance / total number of bits)

        Args:
            queries: queries array

        Returns:
            scores
        """

        table = 1 << np.arange(8)
        table = self.tensor(np.array([np.count_nonzero(x & table) for x in np.arange(256)]))

        delta = self.xor(self.tensor(queries[:, None]), self.backend)

        delta = self.totype(delta, np.int64)

        return self.clip(1.0 - (table[delta].sum(axis=2) / (self.config["dimensions"] * 8)), 0.0, 1.0)
