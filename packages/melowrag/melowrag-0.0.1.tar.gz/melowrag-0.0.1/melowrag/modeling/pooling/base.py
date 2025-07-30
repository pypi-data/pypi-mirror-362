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
from torch import nn

from ..models import Models


class Pooling(nn.Module):
    """
    Builds pooled vectors usings outputs from a transformers model.
    """

    def __init__(self, path, device, tokenizer=None, maxlength=None, modelargs=None):
        """
        Creates a new Pooling model.

        Args:
            path: path to model, accepts Hugging Face model hub id or local path
            device: tensor device id
            tokenizer: optional path to tokenizer
            maxlength: max sequence length
            modelargs: additional model arguments
        """

        super().__init__()

        self.model = Models.load(path, modelargs=modelargs)
        self.tokenizer = Models.tokenizer(tokenizer if tokenizer else path)
        self.device = Models.device(device)

        Models.checklength(self.model, self.tokenizer)

        self.maxlength = (
            maxlength
            if maxlength
            else self.tokenizer.model_max_length
            if self.tokenizer.model_max_length != int(1e30)
            else None
        )

        self.to(self.device)

    def encode(self, documents, batch=32):
        """
        Builds an array of pooled embeddings for documents.

        Args:
            documents: list of documents used to build embeddings
            batch: model batch size

        Returns:
            pooled embeddings
        """

        results = []

        lengths = np.argsort([-len(x) if x else 0 for x in documents])
        documents = [documents[x] for x in lengths]

        for chunk in self.chunk(documents, batch):
            inputs = self.tokenizer(
                chunk, padding=True, truncation="longest_first", return_tensors="pt", max_length=self.maxlength
            )

            inputs = inputs.to(self.device)

            with torch.no_grad():
                outputs = self.forward(**inputs)

            results.extend(outputs.cpu().numpy())

        return np.asarray([results[x] for x in np.argsort(lengths)])

    def chunk(self, texts, size):
        """
        Splits texts into separate batch sizes specified by size.

        Args:
            texts: text elements
            size: batch size

        Returns:
            list of evenly sized batches with the last batch having the remaining elements
        """

        return [texts[x : x + size] for x in range(0, len(texts), size)]

    def forward(self, **inputs):
        """
        Runs inputs through transformers model and returns outputs.

        Args:
            inputs: model inputs

        Returns:
            model outputs
        """

        return self.model(**inputs)[0]
