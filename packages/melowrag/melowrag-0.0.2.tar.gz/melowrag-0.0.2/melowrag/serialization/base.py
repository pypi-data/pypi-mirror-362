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

class Serialize:
    """
    Base class for Serialize instances. This class serializes data to files, streams and bytes.
    """

    def load(self, path):
        """
        Loads data from path.

        Args:
            path: input path

        Returns:
            deserialized data
        """

        with open(path, "rb") as handle:
            return self.loadstream(handle)

    def save(self, data, path):
        """
        Saves data to path.

        Args:
            data: data to save
            path: output path
        """

        with open(path, "wb") as handle:
            self.savestream(data, handle)

    def loadstream(self, stream):
        """
        Loads data from stream.

        Args:
            stream: input stream

        Returns:
            deserialized data
        """

        raise NotImplementedError

    def savestream(self, data, stream):
        """
        Saves data to stream.

        Args:
            data: data to save
            stream: output stream
        """

        raise NotImplementedError

    def loadbytes(self, data):
        """
        Loads data from bytes.

        Args:
            data: input bytes

        Returns:
            deserialized data
        """

        raise NotImplementedError

    def savebytes(self, data):
        """
        Saves data as bytes.

        Args:
            data: data to save

        Returns:
            serialized data
        """

        raise NotImplementedError
