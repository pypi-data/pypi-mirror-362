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

from .tokens import Tokens


class Data:
    """
    Base data tokenization class.
    """

    def __init__(self, tokenizer, columns, maxlength):
        """
        Creates new base instance for tokenizing data.

        Args:
            tokenizer: model tokenizer
            columns: column names
            maxlength: maximum sequence length
        """

        self.tokenizer = tokenizer
        self.columns = columns
        self.maxlength = maxlength

    def __call__(self, train, validation, workers):
        """
        Tokenizes training and validation data and returns processed datasets.

        Args:
            train: training data
            validation: validation data
            workers: number of concurrent tokenizers when processing datasets, only main process used when set to None

        Returns:
            (train, validation)
        """

        return (
            self.prepare(train, self.process, workers),
            self.prepare(validation, self.process, workers) if validation else None,
        )

    def prepare(self, data, fn, workers):
        """
        Prepares and tokenizes data for training.

        Args:
            data: input data
            fn: tokenize processing function to apply
            workers: number of concurrent tokenizers when processing datasets, only main process used when set to None

        Returns:
            tokens
        """

        if hasattr(data, "map"):
            tokens = data.map(fn, batched=True, num_proc=workers, remove_columns=data.column_names)
        else:
            columns = {}
            if hasattr(data, "columns"):
                for column in data.columns:
                    columns[column] = list(data[column])
            else:
                for row in data:
                    for column in row.keys():
                        if column not in columns:
                            columns[column] = []

                        columns[column].append(row[column])

            tokens = Tokens(fn(columns))

        return tokens

    def labels(self, data):
        """
        Extracts a list of unique labels from data.

        Args:
            data: input data

        Returns:
            list of unique labels
        """

        column = self.columns[-1]

        length = self.length(data[column][0] if hasattr(data, "columns") else data[0][column])
        if length:
            return length

        if hasattr(data, "map"):
            labels = sorted(data.unique(self.columns[-1]))
        elif hasattr(data, "columns"):
            labels = sorted(data[self.columns[-1]].unique())
        else:
            labels = sorted({row[self.columns[-1]] for row in data})

        return 1 if [x for x in labels if float(x) != int(x)] else len(labels)

    def process(self, data):
        """
        Tokenizes batch of input data

        Args:
            data: input data batch

        Returns:
            tokenized data
        """

        return data

    def length(self, value):
        """
        Returns the length of value if value has a len function defined. Otherwise,
        None is returned.

        Args:
            value: value to check

        Returns:
            length of value if available, otherwise returns None
        """

        return len(value) if hasattr(value, "__len__") else None
