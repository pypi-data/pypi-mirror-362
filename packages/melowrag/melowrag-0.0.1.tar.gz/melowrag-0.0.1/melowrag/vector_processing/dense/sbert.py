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

try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS = True
except ImportError:
    SENTENCE_TRANSFORMERS = False

from ...modeling import Models
from ..base import Vectors


class STVectors(Vectors):
    """
    Builds vectors using sentence-transformers (aka SBERT).
    """

    def __init__(self, config, scoring, models):
        if not SENTENCE_TRANSFORMERS:
            raise ImportError('sentence-transformers is not available - install "vectors" extra to enable')

        self.pool = None

        super().__init__(config, scoring, models)

    def loadmodel(self, path):
        gpu, pool = self.config.get("gpu", True), False

        if isinstance(gpu, str) and gpu == "all":
            devices = Models.acceleratorcount()

            gpu, pool = devices <= 1, devices > 1

        deviceid = Models.deviceid(gpu)

        modelargs = self.config.get("vectors", {})

        model = self.loadencoder(path, device=Models.device(deviceid), **modelargs)

        if pool:
            self.pool = model.start_multi_process_pool()

        return model

    def encode(self, data, category=None):
        encode = (
            self.model.encode_query
            if category == "query"
            else self.model.encode_document
            if category == "data"
            else self.model.encode
        )

        encodeargs = self.config.get("encodeargs", {})

        return encode(data, pool=self.pool, batch_size=self.encodebatch, **encodeargs)

    def close(self):
        if self.pool:
            self.model.stop_multi_process_pool(self.pool)
            self.pool = None

        super().close()

    def loadencoder(self, path, device, **kwargs):
        """
        Loads the embeddings encoder model from path.

        Args:
            path: model path
            device: tensor device
            kwargs: additional keyword args

        Returns:
            embeddings encoder
        """

        return SentenceTransformer(path, device=device, **kwargs)
