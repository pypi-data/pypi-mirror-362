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

"""
This module provides the Query class for query translation using transformer models.
"""

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, T5ForConditionalGeneration


class Query:
    """
    Query translation model using transformer-based sequence-to-sequence models.

    Args:
        path (str): Path to the query model.
        prefix (str, optional): Text prefix for the model.
        maxlength (int, optional): Maximum sequence length to generate.
    """

    def __init__(self, path, prefix=None, maxlength=512):
        """
        Creates a query translation model.

        Args:
            path: path to query model
            prefix: text prefix
            maxlength: max sequence length to generate
        """

        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(path)

        if not prefix and isinstance(self.model, T5ForConditionalGeneration):
            prefix = "translate English to SQL: "

        self.prefix = prefix
        self.maxlength = maxlength

    def __call__(self, query):
        """
        Runs query translation model.

        Args:
            query: input query

        Returns:
            transformed query
        """

        if self.prefix:
            query = f"{self.prefix}{query}"

        features = self.tokenizer([query], return_tensors="pt")
        output = self.model.generate(
            input_ids=features["input_ids"], attention_mask=features["attention_mask"], max_length=self.maxlength
        )

        result = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return self.clean(result)

    def clean(self, text):
        """
        Applies a series of rules to clean generated text.

        Args:
            text: input text

        Returns:
            clean text
        """

        return text.replace("$=", "<=")
