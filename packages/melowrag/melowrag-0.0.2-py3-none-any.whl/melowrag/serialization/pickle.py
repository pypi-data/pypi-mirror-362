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

import logging
import os
import pickle
import warnings

from .base import Serialize

logger = logging.getLogger(__name__)


class Pickle(Serialize):
    """
    Pickle serialization.
    """

    def __init__(self, allowpickle=False):
        """
        Creates a new instance for Pickle serialization.

        This class ensures the allowpickle parameter or the `ALLOW_PICKLE` environment variable is True. All methods will
        raise errors if this isn't the case.

        Pickle serialization is OK for local data but it isn't recommended when sharing data externally.

        Args:
            allowpickle: default pickle allow mode, only True with methods that generate local temporary data
        """

        super().__init__()

        self.allowpickle = allowpickle

        self.version = 4

    def load(self, path):
        return super().load(path) if self.allow(path) else None

    def save(self, data, path):
        if self.allow():
            super().save(data, path)

    def loadstream(self, stream):
        return pickle.load(stream) if self.allow() else None

    def savestream(self, data, stream):
        if self.allow():
            pickle.dump(data, stream, protocol=self.version)

    def loadbytes(self, data):
        return pickle.loads(data) if self.allow() else None

    def savebytes(self, data):
        return pickle.dumps(data, protocol=self.version) if self.allow() else None

    def allow(self, path=None):
        """
        Checks if loading and saving pickled data is allowed. Raises an error if it's not allowed.

        Args:
            path: optional path to add to generated error messages
        """

        enablepickle = self.allowpickle or os.environ.get("ALLOW_PICKLE", "True") in ("True", "1")
        if not enablepickle:
            raise ValueError(
                "Loading of pickled index data is disabled. "
                f"`{path if path else 'stream'}` was not loaded. "
                "Set the env variable `ALLOW_PICKLE=True` to enable loading pickled index data. "
                "This should only be done for trusted and/or local data.",
                stacklevel=1,
            )

        if not self.allowpickle:
            warnings.warn(
                (
                    "Pickled index data formats are deprecated and loading will be disabled by default in the future. "
                    "Set the env variable `ALLOW_PICKLE=False` to disable the loading of pickled index data formats. "
                    "Saving this index will replace pickled index data formats with the latest index "
                    "formats and remove this warning.",
                ),
                FutureWarning,
                stacklevel=1,
            )

        return enablepickle
