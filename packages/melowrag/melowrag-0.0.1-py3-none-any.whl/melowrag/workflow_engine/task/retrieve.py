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
import tempfile
from urllib.parse import urlparse
from urllib.request import urlretrieve

from .url import UrlTask


class RetrieveTask(UrlTask):
    """
    Task that retrieves urls (local or remote) to a local directory.
    """

    def register(self, directory=None, flatten=True):
        """
        Adds retrieve parameters to task.

        Args:
            directory: local directory used to store retrieved files
            flatten: flatten input directory structure, defaults to True
        """

        # pylint: disable=W0201
        if not directory:
            # pylint: disable=R1732
            self.tempdir = tempfile.TemporaryDirectory()
            directory = self.tempdir.name

        os.makedirs(directory, exist_ok=True)

        self.directory = directory
        self.flatten = flatten

    def prepare(self, element):
        path = urlparse(element).path

        if self.flatten:
            path = os.path.join(self.directory, os.path.basename(path))
        else:
            path = os.path.join(self.directory, os.path.normpath(path.lstrip("/")))
            directory = os.path.dirname(path)

            os.makedirs(directory, exist_ok=True)

        urlretrieve(element, path)

        return path
