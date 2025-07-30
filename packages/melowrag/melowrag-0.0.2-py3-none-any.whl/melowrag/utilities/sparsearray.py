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

try:
    from scipy.sparse import csr_matrix

    SCIPY = True
except ImportError:
    SCIPY = False


class SparseArray:
    """
    Methods to load and save sparse arrays to file.
    """

    def __init__(self):
        """
        Creates a SparseArray instance.
        """

        if not SCIPY:
            raise ImportError("SciPy is not available - install scipy to enable")

    def load(self, f):
        """
        Loads a sparse array from file.

        Args:
            f: input file handle

        Returns:
            sparse array
        """

        data, indices, indptr, shape = (
            np.load(f, allow_pickle=False),
            np.load(f, allow_pickle=False),
            np.load(f, allow_pickle=False),
            np.load(f, allow_pickle=False),
        )

        return csr_matrix((data, indices, indptr), shape=shape)

    def save(self, f, array):
        """
        Saves a sparse array to file.

        Args:
            f: output file handle
            array: sparse array
        """

        for x in [array.data, array.indices, array.indptr, array.shape]:
            np.save(f, x, allow_pickle=False)
