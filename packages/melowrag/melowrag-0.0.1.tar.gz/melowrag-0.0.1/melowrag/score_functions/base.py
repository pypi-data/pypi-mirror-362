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

class Scoring:
    """
    Base scoring.
    """

    def __init__(self, config=None):
        """
        Creates a new Scoring instance.

        Args:
            config: input configuration
        """

        self.config = config if config is not None else {}

        columns = self.config.get("columns", {})
        self.text = columns.get("text", "text")
        self.object = columns.get("object", "object")

        self.model = None

    def insert(self, documents, index=None, checkpoint=None):
        """
        Inserts documents into the scoring index.

        Args:
            documents: list of (id, dict|text|tokens, tags)
            index: indexid offset
            checkpoint: optional checkpoint directory, enables indexing restart
        """

        raise NotImplementedError

    def delete(self, ids):
        """
        Deletes documents from scoring index.

        Args:
            ids: list of ids to delete
        """

        raise NotImplementedError

    def index(self, documents=None):
        """
        Indexes a collection of documents using a scoring method.

        Args:
            documents: list of (id, dict|text|tokens, tags)
        """

        if documents:
            self.insert(documents)

    def upsert(self, documents=None):
        """
        Convience method for API clarity. Calls index method.

        Args:
            documents: list of (id, dict|text|tokens, tags)
        """

        self.index(documents)

    def weights(self, tokens):
        """
        Builds a weights vector for each token in input tokens.

        Args:
            tokens: input tokens

        Returns:
            list of weights for each token
        """

        raise NotImplementedError

    def search(self, query, limit=3):
        """
        Search index for documents matching query.

        Args:
            query: input query
            limit: maximum results

        Returns:
            list of (id, score) or (data, score) if content is enabled
        """

        raise NotImplementedError

    def batchsearch(self, queries, limit=3, threads=True):
        """
        Search index for documents matching queries.

        Args:
            queries: queries to run
            limit: maximum results
            threads: run as threaded search if True and supported
        """

        raise NotImplementedError

    def count(self):
        """
        Returns the total number of documents indexed.

        Returns:
            total number of documents indexed
        """

        raise NotImplementedError

    def load(self, path):
        """
        Loads a saved Scoring object from path.

        Args:
            path: directory path to load scoring index
        """

        raise NotImplementedError

    def save(self, path):
        """
        Saves a Scoring object to path.

        Args:
            path: directory path to save scoring index
        """

        raise NotImplementedError

    def close(self):
        """
        Closes this Scoring object.
        """

        raise NotImplementedError

    def findmodel(self):
        """
        Returns the associated vector model used by this scoring instance, if any.

        Returns:
            associated vector model
        """

        return self.model

    def issparse(self):
        """
        Check if this scoring instance has an associated sparse keyword or sparse vector index.

        Returns:
            True if this index has an associated sparse index
        """

        raise NotImplementedError

    def isweighted(self):
        """
        Check if this scoring instance is for term weighting (i.e.) it has no associated sparse index.

        Returns:
            True if this index is for term weighting
        """

        return not self.issparse()

    def isnormalized(self):
        """
        Check if this scoring instance returns normalized scores.

        Returns:
            True if normalize is enabled, False otherwise
        """

        raise NotImplementedError
