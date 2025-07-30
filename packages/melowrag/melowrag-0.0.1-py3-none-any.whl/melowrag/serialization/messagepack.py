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

import msgpack
from msgpack import Unpacker
from msgpack.exceptions import ExtraData

from .base import Serialize
from .errors import SerializeError


class MessagePack(Serialize):
    """
    MessagePack serialization.
    """

    def __init__(self, streaming=False, **kwargs):
        super().__init__()

        self.streaming = streaming

        self.kwargs = kwargs

    def loadstream(self, stream):
        try:
            return Unpacker(stream, **self.kwargs) if self.streaming else msgpack.unpack(stream)
        except ExtraData as e:
            raise SerializeError(e) from e

    def savestream(self, data, stream):
        msgpack.pack(data, stream)

    def loadbytes(self, data):
        return msgpack.unpackb(data)

    def savebytes(self, data):
        return msgpack.packb(data)
