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

import os

import numpy as np

try:
    from pgvector.sqlalchemy import BIT, HALFVEC, VECTOR
    from sqlalchemy import Column, Index, Integer, MetaData, StaticPool, Table, create_engine, delete, func, text
    from sqlalchemy.orm import Session
    from sqlalchemy.schema import CreateSchema

    PGVECTOR = True
except ImportError:
    PGVECTOR = False

from ..base import VectoreIndex


class PGVector(VectoreIndex):
    """
    Builds an VectoreIndex index backed by a Postgres database.
    """

    def __init__(self, config):
        super().__init__(config)

        if not PGVECTOR:
            raise ImportError('PGVector is not available - install "ann" extra to enable')

        self.engine, self.database, self.connection, self.table = None, None, None, None

        quantize = self.config.get("quantize")
        self.qbits = quantize if quantize and isinstance(quantize, int) and not isinstance(quantize, bool) else None

    def load(self, path):
        self.initialize()

    def index(self, embeddings):
        self.initialize(recreate=True)

        self.database.execute(
            self.table.insert(), [{"indexid": x, "embedding": self.prepare(row)} for x, row in enumerate(embeddings)]
        )

        self.config["offset"] = embeddings.shape[0]
        self.metadata(self.settings())

    def append(self, embeddings):
        self.database.execute(
            self.table.insert(),
            [{"indexid": x + self.config["offset"], "embedding": self.prepare(row)} for x, row in enumerate(embeddings)],
        )

        self.config["offset"] += embeddings.shape[0]
        self.metadata()

    def delete(self, ids):
        self.database.execute(delete(self.table).where(self.table.c["indexid"].in_(ids)))

    def search(self, queries, limit):
        results = []
        for query in queries:
            query = self.database.query(self.table.c["indexid"], self.query(query)).order_by("score").limit(limit)

            results.append([(indexid, self.score(score)) for indexid, score in query])

        return results

    def count(self):
        # pylint: disable=E1102
        return self.database.query(func.count(self.table.c["indexid"])).scalar()

    def save(self, path):
        self.database.commit()
        self.connection.commit()

    def close(self):
        super().close()

        if self.database:
            self.database.close()
            self.engine.dispose()

    def initialize(self, recreate=False):
        """
        Initializes a new database session.

        Args:
            recreate: Recreates the database tables if True
        """

        self.connect()

        self.schema()

        table = self.setting("table", self.defaulttable())

        column, index = self.column()

        self.table = Table(
            table,
            MetaData(),
            Column("indexid", Integer, primary_key=True, autoincrement=False),
            Column("embedding", column),
        )

        index = Index(
            f"{table}-index",
            self.table.c["embedding"],
            postgresql_using="hnsw",
            postgresql_with=self.settings(),
            postgresql_ops={"embedding": index},
        )

        if recreate:
            self.table.drop(self.connection, checkfirst=True)
            index.drop(self.connection, checkfirst=True)

        self.table.create(self.connection, checkfirst=True)
        index.create(self.connection, checkfirst=True)

    def connect(self):
        """
        Establishes a database connection. Cleans up any existing database connection first.
        """

        if self.database:
            self.close()

        self.engine = create_engine(self.url(), poolclass=StaticPool, echo=False)
        self.connection = self.engine.connect()

        self.database = Session(self.connection)

        self.sqldialect(text("CREATE EXTENSION IF NOT EXISTS vector"))

    def schema(self):
        """
        Sets the database schema, if available.
        """

        schema = self.setting("schema")
        if schema:
            with self.engine.begin():
                self.sqldialect(CreateSchema(schema, if_not_exists=True))

            self.sqldialect(text("SET search_path TO :schema,public"), {"schema": schema})

    def settings(self):
        """
        Returns settings for this index.

        Returns:
            dict
        """

        return {"m": self.setting("m", 16), "ef_construction": self.setting("efconstruction", 200)}

    def sqldialect(self, sql, parameters=None):
        """
        Executes a SQL statement based on the current SQL dialect.

        Args:
            sql: SQL to execute
            parameters: optional bind parameters
        """

        args = (sql, parameters) if self.engine.dialect.name == "postgresql" else (text("SELECT 1"),)
        self.database.execute(*args)

    def defaulttable(self):
        """
        Returns the default table name.

        Returns:
            default table name
        """

        return "vectors"

    def url(self):
        """
        Reads the database url parameter.

        Returns:
            database url
        """

        return self.setting("url", os.environ.get("ANN_URL"))

    def column(self):
        """
        Gets embedding column and index definitions for the current settings.

        Returns:
            embedding column definition, index definition
        """

        if self.qbits:
            return BIT(self.config["dimensions"] * 8), "bit_hamming_ops"

        if self.setting("precision") == "half":
            return HALFVEC(self.config["dimensions"]), "halfvec_ip_ops"

        return VECTOR(self.config["dimensions"]), "vector_ip_ops"

    def prepare(self, data):
        """
        Prepares data for the embeddings column. This method returns a bit string for bit vectors and
        the input data unmodified for float vectors.

        Args:
            data: input data

        Returns:
            data ready for the embeddings column
        """

        if self.qbits:
            return "".join(np.where(np.unpackbits(data), "1", "0"))

        return data

    def query(self, query):
        """
        Creates a query statement from an input query. This method uses hamming distance for bit vectors and
        the max_inner_product for float vectors.

        Args:
            query: input query

        Returns:
            query statement
        """

        query = self.prepare(query)

        if self.qbits:
            return self.table.c["embedding"].hamming_distance(query).label("score")

        return self.table.c["embedding"].max_inner_product(query).label("score")

    def score(self, score):
        """
        Calculates the index score from the input score. This method returns the hamming score
        (1.0 - (hamming distance / total number of bits)) for bit vectors and the -score for
        float vectors.

        Args:
            score: input score

        Returns:
            index score
        """

        if self.qbits:
            return min(max(0.0, 1.0 - (score / (self.config["dimensions"] * 8))), 1.0)

        return -score
