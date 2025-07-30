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

from itertools import chain

from .base import Data


class Texts(Data):
    """
    Tokenizes text datasets as input for training language models.
    """

    def __init__(self, tokenizer, columns, maxlength):
        """
        Creates a new instance for tokenizing Texts training data.

        Args:
            tokenizer: model tokenizer
            columns: tuple of columns to use for text
            maxlength: maximum sequence length
        """

        super().__init__(tokenizer, columns, maxlength)

        if not self.columns:
            self.columns = ("text", None)

    def process(self, data):
        text1, text2 = self.columns

        text = (data[text1], data[text2]) if text2 else (data[text1],)

        inputs = self.tokenizer(*text, return_special_tokens_mask=True)

        return self.concat(inputs)

    def concat(self, inputs):
        """
        Concatenates tokenized text into chunks of maxlength.

        Args:
            inputs: tokenized input

        Returns:
            Chunks of tokenized text each with a size of maxlength
        """

        concat = {k: list(chain(*inputs[k])) for k in inputs.keys()}

        length = len(concat[next(iter(inputs.keys()))])

        if length >= self.maxlength:
            length = (length // self.maxlength) * self.maxlength

        result = {k: [v[x : x + self.maxlength] for x in range(0, length, self.maxlength)] for k, v in concat.items()}

        return result
