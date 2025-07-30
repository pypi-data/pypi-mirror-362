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
