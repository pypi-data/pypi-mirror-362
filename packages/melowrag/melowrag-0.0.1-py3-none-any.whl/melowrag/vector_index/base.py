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

import datetime
import platform


class VectoreIndex:
    """
    Base class for VectoreIndex instances. This class builds vector indexes to support similarity search.
    The built-in VectoreIndex backends store ids and vectors. Content storage is supported via database instances.
    """

    def __init__(self, config):
        """
        Creates a new VectoreIndex.

        Args:
            config: index configuration parameters
        """

        self.backend = None

        self.config = config

    def load(self, path):
        """
        Loads an VectoreIndex at path.

        Args:
            path: path to load ann index
        """

        raise NotImplementedError

    def index(self, embeddings):
        """
        Builds an VectoreIndex index.

        Args:
            embeddings: embeddings array
        """

        raise NotImplementedError

    def append(self, embeddings):
        """
        Append elements to an existing index.

        Args:
            embeddings: embeddings array
        """

        raise NotImplementedError

    def delete(self, ids):
        """
        Deletes elements from existing index.

        Args:
            ids: ids to delete
        """

        raise NotImplementedError

    def search(self, queries, limit):
        """
        Searches VectoreIndex index for query. Returns topn results.

        Args:
            queries: queries array
            limit: maximum results

        Returns:
            query results
        """

        raise NotImplementedError

    def count(self):
        """
        Number of elements in the VectoreIndex index.

        Returns:
            count
        """

        raise NotImplementedError

    def save(self, path):
        """
        Saves an VectoreIndex index at path.

        Args:
            path: path to save ann index
        """

        raise NotImplementedError

    def close(self):
        """
        Closes this VectoreIndex.
        """

        self.backend = None

    def setting(self, name, default=None):
        """
        Looks up backend specific setting.

        Args:
            name: setting name
            default: default value when setting not found

        Returns:
            setting value
        """

        backend = self.config.get(self.config["backend"])

        setting = backend.get(name) if backend else None
        return setting if setting else default

    def metadata(self, settings=None):
        """
        Adds index build metadata.

        Args:
            settings: index build settings
        """

        create = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        if settings:
            self.config["build"] = {
                "create": create,
                "python": platform.python_version(),
                "settings": settings,
                "system": f"{platform.system()} ({platform.machine()})",
            }

        self.config["update"] = create
