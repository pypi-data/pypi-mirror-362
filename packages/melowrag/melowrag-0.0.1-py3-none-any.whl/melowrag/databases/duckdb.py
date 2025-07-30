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
import re
from tempfile import TemporaryDirectory

try:
    import duckdb

    DUCKDB = True
except ImportError:
    DUCKDB = False

from .db_schema import Statement
from .embedded import Embedded


class DuckDB(Embedded):
    """
    Database instance backed by DuckDB.
    """

    DELETE_DOCUMENT = "DELETE FROM documents WHERE id = ?"
    DELETE_OBJECT = "DELETE FROM objects WHERE id = ?"

    def __init__(self, config):
        super().__init__(config)

        if not DUCKDB:
            raise ImportError('DuckDB is not available - install "database" extra to enable')

    def execute(self, function, *args):
        return super().execute(function, *self.formatargs(args))

    def insertdocument(self, uid, data, tags, entry):
        self.cursor.execute(DuckDB.DELETE_DOCUMENT, [uid])

        super().insertdocument(uid, data, tags, entry)

    def insertobject(self, uid, data, tags, entry):
        self.cursor.execute(DuckDB.DELETE_OBJECT, [uid])

        super().insertobject(uid, data, tags, entry)

    def connect(self, path=":memory:"):
        # pylint: disable=I1101
        connection = duckdb.connect(path)
        connection.begin()

        return connection

    def getcursor(self):
        return self.connection

    def jsonprefix(self):
        return "json_extract_string(data"

    def jsoncolumn(self, name):
        return f"json_extract_string(data, '$.{name}')"

    def rows(self):
        batch = 256
        rows = self.cursor.fetchmany(batch)
        while rows:
            yield from rows
            rows = self.cursor.fetchmany(batch)

    def addfunctions(self):
        return

    def copy(self, path):
        if os.path.exists(path):
            os.remove(path)

        # pylint: disable=I1101
        connection = duckdb.connect(path)

        tables = ["documents", "objects", "sections"]

        with TemporaryDirectory() as directory:
            for table in tables:
                self.connection.execute(f"COPY {table} TO '{directory}/{table}.parquet' (FORMAT parquet)")

            for schema in [Statement.CREATE_DOCUMENTS, Statement.CREATE_OBJECTS, Statement.CREATE_SECTIONS % "sections"]:
                connection.execute(schema)

            for table in tables:
                connection.execute(f"COPY {table} FROM '{directory}/{table}.parquet' (FORMAT parquet)")

            connection.execute(Statement.CREATE_SECTIONS_INDEX)
            connection.execute("CHECKPOINT")

        connection.begin()

        return connection

    def formatargs(self, args):
        """
        DuckDB doesn't support named parameters. This method replaces named parameters with question marks
        and makes parameters a list.

        Args:
            args: input arguments

        Returns:
            DuckDB compatible args
        """

        if args and len(args) > 1:
            query, parameters = args

            params = []
            for key, value in parameters.items():
                pattern = rf"\:{key}(?=\s|$)"
                match = re.search(pattern, query)
                if match:
                    query = re.sub(pattern, "?", query, count=1)
                    params.append((match.start(), value))

            args = (query, [value for _, value in sorted(params, key=lambda x: x[0])])

        return args
