"""
This module provides the Explain class for analyzing the importance of each token in input texts for a query.
It supports permutation-based token masking to determine token importance relative to a query.
"""

import numpy as np


class Explain:
    """
    Analyzes the importance of each token in input texts for a query using permutation-based masking.

    Args:
        embeddings (Embeddings): Embeddings instance to use for similarity and scoring.
    """

    def __init__(self, embeddings):
        """
        Creates a new explain action.

        Args:
            embeddings: embeddings instance
        """

        self.embeddings = embeddings
        self.content = embeddings.config.get("content")

        self.database = embeddings.database

    def __call__(self, queries, texts, limit):
        """
        Explains the importance of each input token in text for a list of queries.

        Args:
            query: input queries
            texts: optional list of (text|list of tokens), otherwise runs search queries
            limit: optional limit if texts is None

        Returns:
            list of dict per input text per query where a higher token scores
            represents higher importance relative to the query
        """

        texts = self.texts(queries, texts, limit)

        return [self.explain(query, texts[x]) for x, query in enumerate(queries)]

    def texts(self, queries, texts, limit):
        """
        Constructs lists of dict for each input query.

        Args:
            queries: input queries
            texts: optional list of texts
            limit: optional limit if texts is None

        Returns:
            lists of dict for each input query
        """

        if texts:
            results = []
            for scores in self.embeddings.batchsimilarity(queries, texts):
                results.append([{"id": uid, "text": texts[uid], "score": score} for uid, score in scores])

            return results

        return self.embeddings.batchsearch(queries, limit) if self.content else [[]] * len(queries)

    def explain(self, query, texts):
        """
        Explains the importance of each input token in text for a list of queries.

        Args:
            query: input query
            texts: list of text

        Returns:
            list of {"id": value, "text": value, "score": value, "tokens": value} covering each input text element
        """

        results = []

        if self.database:
            query = self.database.parse(query)

            query = " ".join([" ".join(clause) for clause in query["similar"]]) if "similar" in query else None

        if not query or not texts or "score" not in texts[0] or "text" not in texts[0]:
            return texts

        for result in texts:
            text = result["text"]
            tokens = text if isinstance(text, list) else text.split()

            permutations = []
            for i in range(len(tokens)):
                data = tokens.copy()
                data.pop(i)
                permutations.append([" ".join(data)])

            scores = [(i, result["score"] - np.abs(s)) for i, s in self.embeddings.similarity(query, permutations)]

            result["tokens"] = [(tokens[i], score) for i, score in sorted(scores, key=lambda x: x[0])]

            results.append(result)

        return sorted(results, key=lambda x: x["score"], reverse=True)
