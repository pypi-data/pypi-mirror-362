"""
This module provides the Terms class for reducing query statements to keyword terms.
"""


class Terms:
    """
    Reduces a query statement down to keyword terms, extracting query text from similar clauses or returning the original query.

    Args:
        embeddings (Embeddings): Embeddings instance to extract terms from.
    """

    def __init__(self, embeddings):
        """
        Create a new terms action.

        Args:
            embeddings: embeddings instance
        """

        self.database = embeddings.database

    def __call__(self, queries):
        """
        Extracts keyword terms from a list of queries.

        Args:
            queries: list of queries

        Returns:
            list of queries reduced down to keyword term strings
        """

        if self.database:
            terms = []
            for query in queries:
                parse = self.database.parse(query)

                terms.append(" ".join(" ".join(s) for s in parse["similar"]))

            return terms

        return queries
