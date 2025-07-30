import os

try:
    from sqlalchemy import (
        Column,
        Computed,
        Index,
        Integer,
        MetaData,
        StaticPool,
        Table,
        Text,
        create_engine,
        delete,
        desc,
        func,
        text,
    )
    from sqlalchemy.dialects.postgresql import TSVECTOR
    from sqlalchemy.orm import Session
    from sqlalchemy.schema import CreateSchema

    PGTEXT = True
except ImportError:
    PGTEXT = False

from .base import Scoring


class PGText(Scoring):
    """
    Postgres full text search (FTS) based scoring.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if not PGTEXT:
            raise ImportError('PGText is not available - install "scoring" extra to enable')

        self.engine, self.database, self.connection, self.table = None, None, None, None

        self.language = self.config.get("language", "english")

    def insert(self, documents, index=None, checkpoint=None):
        self.initialize(recreate=True)

        rows = []

        for uid, document, _ in documents:
            if isinstance(document, dict):
                document = document.get(self.text, document.get(self.object))

            if document is not None:
                uid = index if index is not None else uid

                if isinstance(document, str | list):
                    rows.append((uid, " ".join(document) if isinstance(document, list) else document))

                index = index + 1 if index is not None else None

        self.database.execute(self.table.insert(), [{"indexid": x, "text": text} for x, text in rows])

    def delete(self, ids):
        self.database.execute(delete(self.table).where(self.table.c["indexid"].in_(ids)))

    def weights(self, tokens):
        return None

    def search(self, query, limit=3):
        query = (
            self.database.query(
                self.table.c["indexid"], text("ts_rank(vector, plainto_tsquery(:language, :query)) rank")
            )
            .order_by(desc(text("rank")))
            .limit(limit)
            .params({"language": self.language, "query": query})
        )

        return [(uid, score) for uid, score in query if score > 1e-5]

    def batchsearch(self, queries, limit=3, threads=True):
        return [self.search(query, limit) for query in queries]

    def count(self):
        # pylint: disable=E1102
        return self.database.query(func.count(self.table.c["indexid"])).scalar()

    def load(self, path):
        if self.database:
            self.database.rollback()
            self.connection.rollback()

        self.initialize()

    def save(self, path):
        if self.database:
            self.database.commit()
            self.connection.commit()

    def close(self):
        if self.database:
            self.database.close()
            self.engine.dispose()

    def issparse(self):
        return True

    def isnormalized(self):
        return True

    def initialize(self, recreate=False):
        """
        Initializes a new database session.

        Args:
            recreate: Recreates the database tables if True
        """

        if not self.database:
            self.engine = create_engine(
                self.config.get("url", os.environ.get("SCORING_URL")), poolclass=StaticPool, echo=False
            )
            self.connection = self.engine.connect()
            self.database = Session(self.connection)

            schema = self.config.get("schema")
            if schema:
                with self.engine.begin():
                    self.sqldialect(CreateSchema(schema, if_not_exists=True))

                self.sqldialect(text("SET search_path TO :schema"), {"schema": schema})

            table = self.config.get("table", "scoring")

            self.table = Table(
                table,
                MetaData(),
                Column("indexid", Integer, primary_key=True, autoincrement=False),
                Column("text", Text),
                (
                    Column("vector", TSVECTOR, Computed(f"to_tsvector('{self.language}', text)", persisted=True))
                    if self.engine.dialect.name == "postgresql"
                    else Column("vector", Integer)
                ),
            )

            index = Index(
                f"{table}-index",
                self.table.c["vector"],
                postgresql_using="gin",
            )

            if recreate:
                self.table.drop(self.connection, checkfirst=True)
                index.drop(self.connection, checkfirst=True)

            self.table.create(self.connection, checkfirst=True)
            index.create(self.connection, checkfirst=True)

    def sqldialect(self, sql, parameters=None):
        """
        Executes a SQL statement based on the current SQL dialect.

        Args:
            sql: SQL to execute
            parameters: optional bind parameters
        """

        args = (sql, parameters) if self.engine.dialect.name == "postgresql" else (text("SELECT 1"),)
        self.database.execute(*args)
