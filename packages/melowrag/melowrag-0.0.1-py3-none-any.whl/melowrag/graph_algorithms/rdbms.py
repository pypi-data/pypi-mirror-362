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

try:
    from grand import Graph  # type:ignore
    from grand.backends import InMemoryCachedBackend, SQLBackend  # type:ignore
    from sqlalchemy import StaticPool, create_engine, text
    from sqlalchemy.schema import CreateSchema

    ORM = True
except ImportError:
    ORM = False

from .networkx import NetworkX


class RDBMS(NetworkX):
    """
    Graph instance backed by a relational database.
    """

    def __init__(self, config):
        if not ORM:
            raise ImportError('RDBMS is not available - install "graph" extra to enable')

        super().__init__(config)

        self.graph = None
        self.database = None

    def __del__(self):
        if hasattr(self, "database") and self.database:
            self.database.close()

    def create(self):
        self.graph, self.database = self.connect()

        for table in [self.config.get("nodes", "nodes"), self.config.get("edges", "edges")]:
            self.database.execute(text(f"DELETE FROM {table}"))

        return self.graph.nx

    def scan(self, attribute=None, data=False):
        if attribute:
            for node in self.backend:
                attributes = self.node(node)
                if attribute in attributes:
                    yield (node, attributes) if data else node
        else:
            yield from super().scan(attribute, data)

    def load(self, path):
        self.graph, self.database = self.connect()

        self.backend = self.graph.nx

    def save(self, path):
        self.database.commit()

    def close(self):
        super().close()

        self.database.close()

    def filter(self, nodes, graph=None):
        return super().filter(nodes, graph if graph else NetworkX(self.config))

    def connect(self):
        """
        Connects to a graph backed by a relational database.

        Args:
            Graph database instance
        """

        kwargs = {"poolclass": StaticPool, "echo": False}
        url = self.config.get("url", os.environ.get("GRAPH_URL"))

        schema = self.config.get("schema")
        if schema:
            engine = create_engine(url)
            with engine.begin() as connection:
                connection.execute(CreateSchema(schema, if_not_exists=True) if "postgresql" in url else text("SELECT 1"))

            kwargs["connect_args"] = {"options": f'-c search_path="{schema}"'} if "postgresql" in url else {}

        backend = SQLBackend(
            db_url=url,
            node_table_name=self.config.get("nodes", "nodes"),
            edge_table_name=self.config.get("edges", "edges"),
            sqlalchemy_kwargs=kwargs,
        )

        # pylint: disable=W0212
        return Graph(backend=InMemoryCachedBackend(backend, maxsize=None)), backend._connection
