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
import torch

from .numpy import NumPy


class Torch(NumPy):
    """
    Builds an VectoreIndex index backed by a PyTorch array.
    """

    def __init__(self, config):
        super().__init__(config)

        self.all, self.cat, self.dot, self.zeros = torch.all, torch.cat, torch.mm, torch.zeros
        self.argsort, self.xor, self.clip = torch.argsort, torch.bitwise_xor, torch.clip

    def tensor(self, array):
        if isinstance(array, np.ndarray):
            array = torch.from_numpy(array)

        return array.cuda() if torch.cuda.is_available() else array

    def numpy(self, array):
        return array.cpu().numpy()

    def totype(self, array, dtype):
        return array.long() if dtype == np.int64 else array

    def settings(self):
        return {"torch": torch.__version__}
