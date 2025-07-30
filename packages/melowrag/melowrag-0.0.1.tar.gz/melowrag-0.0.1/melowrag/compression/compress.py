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


class Compress:
    """
    Base class for Compress instances.
    """

    def pack(self, path, output):
        """
        Compresses files in directory path to file output.

        Args:
            path: input directory path
            output: output file
        """

        raise NotImplementedError

    def unpack(self, path, output):
        """
        Extracts all files in path to output.

        Args:
            path: input file path
            output: output directory
        """

        raise NotImplementedError

    def validate(self, directory, path):
        """
        Validates path is under directory.

        Args:
            directory: base directory
            path: path to validate

        Returns:
            True if path is under directory, False otherwise
        """

        directory = os.path.abspath(directory)
        path = os.path.abspath(path)
        prefix = os.path.commonprefix([directory, path])

        return prefix == directory
