import json
import os
import tempfile
import uuid

import numpy as np

from ..pipelines import Tokenizer
from .recovery import Recovery


class Vectors:
    """
    Base class for vector models. Vector models transform input content into numeric vectors.
    """

    def __init__(self, config, scoring, models):
        """
        Creates a new vectors instance.

        Args:
            config: vector configuration
            scoring: optional scoring instance for term weighting
            models: models cache
        """

        self.config = config
        self.scoring = scoring
        self.models = models

        if config:
            self.initialized = "dimensions" in config

            self.tokenize = config.get("tokenize")

            self.model = self.load(config.get("path"))

            self.encodebatch = config.get("encodebatch", 32)

            self.instructions = config.get("instructions")

            self.dimensionality = config.get("dimensionality")

            quantize = config.get("quantize")
            self.qbits = (
                max(min(quantize, 8), 1) if isinstance(quantize, int) and not isinstance(quantize, bool) else None
            )

    def loadmodel(self, path):
        """
        Loads vector model at path.

        Args:
            path: path to vector model

        Returns:
            vector model
        """

        raise NotImplementedError

    def encode(self, data, category=None):
        """
        Encodes a batch of data using vector model.

        Args:
            data: batch of data
            category: optional category for instruction-based embeddings

        Return:
            transformed data
        """

        raise NotImplementedError

    def load(self, path):
        """
        Loads a model using the current configuration. This method will return previously cached models
        if available.

        Returns:
            model
        """

        if self.models and path in self.models:
            return self.models[path]

        model = self.loadmodel(path)

        if self.models is not None and path:
            self.models[path] = model

        return model

    def index(self, documents, batchsize=500, checkpoint=None):
        """
        Converts a list of documents to a temporary file with embeddings arrays. Returns a tuple of document ids,
        number of dimensions and temporary file with embeddings.

        Args:
            documents: list of (id, data, tags)
            batchsize: index batch size
            checkpoint: optional checkpoint directory, enables indexing restart

        Returns:
            (ids, dimensions, batches, stream)
        """

        ids, dimensions, batches, stream = [], None, 0, None

        vectorsid = self.vectorsid() if checkpoint else None
        recovery = Recovery(checkpoint, vectorsid, self.loadembeddings) if checkpoint else None

        with self.spool(checkpoint, vectorsid) as output:
            stream = output.name
            batch = []
            for document in documents:
                batch.append(document)

                if len(batch) == batchsize:
                    uids, dimensions = self.batch(batch, output, recovery)
                    ids.extend(uids)
                    batches += 1

                    batch = []

            if batch:
                uids, dimensions = self.batch(batch, output, recovery)
                ids.extend(uids)
                batches += 1

        return (ids, dimensions, batches, stream)

    def vectors(self, documents, batchsize=500, checkpoint=None, buffer=None, dtype=None):
        """
        Bulk encodes documents into vectors using index(). Return the data as a mmap-ed array.

        Args:
            documents: list of (id, data, tags)
            batchsize: index batch size
            checkpoint: optional checkpoint directory, enables indexing restart
            buffer: file path used for memmap buffer
            dtype: dtype for buffer

        Returns:
            (ids, dimensions, embeddings)
        """

        ids, dimensions, batches, stream = self.index(documents, batchsize, checkpoint)

        embeddings = None
        if ids:
            embeddings = np.memmap(buffer, dtype=dtype, shape=(len(ids), dimensions), mode="w+")
            with open(stream, "rb") as queue:
                x = 0
                for _ in range(batches):
                    batch = self.loadembeddings(queue)
                    embeddings[x : x + batch.shape[0]] = batch
                    x += batch.shape[0]

        if not checkpoint:
            os.remove(stream)

        return (ids, dimensions, embeddings)

    def close(self):
        """
        Closes this vectors instance.
        """

        self.model = None

    def transform(self, document):
        """
        Transforms document into an embeddings vector.

        Args:
            document: (id, data, tags)

        Returns:
            embeddings vector
        """

        return self.batchtransform([document])[0]

    def batchtransform(self, documents, category=None):
        """
        Transforms batch of documents into embeddings vectors.

        Args:
            documents: list of documents used to build embeddings
            category: category for instruction-based embeddings

        Returns:
            embeddings vectors
        """

        documents = [self.prepare(data, category) for _, data, _ in documents]

        if documents and isinstance(documents[0], np.ndarray):
            return np.array(documents, dtype=np.float32)

        return self.vectorize(documents, category)

    def dot(self, queries, data):
        """
        Calculates the dot product similarity between queries and documents. This method
        assumes each of the inputs are normalized.

        Args:
            queries: queries
            data: search data

        Returns:
            dot product scores
        """

        return np.dot(queries, data.T).tolist()

    def vectorsid(self):
        """
        Generates vectors uid for this vectors instance.

        Returns:
            vectors uid
        """

        select = ["path", "method", "tokenizer", "maxlength", "tokenize", "instructions", "dimensionality", "quantize"]
        config = {k: v for k, v in self.config.items() if k in select}
        config.update(self.config.get("vectors", {}))

        return str(uuid.uuid5(uuid.NAMESPACE_DNS, json.dumps(config, sort_keys=True)))

    def spool(self, checkpoint, vectorsid):
        """
        Opens a spool file for queuing generated vectors.

        Args:
            checkpoint: optional checkpoint directory, enables indexing restart
            vectorsid: vectors uid for current configuration

        Returns:
            vectors spool file
        """

        if checkpoint:
            os.makedirs(checkpoint, exist_ok=True)
            return open(f"{checkpoint}/{vectorsid}", "wb")

        return tempfile.NamedTemporaryFile(mode="wb", suffix=".npy", delete=False)

    def batch(self, documents, output, recovery):
        """
        Builds a batch of embeddings.

        Args:
            documents: list of documents used to build embeddings
            output: output temp file to store embeddings
            recovery: optional recovery instance

        Returns:
            (ids, dimensions) list of ids and number of dimensions in embeddings
        """

        ids = [uid for uid, _, _ in documents]
        documents = [self.prepare(data, "data") for _, data, _ in documents]
        dimensions = None

        embeddings = recovery() if recovery else None
        embeddings = self.vectorize(documents, "data") if embeddings is None else embeddings
        if embeddings is not None:
            dimensions = embeddings.shape[1]
            self.saveembeddings(output, embeddings)

        return (ids, dimensions)

    def prepare(self, data, category=None):
        """
        Prepares input data for vector model.

        Args:
            data: input data
            category: category for instruction-based embeddings

        Returns:
            data formatted for vector model
        """

        data = self.tokens(data)

        category = category if category else "query"

        if self.instructions and category in self.instructions and isinstance(data, str):
            data = f"{self.instructions[category]}{data}"

        return data

    def tokens(self, data):
        """
        Prepare data as tokens model can accept.

        Args:
            data: input data

        Returns:
            tokens formatted for model
        """

        if self.tokenize and isinstance(data, str):
            data = Tokenizer.tokenize(data)

        if isinstance(data, list):
            data = " ".join(data)

        return data

    def vectorize(self, data, category=None):
        """
        Runs data vectorization, which consists of the following steps.

          1. Encode data into vectors using underlying model
          2. Truncate vectors, if necessary
          3. Normalize vectors
          4. Quantize vectors, if necessary

        Args:
            data: input data
            category: category for instruction-based embeddings

        Returns:
            embeddings vectors
        """

        category = category if category else "query"

        embeddings = self.encode(data, category)

        if embeddings is not None:
            if self.dimensionality and self.dimensionality < embeddings.shape[1]:
                embeddings = self.truncate(embeddings)

            embeddings = self.normalize(embeddings)

            if self.qbits:
                embeddings = self.quantize(embeddings)

        return embeddings

    def loadembeddings(self, f):
        """
        Loads embeddings from file.

        Args:
            f: file to load from

        Returns:
            embeddings
        """

        return np.load(f, allow_pickle=False)

    def saveembeddings(self, f, embeddings):
        """
        Saves embeddings to output.

        Args:
            f: output file
            embeddings: embeddings to save
        """

        np.save(f, embeddings, allow_pickle=False)

    def truncate(self, embeddings):
        """
        Truncates embeddings to the configured dimensionality.

        This is only useful for models trained to store more important information in
        earlier dimensions such as Matryoshka Representation Learning (MRL).

        Args:
            embeddings: input embeddings

        Returns:
            truncated embeddings
        """

        return embeddings[:, : self.dimensionality]

    def normalize(self, embeddings):
        """
        Normalizes embeddings using L2 normalization. Operation applied directly on array.

        Args:
            embeddings: input embeddings

        Returns:
            embeddings
        """

        if len(embeddings.shape) > 1:
            embeddings /= np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
        else:
            embeddings /= np.linalg.norm(embeddings)

        return embeddings

    def quantize(self, embeddings):
        """
        Quantizes embeddings using scalar quantization.

        Args:
            embeddings: input embeddings

        Returns:
            quantized embeddings
        """

        factor = 2 ** (self.qbits - 1)

        scalars = embeddings * factor
        scalars = scalars.clip(-factor, factor - 1) + factor
        scalars = scalars.astype(np.uint8)

        bits = np.unpackbits(scalars.reshape(-1, 1), axis=1)

        bits = bits[:, -self.qbits :]

        return np.packbits(bits.reshape(embeddings.shape[0], embeddings.shape[1] * self.qbits), axis=1)

    def __repr__(self):
        """
        Returns a detailed string representation of the Vectors instance.

        Returns:
            Detailed string representation
        """
        class_name = self.__class__.__name__
        config_info = {}
        if hasattr(self, "config") and self.config:
            config_info.update(
                {
                    "path": self.config.get("path"),
                    "method": self.config.get("method"),
                    "tokenize": getattr(self, "tokenize", None),
                    "encodebatch": getattr(self, "encodebatch", None),
                    "dimensionality": getattr(self, "dimensionality", None),
                    "quantize": getattr(self, "qbits", None),
                    "instructions": bool(getattr(self, "instructions", None)),
                }
            )
        config_info = {k: v for k, v in config_info.items() if v is not None}
        status = "initialized" if getattr(self, "initialized", False) else "uninitialized"
        return f"{class_name}({config_info}, status={status})"

    def __str__(self):
        """
        Returns a user-friendly string representation of the Vectors instance.

        Returns:
            User-friendly string representation
        """
        class_name = self.__class__.__name__
        details = []
        if hasattr(self, "config") and self.config:
            if self.config.get("path"):
                details.append(f"model_path='{self.config['path']}'")
            if self.config.get("method"):
                details.append(f"method='{self.config['method']}'")
        if hasattr(self, "dimensionality") and self.dimensionality:
            details.append(f"dimensions={self.dimensionality}")
        if hasattr(self, "encodebatch") and self.encodebatch:
            details.append(f"batch_size={self.encodebatch}")
        if hasattr(self, "tokenize") and self.tokenize:
            details.append("tokenized")
        if hasattr(self, "qbits") and self.qbits:
            details.append(f"quantized({self.qbits}bits)")
        if hasattr(self, "instructions") and self.instructions:
            details.append("instruction-based")
        status = "✓" if getattr(self, "initialized", False) else "✗"
        details_str = ", ".join(details) if details else "default"
        return f"{class_name}({details_str}) [{status}]"
