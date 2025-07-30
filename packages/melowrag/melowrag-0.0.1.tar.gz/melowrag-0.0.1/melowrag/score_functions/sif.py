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


class SIF(TFIDF):
    """
    Smooth Inverse Frequency (SIF) scoring.
    """

    def __init__(self, config=None):
        super().__init__(config)

        self.a = self.config.get("a", 1e-3)

    def computefreq(self, tokens):
        return {token: self.wordfreq[token] for token in tokens}

    def score(self, freq, idf, length):
        if isinstance(freq, np.ndarray) and freq.shape != np.array(idf).shape:
            freq.fill(freq.sum())

        return self.a / (self.a + freq / self.tokens)
