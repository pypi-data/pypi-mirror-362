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
