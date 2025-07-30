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

from .errors import SerializeError
from .factory import SerializeFactory


class Serializer:
    """
    Methods to serialize and deserialize data.
    """

    @staticmethod
    def load(path):
        """
        Loads data from path. This method first tries to load the default serialization format.
        If that fails, it will fallback to pickle format for backwards-compatability purposes.

        Note that loading pickle files requires the env variable `ALLOW_PICKLE=True`.

        Args:
            path: data to load

        Returns:
            data
        """

        try:
            return SerializeFactory.create().load(path)
        except SerializeError:
            return SerializeFactory.create("pickle").load(path)

    @staticmethod
    def save(data, path):
        """
        Saves data to path.

        Args:
            data: data to save
            path: output path
        """

        SerializeFactory.create().save(data, path)
