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

from urllib.parse import urlparse

from ..utilities import Resolver
from .client import Client
from .duckdb import DuckDB
from .sqlite import SQLite


class DatabaseFactory:
    """
    Methods to create document databases.
    """

    @staticmethod
    def create(config):
        """
        Create a Database.

        Args:
            config: database configuration parameters

        Returns:
            Database
        """

        database = None

        content = config.get("content")

        if content is True:
            content = "sqlite"

        if content == "duckdb":
            database = DuckDB(config)
        elif content == "sqlite":
            database = SQLite(config)
        elif content:
            url = urlparse(content)
            if content == "client" or url.scheme:
                database = Client(config)
            else:
                database = DatabaseFactory.resolve(content, config)

        config["content"] = content

        return database

    @staticmethod
    def resolve(backend, config):
        """
        Attempt to resolve a custom backend.

        Args:
            backend: backend class
            config: index configuration parameters

        Returns:
            Database
        """

        try:
            return Resolver()(backend)(config)
        except Exception as e:
            raise ImportError(f"Unable to resolve database backend: '{backend}'") from e
