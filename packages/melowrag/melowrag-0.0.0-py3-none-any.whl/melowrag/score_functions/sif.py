import numpy as np

from .tfidf import TFIDF


class SIF(TFIDF):
    """
    Smooth Inverse Frequency (SIF) scoring.
    """

    def __init__(self, config=None):
        super().__init__(config)

        self.a = self.config.get("a", 1e-3)

    def computefreq(self, tokens):
        return {token: self.wordfreq[token] for token in tokens}

    def score(self, freq, idf, length):
        if isinstance(freq, np.ndarray) and freq.shape != np.array(idf).shape:
            freq.fill(freq.sum())

        return self.a / (self.a + freq / self.tokens)
