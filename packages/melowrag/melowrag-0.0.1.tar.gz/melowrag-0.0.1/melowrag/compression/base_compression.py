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
from tempfile import TemporaryDirectory

from .tar_compression import Tar
from .zip_compression import Zip


class Archive:
    """
    Base class for archive instances.
    """

    def __init__(self, directory=None):
        """
        Creates a new archive instance.

        Args:
            directory: directory to use as working directory, defaults to a temporary directory
        """

        self.directory = directory

    def isarchive(self, path):
        """
        Checks if path is an archive file based on the extension.

        Args:
            path: path to check

        Returns:
            True if the path ends with an archive extension, False otherwise
        """

        return path and any(path.lower().endswith(extension) for extension in [".tar.bz2", ".tar.gz", ".tar.xz", ".zip"])

    def path(self):
        """
        Gets the current working directory for this archive instance.

        Returns:
            archive working directory
        """

        if not self.directory:
            # pylint: disable=R1732
            self.directory = TemporaryDirectory()

        return self.directory.name if isinstance(self.directory, TemporaryDirectory) else self.directory

    def load(self, path, compression=None):
        """
        Extracts file at path to archive working directory.

        Args:
            path: path to archive file
            compression: compression format, infers from path if not provided
        """

        compress = self.create(path, compression)
        compress.unpack(path, self.path())

    def save(self, path, compression=None):
        """
        Archives files in archive working directory to file at path.

        Args:
            path: path to archive file
            compression: compression format, infers from path if not provided
        """

        output = os.path.dirname(path)
        if output:
            os.makedirs(output, exist_ok=True)

        compress = self.create(path, compression)
        compress.pack(self.path(), path)

    def create(self, path, compression):
        """
        Method to construct a Compress instance.

        Args:
            path: file path
            compression: compression format, infers using file extension if not provided

        Returns:
            Compress
        """

        compression = compression if compression else path.lower().split(".")[-1]

        return Zip() if compression == "zip" else Tar()

    def __repr__(self):
        """
        Returns a detailed string representation of the Archive instance.
        """
        class_name = self.__class__.__name__
        dir_info = self.directory if self.directory else "<TemporaryDirectory>"
        archive_types = ["tar", "zip"]
        return f"{class_name}(directory={dir_info!r}, types={archive_types})"

    def __str__(self):
        """
        Returns a user-friendly string representation of the Archive instance.
        """
        class_name = self.__class__.__name__
        dir_info = self.directory if self.directory else "temporary directory"
        return f"{class_name}(directory={dir_info}) [supports: tar, zip]"
