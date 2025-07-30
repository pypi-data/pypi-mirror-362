import datetime
import json

from .base import Database
from .db_schema import Statement


# pylint: disable=R0904
class RDBMS(Database):
    """
    Base relational database class. A relational database uses SQL to insert, update, delete and select from a
    database instance.
    """

    def __init__(self, config):
        """
        Creates a new Database.

        Args:
            config: database configuration parameters
        """

        super().__init__(config)

        self.connection = None
        self.cursor = None

    def load(self, path):
        self.session(path)

    def insert(self, documents, index=0):
        self.initialize()

        entry = datetime.datetime.now(datetime.timezone.utc)

        for uid, document, tags in documents:
            if isinstance(document, dict):
                document = self.loaddocument(uid, document, tags, entry)

            if document is not None:
                if isinstance(document, list):
                    document = " ".join(document)
                elif not isinstance(document, str):
                    self.loadobject(uid, document, tags, entry)

                    document = None

                self.loadsection(index, uid, document, tags, entry)
                index += 1

        self.finalize()

    def delete(self, ids):
        if self.connection:
            self.batch(ids=ids)

            self.cursor.execute(Statement.DELETE_DOCUMENTS)
            self.cursor.execute(Statement.DELETE_OBJECTS)
            self.cursor.execute(Statement.DELETE_SECTIONS)

    def reindex(self, config):
        if self.connection:
            self.configure(config)

            select = self.resolve(self.text)

            name = self.reindexstart()

            self.cursor.execute(Statement.COPY_SECTIONS % (name, select))

            self.cursor.execute(Statement.STREAM_SECTIONS % name)
            for uid, text, data, obj, tags in self.rows():
                if not text and self.encoder and obj:
                    yield (uid, self.encoder.decode(obj), tags)
                else:
                    data = json.loads(data) if data and isinstance(data, str) else data

                    yield (uid, data if data else text, tags)

            self.cursor.execute(Statement.DROP_SECTIONS)
            self.cursor.execute(Statement.RENAME_SECTIONS % name)

            self.reindexend(name)

    def save(self, path):
        if self.connection:
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()

    def ids(self, ids):
        self.batch(ids=ids)
        self.cursor.execute(Statement.SELECT_IDS)

        return self.cursor.fetchall()

    def count(self):
        self.cursor.execute(Statement.COUNT_IDS)
        return self.cursor.fetchone()[0]

    def resolve(self, name, alias=None):
        sections = ["indexid", "id", "tags", "entry"]
        noprefix = ["data", "object", "score", "text"]

        if alias:
            if name == alias or alias in sections:
                return name

            return f'{name} as "{alias}"'

        if self.expressions and name in self.expressions:
            return self.expressions[name]

        if name.startswith(self.jsonprefix()) or any(f"s.{s}" == name for s in sections):
            return name

        if name.lower() in sections:
            return f"s.{name}"

        if name.lower() in noprefix:
            return name

        return self.jsoncolumn(name)

    def embed(self, similarity, batch):
        self.batch(indexids=[i for i, _ in similarity[batch]], batch=batch)

        if not batch:
            self.scores(similarity)

        return Statement.IDS_CLAUSE % batch

    # pylint: disable=R0912
    def query(self, query, limit, parameters, indexids):
        select = query.get("select", self.defaults())
        where = query.get("where")
        groupby, having = query.get("groupby"), query.get("having")
        orderby, qlimit, offset = query.get("orderby"), query.get("limit"), query.get("offset")
        similarity = query.get("similar")

        if indexids:
            select = f"{self.resolve('indexid')}, {self.resolve('score')}"

        query = Statement.TABLE_CLAUSE % select
        if where is not None:
            query += f" WHERE {where}"
        if groupby is not None:
            query += f" GROUP BY {groupby}"
        if having is not None:
            query += f" HAVING {having}"
        if orderby is not None:
            query += f" ORDER BY {orderby}"

        if similarity and orderby is None:
            query += " ORDER BY score DESC"

        if qlimit is not None or limit:
            query += f" LIMIT {qlimit if qlimit else limit}"

            if offset is not None:
                query += f" OFFSET {offset}"

        if not similarity:
            self.scores(None)

        args = (query, parameters) if parameters else (query,)
        self.execute(self.cursor.execute, *args)

        columns = [c[0] for c in self.cursor.description]

        results = []
        for row in self.rows():
            result = {}

            for x, column in enumerate(columns):
                if column not in result or result[column] is None:
                    if self.encoder and column == self.object:
                        result[column] = self.encoder.decode(row[x])
                    else:
                        result[column] = row[x]

            results.append(result)

        return [(x["indexid"], x["score"]) for x in results] if indexids else results

    def initialize(self):
        """
        Creates connection and initial database schema if no connection exists.
        """

        if not self.connection:
            self.session()

            self.createtables()

    def session(self, path=None, connection=None):
        """
        Starts a new database session.

        Args:
            path: path to database file
            connection: existing connection to use
        """

        self.connection = connection if connection else self.connect(path) if path else self.connect()
        self.cursor = self.getcursor()

        self.addfunctions()

        self.createbatch()
        self.createscores()

    def createtables(self):
        """
        Creates the initial table schema.
        """

        self.cursor.execute(Statement.CREATE_DOCUMENTS)
        self.cursor.execute(Statement.CREATE_OBJECTS)
        self.cursor.execute(Statement.CREATE_SECTIONS % "sections")
        self.cursor.execute(Statement.CREATE_SECTIONS_INDEX)

    def finalize(self):
        """
        Post processing logic run after inserting a batch of documents. Default method is no-op.
        """

    def loaddocument(self, uid, document, tags, entry):
        """
        Applies pre-processing logic and inserts a document.

        Args:
            uid: unique id
            document: input document dictionary
            tags: document tags
            entry: generated entry date

        Returns:
            section value
        """

        document = document.copy()

        obj = document.pop(self.object) if self.object in document else None

        if document:
            self.insertdocument(uid, json.dumps(document, allow_nan=False), tags, entry)

        if self.text in document and obj:
            self.loadobject(uid, obj, tags, entry)

        return document[self.text] if self.text in document else obj

    def insertdocument(self, uid, data, tags, entry):
        """
        Inserts a document.

        Args:
            uid: unique id
            data: document data
            tags: document tags
            entry: generated entry date
        """

        self.cursor.execute(Statement.INSERT_DOCUMENT, [uid, data, tags, entry])

    def loadobject(self, uid, obj, tags, entry):
        """
        Applies pre-preprocessing logic and inserts an object.

        Args:
            uid: unique id
            obj: input object
            tags: object tags
            entry: generated entry date
        """

        if self.encoder:
            self.insertobject(uid, self.encoder.encode(obj), tags, entry)

    def insertobject(self, uid, data, tags, entry):
        """
        Inserts an object.

        Args:
            uid: unique id
            data: encoded data
            tags: object tags
            entry: generated entry date
        """

        self.cursor.execute(Statement.INSERT_OBJECT, [uid, data, tags, entry])

    def loadsection(self, index, uid, text, tags, entry):
        """
        Applies pre-processing logic and inserts a section.

        Args:
            index: index id
            uid: unique id
            text: section text
            tags: section tags
            entry: generated entry date
        """

        self.insertsection(index, uid, text, tags, entry)

    def insertsection(self, index, uid, text, tags, entry):
        """
        Inserts a section.

        Args:
            index: index id
            uid: unique id
            text: section text
            tags: section tags
            entry: generated entry date
        """

        self.cursor.execute(Statement.INSERT_SECTION, [index, uid, text, tags, entry])

    def reindexstart(self):
        """
        Starts a reindex operation.

        Returns:
            temporary working table name
        """

        name = "rebuild"

        self.cursor.execute(Statement.CREATE_SECTIONS % name)

        return name

    # pylint: disable=W0613
    def reindexend(self, name):
        """
        Ends a reindex operation.

        Args:
            name: working table name
        """

        self.cursor.execute(Statement.CREATE_SECTIONS_INDEX)

    def batch(self, indexids=None, ids=None, batch=None):
        """
        Loads ids to a temporary batch table for efficient query processing.

        Args:
            indexids: list of indexids
            ids: list of ids
            batch: batch index, used when statement has multiple subselects
        """

        if not batch:
            self.cursor.execute(Statement.DELETE_BATCH)

        self.insertbatch(indexids, ids, batch)

    def createbatch(self):
        """
        Creates temporary batch table.
        """

        self.cursor.execute(Statement.CREATE_BATCH)

    def insertbatch(self, indexids, ids, batch):
        """
        Inserts batch of ids.
        """

        if indexids:
            self.cursor.executemany(Statement.INSERT_BATCH_INDEXID, [(i, batch) for i in indexids])
        if ids:
            self.cursor.executemany(Statement.INSERT_BATCH_ID, [(str(uid), batch) for uid in ids])

    def scores(self, similarity):
        """
        Loads a batch of similarity scores to a temporary table for efficient query processing.

        Args:
            similarity: similarity results as [(indexid, score)]
        """

        self.cursor.execute(Statement.DELETE_SCORES)

        if similarity:
            scores = {}
            for s in similarity:
                for i, score in s:
                    if i not in scores:
                        scores[i] = []
                    scores[i].append(score)

            self.insertscores(scores)

    def createscores(self):
        """
        Creates temporary scores table.
        """

        self.cursor.execute(Statement.CREATE_SCORES)

    def insertscores(self, scores):
        """
        Inserts a batch of scores.

        Args:
            scores: scores to add
        """

        if scores:
            self.cursor.executemany(Statement.INSERT_SCORE, [(i, sum(s) / len(s)) for i, s in scores.items()])

    def defaults(self):
        """
        Returns a list of default columns when there is no select clause.

        Returns:
            list of default columns
        """

        return "s.id, text, score"

    def connect(self, path=None):
        """
        Creates a new database connection.

        Args:
            path: path to database file

        Returns:
            connection
        """

        raise NotImplementedError

    def getcursor(self):
        """
        Opens a cursor for current connection.

        Returns:
            cursor
        """

        raise NotImplementedError

    def jsonprefix(self):
        """
        Returns json column prefix to test for.

        Returns:
            dynamic column prefix
        """

        raise NotImplementedError

    def jsoncolumn(self, name):
        """
        Builds a json extract column expression for name.

        Args:
            name: column name

        Returns:
            dynamic column expression
        """

        raise NotImplementedError

    def rows(self):
        """
        Returns current cursor row iterator for last executed query.

        Args:
            cursor: cursor

        Returns:
            iterable collection of rows
        """

        raise NotImplementedError

    def addfunctions(self):
        """
        Adds custom functions in current connection.
        """

        raise NotImplementedError
