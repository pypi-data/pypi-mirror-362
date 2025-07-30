import numpy as np

from .action import Action


class Transform:
    """
    Executes a transform. Processes a stream of documents, loads batches into enabled data stores
    and vectorizes documents.
    """

    def __init__(self, embeddings, action, checkpoint=None):
        """
        Creates a new transform.

        Args:
            embeddings: embeddings instance
            action: index action
            checkpoint: optional checkpoint directory, enables indexing restart
        """

        self.embeddings = embeddings
        self.action = action
        self.checkpoint = checkpoint

        self.config = embeddings.config
        self.delete = embeddings.delete
        self.model = embeddings.model
        self.database = embeddings.database
        self.graph = embeddings.graph
        self.indexes = embeddings.indexes
        self.scoring = embeddings.scoring if embeddings.issparse() else None

        self.offset = embeddings.config.get("offset", 0) if action == Action.UPSERT else 0
        self.batch = embeddings.config.get("batch", 1024)

        quantize = embeddings.config.get("quantize")
        self.qbits = quantize if isinstance(quantize, int) and not isinstance(quantize, bool) else None

        columns = embeddings.config.get("columns", {})
        self.text = columns.get("text", "text")
        self.object = columns.get("object", "object")

        self.indexing = embeddings.model or embeddings.scoring

        self.deletes = set()

    def __call__(self, documents, buffer):
        """
        Processes an iterable collection of documents, handles any iterable including generators.

        This method loads a stream of documents into enabled data stores and vectorizes
        documents into an embeddings array.

        Args:
            documents: iterable of (id, data, tags)
            buffer: file path used for memmap buffer

        Returns:
            (document ids, dimensions, embeddings)
        """

        ids, dimensions, embeddings = None, None, None

        if self.model:
            ids, dimensions, embeddings = self.vectors(documents, buffer)
        else:
            ids = self.ids(documents)

        return (ids, dimensions, embeddings)

    def vectors(self, documents, buffer):
        """
        Runs a vectors transform operation when dense indexing is enabled.

        Args:
            documents: iterable of (id, data, tags)
            buffer: file path used for memmap buffer

        Returns:
            (document ids, dimensions, embeddings)
        """

        dtype = np.uint8 if self.qbits else np.float32

        return self.model.vectors(self.stream(documents), self.batch, self.checkpoint, buffer, dtype)

    def ids(self, documents):
        """
        Runs an ids transform operation when dense indexing is disabled.

        Args:
            documents: iterable of (id, data, tags)

        Returns:
            document ids
        """

        ids = []
        for uid, _, _ in self.stream(documents):
            ids.append(uid)

        self.config["offset"] = self.offset

        return ids

    def stream(self, documents):
        """
        This method does two things:

        1. Filter and yield data to vectorize
        2. Batch and load original documents into enabled data stores (database, graph, scoring)

        Documents are yielded for vectorization if one of the following is True:
            - dict with a text or object field
            - not a dict

        Otherwise, documents are only batched and inserted into data stores

        Args:
            documents: iterable collection (id, data, tags)
        """

        batch, offset = [], 0

        for document in documents:
            if isinstance(document[1], dict):
                if not self.indexing and not document[1].get(self.text):
                    document[1][self.text] = str(document[0])

                if self.text in document[1]:
                    yield (document[0], document[1][self.text], document[2])
                    offset += 1
                elif self.object in document[1]:
                    yield (document[0], document[1][self.object], document[2])
                    offset += 1
            else:
                yield document
                offset += 1

            batch.append(document)
            if len(batch) == self.batch:
                self.load(batch, offset)
                batch, offset = [], 0

        if batch:
            self.load(batch, offset)

    def load(self, batch, offset):
        """
        Loads a document batch. This method deletes existing ids from an embeddings index and
        loads into enabled data stores (database, graph, scoring).

        Args:
            batch: list of (id, data, tags)
            offset: index offset for batch
        """

        if self.action == Action.UPSERT:
            deletes = [uid for uid, _, _ in batch if uid not in self.deletes]
            if deletes:
                self.delete(deletes)

                self.deletes.update(deletes)

        if self.database and self.action != Action.REINDEX:
            self.database.insert(batch, self.offset)

        if self.scoring:
            self.scoring.insert(batch, self.offset, self.checkpoint)

        if self.indexes:
            self.indexes.insert(batch, self.offset, self.checkpoint)

        if self.graph:
            self.graph.insert(batch, self.offset)

        self.offset += offset
