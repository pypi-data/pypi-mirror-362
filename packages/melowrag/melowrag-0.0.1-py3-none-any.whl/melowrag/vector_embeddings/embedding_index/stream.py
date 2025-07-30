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

from .autoid import AutoId
from .transform import Action


class Stream:
    """
    Yields input document as standard (id, data, tags) tuples.
    """

    def __init__(self, embeddings, action=None):
        """
        Create a new stream.

        Args:
            embeddings: embeddings instance
            action: optional index action
        """

        self.embeddings = embeddings
        self.action = action

        self.config = embeddings.config

        self.offset = self.config.get("offset", 0) if action == Action.UPSERT else 0
        autoid = self.config.get("autoid", self.offset)

        autoid = 0 if isinstance(autoid, int) and action != Action.UPSERT else autoid
        self.autoid = AutoId(autoid)

    def __call__(self, documents):
        """
        Yield (id, data, tags) tuples from a stream of documents.

        Args:
            documents: input documents
        """

        for document in documents:
            if isinstance(document, dict):
                document = document.get("id"), document, document.get("tags")
            elif isinstance(document, tuple):
                document = document if len(document) >= 3 else (document[0], document[1], None)
            else:
                document = None, document, None

            if self.action and document[0] is None:
                document = (self.autoid(document[1]), document[1], document[2])

            yield document

        current = self.autoid.current()
        if self.action and current:
            self.config["autoid"] = current
