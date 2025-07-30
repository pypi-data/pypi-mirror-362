import json
import logging
import os
import tempfile
from multiprocessing import Pool

import numpy as np
from huggingface_hub.errors import HFValidationError
from transformers.utils import cached_file

try:
    from staticvectors import Database, StaticVectors  # type:ignore

    STATICVECTORS = True
except ImportError:
    STATICVECTORS = False

from ...pipelines import Tokenizer
from ..base import Vectors

logger = logging.getLogger(__name__)

# pylint: disable=W0603
PARAMETERS, VECTORS = None, None


def create(config, scoring):
    """
    Multiprocessing helper method. Creates a global embeddings object to be accessed in a new subprocess.

    Args:
        config: vector configuration
        scoring: scoring instance
    """

    global PARAMETERS
    global VECTORS

    PARAMETERS, VECTORS = (config, scoring, None), None


def transform(document):
    """
    Multiprocessing helper method. Transforms document into an embeddings vector.

    Args:
        document: (id, data, tags)

    Returns:
        (id, embedding)
    """

    global VECTORS
    if not VECTORS:
        VECTORS = WordVectors(*PARAMETERS)

    return (document[0], VECTORS.transform(document))


class WordVectors(Vectors):
    """
    Builds vectors using weighted word embeddings.
    """

    @staticmethod
    def ismodel(path):
        """
        Checks if path is a WordVectors model.

        Args:
            path: input path

        Returns:
            True if this is a WordVectors model, False otherwise
        """

        if WordVectors.isdatabase(path):
            return True

        try:
            path = cached_file(path_or_repo_id=path, filename="config.json")
            if path:
                with open(path, encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("model_type") == "staticvectors"

        except (HFValidationError, OSError):
            pass

        return False

    @staticmethod
    def isdatabase(path):
        """
        Checks if this is a SQLite database file which is the file format used for word vectors databases.

        Args:
            path: path to check

        Returns:
            True if this is a SQLite database
        """

        return isinstance(path, str) and STATICVECTORS and Database.isdatabase(path)

    def __init__(self, config, scoring, models):
        if not STATICVECTORS:
            raise ImportError('staticvectors is not available - install "vectors" extra to enable')

        super().__init__(config, scoring, models)

    def loadmodel(self, path):
        return StaticVectors(path)

    def encode(self, data, category=None):
        embeddings = []
        for tokens in data:
            if isinstance(tokens, str):
                tokenlist = Tokenizer.tokenize(tokens)
                tokens = tokenlist if tokenlist else [tokens]

            weights = self.scoring.weights(tokens) if self.scoring else None

            # pylint: disable=E1133
            if weights and [x for x in weights if x > 0]:
                embedding = np.average(self.lookup(tokens), weights=np.array(weights, dtype=np.float32), axis=0)
            else:
                embedding = np.mean(self.lookup(tokens), axis=0)

            embeddings.append(embedding)

        return np.array(embeddings, dtype=np.float32)

    def index(self, documents, batchsize=500, checkpoint=None):
        parallel = self.config.get("parallel", True)
        parallel = os.cpu_count() if parallel and isinstance(parallel, bool) else int(parallel)

        if not parallel:
            return super().index(documents, batchsize)

        ids, dimensions, batches, stream = [], None, 0, None

        args = (self.config, self.scoring)

        with Pool(parallel, initializer=create, initargs=args) as pool:
            with tempfile.NamedTemporaryFile(mode="wb", suffix=".npy", delete=False) as output:
                stream = output.name
                embeddings = []
                for uid, embedding in pool.imap(transform, documents, self.encodebatch):
                    if not dimensions:
                        dimensions = embedding.shape[0]

                    ids.append(uid)
                    embeddings.append(embedding)

                    if len(embeddings) == batchsize:
                        np.save(output, np.array(embeddings, dtype=np.float32), allow_pickle=False)
                        batches += 1

                        embeddings = []

                if embeddings:
                    np.save(output, np.array(embeddings, dtype=np.float32), allow_pickle=False)
                    batches += 1

        return (ids, dimensions, batches, stream)

    def lookup(self, tokens):
        """
        Queries word vectors for given list of input tokens.

        Args:
            tokens: list of tokens to query

        Returns:
            word vectors array
        """

        return self.model.embeddings(tokens)

    def tokens(self, data):
        return data
