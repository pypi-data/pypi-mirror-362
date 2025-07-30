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
import time

try:
    from sqlalchemy import StaticPool, Text, cast, create_engine, insert
    from sqlalchemy import text as textsql
    from sqlalchemy.orm import Session, aliased
    from sqlalchemy.schema import CreateSchema

    from .db_schema import Base, Batch, Document, Object, Score, Section, SectionBase

    ORM = True
except ImportError:
    ORM = False

from .rdbms import RDBMS


class Client(RDBMS):
    """
    Database client instance. This class connects to an external database using SQLAlchemy. It supports any database
    that is supported by SQLAlchemy (PostgreSQL, MariaDB, etc) and has JSON support.
    """

    def __init__(self, config):
        """
        Creates a new Database.

        Args:
            config: database configuration parameters
        """

        super().__init__(config)

        if not ORM:
            raise ImportError('SQLAlchemy is not available - install "database" extra to enable')

        self.engine, self.dbconnection = None, None

    def save(self, path):
        super().save(path)

        if self.dbconnection:
            self.dbconnection.commit()

    def close(self):
        super().close()

        if self.engine:
            self.engine.dispose()

    def reindexstart(self):
        name = f"rebuild{round(time.time() * 1000)}"

        type("Rebuild", (SectionBase,), {"__tablename__": name})
        Base.metadata.tables[name].create(self.dbconnection)

        return name

    def reindexend(self, name):
        Base.metadata.remove(Base.metadata.tables[name])

    def jsonprefix(self):
        return "cast("

    def jsoncolumn(self, name):
        d = aliased(Document, name="d")

        return str(
            cast(d.data[name].as_string(), Text).compile(
                dialect=self.engine.dialect, compile_kwargs={"literal_binds": True}
            )
        )

    def createtables(self):
        Base.metadata.create_all(self.dbconnection, checkfirst=True)

        for table in ["sections", "documents", "objects"]:
            self.cursor.execute(f"DELETE FROM {table}")

    def finalize(self):
        self.connection.flush()

    def insertdocument(self, uid, data, tags, entry):
        self.connection.add(Document(id=uid, data=data, tags=tags, entry=entry))

    def insertobject(self, uid, data, tags, entry):
        self.connection.add(Object(id=uid, object=data, tags=tags, entry=entry))

    def insertsection(self, index, uid, text, tags, entry):
        self.connection.add(Section(indexid=index, id=uid, text=text, tags=tags, entry=entry))

    def createbatch(self):
        Base.metadata.tables["batch"].create(self.dbconnection, checkfirst=True)

    def insertbatch(self, indexids, ids, batch):
        if indexids:
            self.connection.execute(insert(Batch), [{"indexid": i, "batch": batch} for i in indexids])
        if ids:
            self.connection.execute(insert(Batch), [{"id": str(uid), "batch": batch} for uid in ids])

    def createscores(self):
        Base.metadata.tables["scores"].create(self.dbconnection, checkfirst=True)

    def insertscores(self, scores):
        if scores:
            self.connection.execute(insert(Score), [{"indexid": i, "score": sum(s) / len(s)} for i, s in scores.items()])

    def connect(self, path=None):
        content = self.config.get("content")

        content = os.environ.get("CLIENT_URL") if content == "client" else content

        self.engine = create_engine(content, poolclass=StaticPool, echo=False, json_serializer=lambda x: x)
        self.dbconnection = self.engine.connect()

        database = Session(self.dbconnection)

        schema = self.config.get("schema")
        if schema:
            with self.engine.begin():
                self.sqldialect(database, CreateSchema(schema, if_not_exists=True))

            self.sqldialect(database, textsql("SET search_path TO :schema"), {"schema": schema})

        return database

    def getcursor(self):
        return Cursor(self.connection)

    def rows(self):
        return self.cursor

    def addfunctions(self):
        return

    def sqldialect(self, database, sql, parameters=None):
        """
        Executes a SQL statement based on the current SQL dialect.

        Args:
            database: current database
            sql: SQL to execute
            parameters: optional bind parameters
        """

        args = (sql, parameters) if self.engine.dialect.name == "postgresql" else (textsql("SELECT 1"),)
        database.execute(*args)


class Cursor:
    """
    Implements basic compatibility with the Python DB-API.
    """

    def __init__(self, connection):
        self.connection = connection
        self.result = None

    def __iter__(self):
        return self.result

    def execute(self, statement, parameters=None):
        """
        Executes statement.

        Args:
            statement: statement to execute
            parameters: optional dictionary with bind parameters
        """

        if isinstance(statement, str):
            statement = textsql(statement)

        self.result = self.connection.execute(statement, parameters)

    def fetchall(self):
        """
        Fetches all rows from the current result.

        Returns:
            all rows from current result
        """

        return self.result.all() if self.result else None

    def fetchone(self):
        """
        Fetches first row from current result.

        Returns:
            first row from current result
        """

        return self.result.first() if self.result else None

    @property
    def description(self):
        """
        Returns columns for current result.

        Returns:
            list of columns
        """

        return [(key,) for key in self.result.keys()] if self.result else None
