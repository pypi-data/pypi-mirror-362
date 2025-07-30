import os

try:
    from pgvector import SparseVector
    from pgvector.sqlalchemy import SPARSEVEC

    PGSPARSE = True
except ImportError:
    PGSPARSE = False

from ..dense_index import PGVector


class PGSparse(PGVector):
    """
    Builds a Sparse VectoreIndex index backed by a Postgres database.
    """

    def __init__(self, config):
        if not PGSPARSE:
            raise ImportError('PGSparse is not available - install "ann" extra to enable')

        super().__init__(config)

        self.qbits = None

    def defaulttable(self):
        return "svectors"

    def url(self):
        return self.setting("url", os.environ.get("SCORING_URL", os.environ.get("ANN_URL")))

    def column(self):
        return SPARSEVEC(self.config["dimensions"]), "sparsevec_ip_ops"

    def prepare(self, data):
        return SparseVector(data)
