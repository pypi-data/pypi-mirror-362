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
