from .rdbms import RDBMS


class Embedded(RDBMS):
    """
    Base class for embedded relational databases. An embedded relational database stores all content in a local file.
    """

    def __init__(self, config):
        """
        Creates a new Database.

        Args:
            config: database configuration parameters
        """

        super().__init__(config)

        self.path = None

    def load(self, path):
        super().load(path)

        self.path = path

    def save(self, path):
        if not self.path:
            self.connection.commit()

            connection = self.copy(path)

            self.connection.close()

            self.session(connection=connection)
            self.path = path

        elif self.path == path:
            self.connection.commit()

        else:
            self.copy(path).close()

    def jsonprefix(self):
        return "json_extract(data"

    def jsoncolumn(self, name):
        return f"json_extract(data, '$.{name}')"

    def copy(self, path):
        """
        Copies the current database into path.

        Args:
            path: path to write database

        Returns:
            new connection with data copied over
        """

        raise NotImplementedError
