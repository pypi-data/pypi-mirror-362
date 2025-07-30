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
import os
from collections import Counter
from multiprocessing.pool import ThreadPool

import numpy as np

from ..pipelines import Tokenizer
from ..serialization import Serializer
from .base import Scoring
from .terms import Terms


class TFIDF(Scoring):
    """
    Term frequency-inverse document frequency (TF-IDF) scoring.
    """

    def __init__(self, config=None):
        super().__init__(config)

        self.total = 0
        self.tokens = 0
        self.avgdl = 0

        self.docfreq = Counter()
        self.wordfreq = Counter()
        self.avgfreq = 0

        self.idf = {}
        self.avgidf = 0

        self.tags = Counter()

        self.tokenizer = None

        self.terms = Terms(self.config["terms"], self.score, self.idf) if self.config.get("terms") else None

        self.documents = {} if self.config.get("content") else None

        self.normalize = self.config.get("normalize")
        self.avgscore = None

    def insert(self, documents, index=None, checkpoint=None):
        for uid, document, tags in documents:
            if isinstance(document, dict):
                document = document.get(self.text, document.get(self.object))

            if document is not None:
                uid = index if index is not None else uid

                if isinstance(document, str | list):
                    if self.documents is not None:
                        self.documents[uid] = document

                    tokens = self.tokenize(document) if isinstance(document, str) else document

                    if self.terms is not None:
                        self.terms.insert(uid, tokens)

                    self.addstats(tokens, tags)

                index = index + 1 if index is not None else None

    def delete(self, ids):
        if self.terms:
            self.terms.delete(ids)

        if self.documents:
            for uid in ids:
                self.documents.pop(uid)

    def index(self, documents=None):
        super().index(documents)

        if self.wordfreq:
            self.tokens = sum(self.wordfreq.values())

            self.avgfreq = self.tokens / len(self.wordfreq.values())

            self.avgdl = self.tokens / self.total

            idfs = self.computeidf(np.array(list(self.docfreq.values())))
            for x, word in enumerate(self.docfreq):
                self.idf[word] = float(idfs[x])

            self.avgidf = float(np.mean(idfs))

            self.avgscore = self.score(self.avgfreq, self.avgidf, self.avgdl)

            self.tags = Counter({tag: number for tag, number in self.tags.items() if number >= self.total * 0.005})

        if self.terms:
            self.terms.index()

    def weights(self, tokens):
        length = len(tokens)

        freq = self.computefreq(tokens)
        freq = np.array([freq[token] for token in tokens])

        idf = np.array([self.idf[token] if token in self.idf else self.avgidf for token in tokens])

        weights = self.score(freq, idf, length).tolist()

        if self.tags:
            tags = {token: self.tags[token] for token in tokens if token in self.tags}
            if tags:
                maxWeight = max(weights)
                maxTag = max(tags.values())

                weights = [
                    max(maxWeight * (tags[tokens[x]] / maxTag), weight) if tokens[x] in tags else weight
                    for x, weight in enumerate(weights)
                ]

        return weights

    def search(self, query, limit=3):
        if self.terms:
            query = self.tokenize(query) if isinstance(query, str) else query

            scores = self.terms.search(query, limit)

            if self.normalize and scores:
                maxscore = min(scores[0][1] + self.avgscore, 6 * self.avgscore)

                scores = [(x, min(score / maxscore, 1.0)) for x, score in scores]

            return self.results(scores)

        return None

    def batchsearch(self, queries, limit=3, threads=True):
        threads = math.ceil(self.count() / 25000) if isinstance(threads, bool) and threads else int(threads)
        threads = min(max(threads, 1), os.cpu_count())

        results = []
        with ThreadPool(threads) as pool:
            for result in pool.starmap(self.search, [(x, limit) for x in queries]):
                results.append(result)

        return results

    def count(self):
        return self.terms.count() if self.terms else self.total

    def load(self, path):
        state = Serializer.load(path)

        for key in ["docfreq", "wordfreq", "tags"]:
            state[key] = Counter(state[key])

        state["documents"] = dict(state["documents"]) if state["documents"] else state["documents"]

        self.__dict__.update(state)

        if self.config.get("terms"):
            self.terms = Terms(self.config["terms"], self.score, self.idf)
            self.terms.load(path + ".terms")

    def save(self, path):
        skipfields = ("config", "terms", "tokenizer")

        state = {key: value for key, value in self.__dict__.items() if key not in skipfields}

        state["documents"] = list(state["documents"].items()) if state["documents"] else state["documents"]

        Serializer.save(state, path)

        if self.terms:
            self.terms.save(path + ".terms")

    def close(self):
        if self.terms:
            self.terms.close()

    def issparse(self):
        return self.terms is not None

    def isnormalized(self):
        return self.normalize

    def computefreq(self, tokens):
        """
        Computes token frequency. Used for token weighting.

        Args:
            tokens: input tokens

        Returns:
            {token: count}
        """

        return Counter(tokens)

    def computeidf(self, freq):
        """
        Computes an idf score for word frequency.

        Args:
            freq: word frequency

        Returns:
            idf score
        """

        return np.log((self.total + 1) / (freq + 1)) + 1

    # pylint: disable=W0613
    def score(self, freq, idf, length):
        """
        Calculates a score for each token.

        Args:
            freq: token frequency
            idf: token idf score
            length: total number of tokens in source document

        Returns:
            token score
        """

        return idf * np.sqrt(freq) * (1 / np.sqrt(length))

    def addstats(self, tokens, tags):
        """
        Add tokens and tags to stats.

        Args:
            tokens: list of tokens
            tags: list of tags
        """

        self.wordfreq.update(tokens)

        self.docfreq.update(set(tokens))

        if tags:
            self.tags.update(tags.split())

        self.total += 1

    def tokenize(self, text):
        """
        Tokenizes text using default tokenizer.

        Args:
            text: input text

        Returns:
            tokens
        """

        if not self.tokenizer:
            self.tokenizer = self.loadtokenizer()

        return self.tokenizer(text)

    def loadtokenizer(self):
        """
        Load default tokenizer.

        Returns:
            tokenize method
        """

        if self.config.get("tokenizer"):
            return Tokenizer(**self.config.get("tokenizer"))

        if self.config.get("terms"):
            return Tokenizer()

        return Tokenizer.tokenize

    def results(self, scores):
        """
        Resolves a list of (id, score) with document content, if available. Otherwise, the original input is returned.

        Args:
            scores: list of (id, score)

        Returns:
            resolved results
        """

        scores = [(x, float(score)) for x, score in scores]

        if self.documents:
            return [{"id": x, "text": self.documents[x], "score": score} for x, score in scores]

        return scores
