import os
import sqlite3

from .embedded import Embedded


class SQLite(Embedded):
    """
    Database instance backed by SQLite.
    """

    def connect(self, path=""):
        connection = sqlite3.connect(path, check_same_thread=False)

        if self.setting("wal"):
            connection.execute("PRAGMA journal_mode=WAL")

        return connection

    def getcursor(self):
        return self.connection.cursor()

    def rows(self):
        return self.cursor

    def addfunctions(self):
        if self.connection and self.functions:
            sqlite3.enable_callback_tracebacks(True)

            for name, argcount, fn in self.functions:
                self.connection.create_function(name, argcount, fn)

    def copy(self, path):
        if os.path.exists(path):
            os.remove(path)

        connection = self.connect(path)

        if self.connection.in_transaction:
            for sql in self.connection.iterdump():
                connection.execute(sql)
        else:
            self.connection.backup(connection)

        return connection
