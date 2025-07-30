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
import sqlite3

try:
    import sqlite_vec  # type:ignore

    SQLITEVEC = True
except ImportError:
    SQLITEVEC = False

from ..base import VectoreIndex


class SQLite(VectoreIndex):
    """
    Builds an VectoreIndex index backed by a SQLite database.
    """

    def __init__(self, config):
        super().__init__(config)

        if not SQLITEVEC:
            raise ImportError('sqlite-vec is not available - install "ann" extra to enable')

        self.connection, self.cursor, self.path = None, None, ""

        self.quantize = self.setting("quantize")
        self.quantize = 8 if isinstance(self.quantize, bool) else int(self.quantize) if self.quantize else None

    def load(self, path):
        self.path = path

    def index(self, embeddings):
        self.initialize(recreate=True)

        self.database().executemany(self.insertsql(), enumerate(embeddings))

        self.config["offset"] = embeddings.shape[0]
        self.metadata(self.settings())

    def append(self, embeddings):
        self.database().executemany(
            self.insertsql(), [(x + self.config["offset"], row) for x, row in enumerate(embeddings)]
        )

        self.config["offset"] += embeddings.shape[0]
        self.metadata()

    def delete(self, ids):
        self.database().executemany(self.deletesql(), [(x,) for x in ids])

    def search(self, queries, limit):
        results = []
        for query in queries:
            self.database().execute(self.searchsql(), [query, limit])

            results.append(list(self.database()))

        return results

    def count(self):
        self.database().execute(self.countsql())
        return self.cursor.fetchone()[0]

    def save(self, path):
        if not self.path:
            self.connection.commit()

            connection = self.copy(path)

            self.connection.close()

            self.connection = connection
            self.cursor = self.connection.cursor()
            self.path = path

        elif self.path == path:
            self.connection.commit()

        else:
            self.copy(path).close()

    def close(self):
        super().close()

        if self.connection:
            self.connection.close()
            self.connection = None

    def initialize(self, recreate=False):
        """
        Initializes a new database session.

        Args:
            recreate: Recreates the database tables if True
        """

        self.database().execute(self.tablesql())

        if recreate:
            self.database().execute(self.tosql("DELETE FROM {table}"))

    def settings(self):
        """
        Returns settings for this index.

        Returns:
            dict
        """

        sqlite, sqlitevec = self.database().execute("SELECT sqlite_version(), vec_version()").fetchone()

        return {"sqlite": sqlite, "sqlite-vec": sqlitevec}

    def database(self):
        """
        Gets the current database cursor. Creates a new connection
        if there isn't one.

        Returns:
            cursor
        """

        if not self.connection:
            self.connection = self.connect(self.path)
            self.cursor = self.connection.cursor()

        return self.cursor

    def connect(self, path):
        """
        Creates a new database connection.

        Args:
            path: path to database file

        Returns:
            database connection
        """

        connection = sqlite3.connect(path, check_same_thread=False)

        connection.enable_load_extension(True)
        sqlite_vec.load(connection)
        connection.enable_load_extension(False)

        return connection

    def copy(self, path):
        """
        Copies content from the current database into target.

        Args:
            path: target database path

        Returns:
            new database connection
        """

        if os.path.exists(path):
            os.remove(path)

        connection = self.connect(path)

        if self.connection.in_transaction:
            connection.execute(self.tablesql())

            for sql in self.connection.iterdump():
                if self.tosql('insert into "{table}"') in sql.lower():
                    connection.execute(sql)
        else:
            self.connection.backup(connection)

        return connection

    def tablesql(self):
        """
        Builds a CREATE table statement for table.

        Returns:
            CREATE TABLE
        """

        if self.quantize == 1:
            embedding = f"embedding BIT[{self.config['dimensions']}]"

        elif self.quantize == 8:
            embedding = f"embedding INT8[{self.config['dimensions']}] distance=cosine"

        else:
            embedding = f"embedding FLOAT[{self.config['dimensions']}] distance=cosine"

        return self.tosql(
            f"CREATE VIRTUAL TABLE IF NOT EXISTS {{table}} USING vec0(indexid INTEGER PRIMARY KEY, {embedding})"
        )

    def insertsql(self):
        """
        Creates an INSERT SQL statement.

        Returns:
            INSERT
        """

        return self.tosql(f"INSERT INTO {{table}}(indexid, embedding) VALUES (?, {self.embeddingsql()})")

    def deletesql(self):
        """
        Creates a DELETE SQL statement.

        Returns:
            DELETE
        """

        return self.tosql("DELETE FROM {table} WHERE indexid = ?")

    def searchsql(self):
        """
        Creates a SELECT SQL statement for search.

        Returns:
            SELECT
        """

        return self.tosql(
            "SELECT indexid, 1 - distance FROM {table} "
            f"WHERE embedding MATCH {self.embeddingsql()} AND k = ? ORDER BY distance"
        )

    def countsql(self):
        """
        Creates a SELECT COUNT statement.

        Returns:
            SELECT COUNT
        """

        return self.tosql("SELECT count(indexid) FROM {table}")

    def embeddingsql(self):
        """
        Creates an embeddings column SQL snippet.

        Returns:
            embeddings column SQL
        """

        if self.quantize == 1:
            embedding = "vec_quantize_binary(?)"

        elif self.quantize == 8:
            embedding = "vec_quantize_int8(?, 'unit')"

        else:
            embedding = "?"

        return embedding

    def tosql(self, sql):
        """
        Creates a SQL statement substituting in the configured table name.

        Args:
            sql: SQL statement with a {table} parameter

        Returns:
            fully resolved SQL statement
        """

        table = self.setting("table", "vectors")
        return sql.format(table=table)
