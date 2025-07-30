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

from .base import Data


class Sequences(Data):
    """
    Tokenizes sequence-sequence datasets as input for training sequence-sequence models
    """

    def __init__(self, tokenizer, columns, maxlength, prefix):
        """
        Creates a new instance for tokenizing Sequences training data.

        Args:
            tokenizer: model tokenizer
            columns: tuple of columns to use for text/label
            maxlength: maximum sequence length
            prefix: source prefix
        """

        super().__init__(tokenizer, columns, maxlength)

        if not self.columns:
            self.columns = ("source", "target")

        self.prefix = prefix

    def process(self, data):
        source, target = self.columns

        source = [self.prefix + x if self.prefix else x for x in data[source]]
        inputs = self.tokenizer(source, max_length=self.maxlength, padding=False, truncation=True)

        with self.tokenizer.as_target_tokenizer():
            targets = self.tokenizer(data[target], max_length=self.maxlength, padding=False, truncation=True)

        inputs["labels"] = targets["input_ids"]

        return inputs
