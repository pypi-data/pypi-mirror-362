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

import types

import numpy as np

from ...utilities import Resolver
from ..base import Vectors


class External(Vectors):
    """
    Builds vectors using an external method. This can be a local function or an external API call.
    """

    def __init__(self, config, scoring, models):
        super().__init__(config, scoring, models)

        self.transform = self.resolve(config.get("transform"))

    def loadmodel(self, path):
        return None

    def encode(self, data, category=None):
        if self.transform and data and not isinstance(data[0], np.ndarray):
            data = self.transform(data)

        return data.astype(np.float32) if isinstance(data, np.ndarray) else np.array(data, dtype=np.float32)

    def resolve(self, transform):
        """
        Resolves a transform function.

        Args:
            transform: transform function

        Returns:
            resolved transform function
        """

        if transform:
            transform = Resolver()(transform) if transform and isinstance(transform, str) else transform

            transform = transform if isinstance(transform, types.FunctionType) else transform()

        return transform
