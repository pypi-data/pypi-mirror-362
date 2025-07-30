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

from ..modeling import Models
from .tensors import Tensors


class HFModel(Tensors):
    """
    Pipeline backed by a Hugging Face Transformers model.
    """

    def __init__(self, path=None, quantize=False, gpu=False, batch=64):
        """
        Creates a new HFModel.

        Args:
            path: optional path to model, accepts Hugging Face model hub id or local path,
                  uses default model for task if not provided
            quantize: if model should be quantized, defaults to False
            gpu: True/False if GPU should be enabled, also supports a GPU device id
            batch: batch size used to incrementally process content
        """

        self.path = path

        self.quantization = quantize

        self.deviceid = Models.deviceid(gpu)
        self.device = Models.device(self.deviceid)

        self.batchsize = batch

    def prepare(self, model):
        """
        Prepares a model for processing. Applies dynamic quantization if necessary.

        Args:
            model: input model

        Returns:
            model
        """

        if self.deviceid == -1 and self.quantization:
            model = self.quantize(model)

        return model

    def tokenize(self, tokenizer, texts):
        """
        Tokenizes text using tokenizer. This method handles overflowing tokens and automatically splits
        them into separate elements. Indices of each element is returned to allow reconstructing the
        transformed elements after running through the model.

        Args:
            tokenizer: Tokenizer
            texts: list of text

        Returns:
            (tokenization result, indices)
        """

        batch, positions = [], []
        for x, text in enumerate(texts):
            elements = [t + " " for t in text.split("\n") if t]
            batch.extend(elements)
            positions.extend([x] * len(elements))

        tokens = tokenizer(batch, padding=True)

        inputids, attention, indices = [], [], []
        for x, ids in enumerate(tokens["input_ids"]):
            if len(ids) > tokenizer.model_max_length:
                ids = [i for i in ids if i != tokenizer.pad_token_id]

                for chunk in self.batch(ids, tokenizer.model_max_length - 1):
                    if chunk[-1] != tokenizer.eos_token_id:
                        chunk.append(tokenizer.eos_token_id)

                    mask = [1] * len(chunk)

                    if len(chunk) < tokenizer.model_max_length:
                        pad = tokenizer.model_max_length - len(chunk)
                        chunk.extend([tokenizer.pad_token_id] * pad)
                        mask.extend([0] * pad)

                    inputids.append(chunk)
                    attention.append(mask)
                    indices.append(positions[x])
            else:
                inputids.append(ids)
                attention.append(tokens["attention_mask"][x])
                indices.append(positions[x])

        tokens = {"input_ids": inputids, "attention_mask": attention}

        # pylint: disable=E1102
        return ({name: self.tensor(tensor).to(self.device) for name, tensor in tokens.items()}, indices)
