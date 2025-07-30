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

import contextlib
import os
import tempfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .filetohtml import FileToHTML
from .htmltomd import HTMLToMarkdown
from .segmentation import Segmentation


class Textractor(Segmentation):
    """
    Extracts text from files.
    """

    # pylint: disable=R0913
    def __init__(
        self,
        sentences=False,
        lines=False,
        paragraphs=False,
        minlength=None,
        join=False,
        sections=False,
        cleantext=True,
        chunker=None,
        headers=None,
        backend="available",
        **kwargs,
    ):
        super().__init__(sentences, lines, paragraphs, minlength, join, sections, cleantext, chunker, **kwargs)

        backend = "tika" if kwargs.get("tika") else None if "tika" in kwargs else backend

        self.html = FileToHTML(backend) if backend else None

        self.markdown = HTMLToMarkdown(self.paragraphs, self.sections)

        self.headers = headers if headers else {}

    def text(self, text):
        path, exists = self.valid(text)

        if not path:
            html = text

        elif self.html:
            path = path if exists else self.download(path)

            html = self.html(path)

            html = html if html else self.retrieve(path)

            if not exists:
                os.remove(path)

        else:
            html = self.retrieve(path)

        return self.markdown(html)

    def valid(self, path):
        """
        Checks if path is a valid local file or web url. Returns path if valid along with a flag
        denoting if the path exists locally.

        Args:
            path: path to check

        Returns:
            (path, exists)
        """

        path = path.replace("file://", "")

        exists = os.path.exists(path)

        return (path if exists or urlparse(path).scheme in ("http", "https") else None, exists)

    def download(self, url):
        """
        Downloads content of url to a temporary file.

        Args:
            url: input url

        Returns:
            temporary file path
        """

        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as output:
            path = output.name

            output.write(self.retrieve(url))

        return path

    def retrieve(self, url):
        """
        Retrieves content from url.

        Args:
            url: input url

        Returns:
            data
        """

        if os.path.exists(url):
            with open(url, "rb") as f:
                return f.read()

        with contextlib.closing(urlopen(Request(url, headers=self.headers))) as connection:
            return connection.read()
