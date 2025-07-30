import functools
import os
import sqlite3
import sys
from array import array
from collections import Counter
from threading import RLock

import numpy as np


class Terms:
    """
    Builds, searches and stores memory efficient term frequency sparse arrays for a scoring instance.
    """

    CREATE_TERMS = """
        CREATE TABLE IF NOT EXISTS terms (
            term TEXT PRIMARY KEY,
            ids BLOB,
            freqs BLOB
        )
    """

    INSERT_TERM = "INSERT OR REPLACE INTO terms VALUES (?, ?, ?)"
    SELECT_TERMS = "SELECT ids, freqs FROM terms WHERE term = ?"

    CREATE_DOCUMENTS = """
        CREATE TABLE IF NOT EXISTS documents (
            indexid INTEGER PRIMARY KEY,
            id TEXT,
            deleted INTEGER,
            length INTEGER
        )
    """

    DELETE_DOCUMENTS = "DELETE FROM documents"
    INSERT_DOCUMENT = "INSERT OR REPLACE INTO documents VALUES (?, ?, ?, ?)"
    SELECT_DOCUMENTS = "SELECT indexid, id, deleted, length FROM documents ORDER BY indexid"

    def __init__(self, config, score, idf):
        """
        Creates a new terms index.

        Args:
            config: configuration
            score: score function
            idf: idf weights
        """

        self.config = config if isinstance(config, dict) else {}
        self.cachelimit = self.config.get("cachelimit", 250000000)
        self.cutoff = self.config.get("cutoff", 0.1)

        self.score, self.idf = score, idf

        self.ids, self.deletes, self.lengths = [], [], array("q")

        self.terms, self.cachesize = {}, 0

        self.connection, self.cursor, self.path = None, None, None

        self.lock = RLock()

    def insert(self, uid, terms):
        """
        Insert term into index.

        Args:
            uid: document id
            terms: document terms
        """

        self.initialize()

        indexid = len(self.ids)

        freqs, length = Counter(terms), len(terms)

        for term, count in freqs.items():
            self.add(indexid, term, count)

            self.cachesize += 16

        if self.cachesize >= self.cachelimit:
            self.index()

        self.ids.append(uid)
        self.lengths.append(length)

    def delete(self, ids):
        """
        Mark ids as deleted. This prevents deleted results from showing up in search results.
        The data is not removed from the underlying term frequency sparse arrays.

        Args:
            ids: ids to delete
        """

        self.deletes.extend([self.ids.index(i) for i in ids])

    def index(self):
        """
        Saves any remaining cached terms to the database.
        """

        for term, (nuids, nfreqs) in self.terms.items():
            uids, freqs = self.lookup(term)

            if uids:
                uids.extend(nuids)
                freqs.extend(nfreqs)
            else:
                uids, freqs = nuids, nfreqs

            if sys.byteorder == "big":
                uids.byteswap()
                freqs.byteswap()

            self.cursor.execute(Terms.INSERT_TERM, [term, uids.tobytes(), freqs.tobytes()])

        self.weights.cache_clear()

        self.terms, self.cachesize = {}, 0

    def search(self, terms, limit):
        """
        Searches term index a term-at-a-time. Each term frequency sparse array is retrieved
        and used to calculate term match scores.

        This method calculates term scores in two steps as shown below.

          1. Query and score less common term scores first
          2. Merge in common term scores for all documents matching the first query

        This is similar to the common terms query in Apache Lucene.

        Args:
            terms: query terms
            limit: maximum results

        Returns:
            list of (id, score)
        """

        scores = np.zeros(len(self.ids), dtype=np.float32)

        terms, skipped, hasscores = Counter(terms), {}, False
        for term, freq in terms.items():
            uids, weights = self.weights(term)
            if uids is not None:
                if len(uids) <= self.cutoff * len(self.ids):
                    scores[uids] += freq * weights

                    hasscores = True
                else:
                    skipped[term] = freq

        return self.topn(scores, limit, hasscores, skipped)

    def count(self):
        """
        Number of elements in the scoring index.

        Returns:
            count
        """

        return len(self.ids) - len(self.deletes)

    def load(self, path):
        """
        Loads terms database from path. This method loads document attributes into memory.

        Args:
            path: path to read terms database
        """

        self.connection = self.connect(path)
        self.cursor = self.connection.cursor()
        self.path = path

        self.ids, self.deletes, self.lengths = [], [], array("q")

        self.cursor.execute(Terms.SELECT_DOCUMENTS)
        for indexid, uid, deleted, length in self.cursor:
            self.ids.append(uid)

            if deleted:
                self.deletes.append(indexid)

            self.lengths.append(length)

        if all(uid.isdigit() for uid in self.ids):
            self.ids = [int(uid) for uid in self.ids]

        self.weights.cache_clear()

    def save(self, path):
        """
        Saves terms database to path. This method creates or replaces document attributes into the database.

        Args:
            path: path to write terms database
        """

        self.cursor.execute(Terms.DELETE_DOCUMENTS)

        for i, uid in enumerate(self.ids):
            self.cursor.execute(Terms.INSERT_DOCUMENT, [i, uid, 1 if i in self.deletes else 0, self.lengths[i]])

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
        """
        Close and free resources used by this instance.
        """

        if self.connection:
            self.connection.close()

    def initialize(self):
        """
        Creates connection and initial database schema if no connection exists.
        """

        if not self.connection:
            self.connection = self.connect()
            self.cursor = self.connection.cursor()

            self.cursor.execute(Terms.CREATE_TERMS)
            self.cursor.execute(Terms.CREATE_DOCUMENTS)

    def connect(self, path=""):
        """
        Creates a new term database connection.

        Args:
            path: path to term database file

        Returns:
            connection
        """

        connection = sqlite3.connect(path, check_same_thread=False)

        if self.config.get("wal"):
            connection.execute("PRAGMA journal_mode=WAL")

        return connection

    def copy(self, path):
        """
        Copies content from current terms database into target.

        Args:
            path: target database path

        Returns:
            new database connection
        """

        if os.path.exists(path):
            os.remove(path)

        connection = self.connect(path)

        if self.connection.in_transaction:
            for sql in self.connection.iterdump():
                connection.execute(sql)
        else:
            self.connection.backup(connection)

        return connection

    def add(self, indexid, term, freq):
        """
        Adds a term frequency entry.

        Args:
            indexid: internal index id
            term: term
            freq: term frequency
        """

        if term not in self.terms:
            self.terms[term] = (array("q"), array("q"))

        ids, freqs = self.terms[term]
        ids.append(indexid)
        freqs.append(freq)

    def lookup(self, term):
        """
        Retrieves a term frequency sparse array.

        Args:
            term: term to lookup

        Returns:
            term frequency sparse array
        """

        uids, freqs = None, None

        result = self.cursor.execute(Terms.SELECT_TERMS, [term]).fetchone()
        if result:
            uids, freqs = (array("q"), array("q"))
            uids.frombytes(result[0])
            freqs.frombytes(result[1])

            if sys.byteorder == "big":
                uids.byteswap()
                freqs.byteswap()

        return uids, freqs

    @functools.lru_cache(maxsize=500)  # noqa: B019
    def weights(self, term):
        """
        Computes a term weights sparse array for term. This method is wrapped with a least recently used cache,
        which will return common term weights from the cache.

        Args:
            term: term

        Returns:
            term weights sparse array
        """

        lengths = np.frombuffer(self.lengths, dtype=np.int64)

        with self.lock:
            uids, freqs = self.lookup(term)
            weights = None

        if uids:
            uids = np.frombuffer(uids, dtype=np.int64)
            weights = self.score(np.frombuffer(freqs, dtype=np.int64), self.idf[term], lengths[uids]).astype(np.float32)

        return uids, weights

    def topn(self, scores, limit, hasscores, skipped):
        """
        Get topn scores from an partial scores array.

        Args:
            scores: partial scores array with scores for less common terms
            limit: maximum results
            hasscores: True if partial scores array has any nonzero scores, False otherwise
            skipped: terms skipped in initial query

        Returns:
            topn scores
        """

        topn = min(len(scores), limit * 5)

        matches = self.candidates(scores, topn)

        self.merge(scores, matches, hasscores, skipped)

        if not hasscores:
            matches = self.candidates(scores, topn)

        matches = matches[np.argsort(-scores[matches])]

        return [(self.ids[x], float(scores[x])) for x in matches[:limit] if scores[x] > 0]

    def merge(self, scores, matches, hasscores, terms):
        """
        Merges common term scores into scores array.

        Args:
            scores: partial scores array
            matches: current matches, if any
            hasscores: True if scores has current matches, False otherwise
            terms: common terms
        """

        for term, freq in terms.items():
            uids, weights = self.weights(term)

            if hasscores:
                indices = np.searchsorted(uids, matches)

                indices = [x for i, x in enumerate(indices) if x < len(uids) and uids[x] == matches[i]]

                uids, weights = uids[indices], weights[indices]

            scores[uids] += freq * weights

    def candidates(self, scores, topn):
        """
        Gets the topn scored candidates. This method ignores deleted documents.

        Args:
            scores: scores array
            topn: topn elements

        Returns:
            topn scored candidates
        """

        scores[self.deletes] = 0

        return np.argpartition(scores, -topn)[-topn:]
