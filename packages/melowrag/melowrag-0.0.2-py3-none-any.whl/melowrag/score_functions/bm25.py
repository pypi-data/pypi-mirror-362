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

import numpy as np

from .tfidf import TFIDF


class BM25(TFIDF):
    """
    Best matching (BM25) scoring.
    """

    def __init__(self, config=None):
        super().__init__(config)

        self.k1 = self.config.get("k1", 1.2)
        self.b = self.config.get("b", 0.75)

    def computeidf(self, freq):
        return np.log(1 + (self.total - freq + 0.5) / (freq + 0.5))

    def score(self, freq, idf, length):
        k = self.k1 * ((1 - self.b) + self.b * length / self.avgdl)
        return idf * (freq * (self.k1 + 1)) / (freq + k)
