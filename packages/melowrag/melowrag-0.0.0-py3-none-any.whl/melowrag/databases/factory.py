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
