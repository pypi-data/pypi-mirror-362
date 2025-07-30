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

from .base_compression import Archive


class ArchiveFactory:
    """
    Methods to create Archive instances.
    """

    @staticmethod
    def create(directory=None):
        """
        Create a new Archive instance.

        Args:
            directory: optional default working directory, otherwise uses a temporary directory

        Returns:
            Archive
        """

        return Archive(directory)

    def __repr__(self):
        """
        Returns a detailed string representation of the ArchiveFactory class.
        """
        return f"{self.__class__.__name__}(factory for Archive instances)"

    def __str__(self):
        """
        Returns a user-friendly string representation of the ArchiveFactory class.
        """
        return "ArchiveFactory: use .create(directory) to get an Archive instance"
