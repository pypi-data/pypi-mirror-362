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

from ...utilities import Resolver
from .base import Encoder
from .serialize import SerializeEncoder


class EncoderFactory:
    """
    Encoder factory. Creates new Encoder instances.
    """

    @staticmethod
    def get(encoder):
        """
        Gets a new instance of encoder class.

        Args:
            encoder: Encoder instance class

        Returns:
            Encoder class
        """

        if "." not in encoder:
            encoder = ".".join(__name__.split(".")[:-1]) + "." + encoder.capitalize() + "Encoder"

        return Resolver()(encoder)

    @staticmethod
    def create(encoder):
        """
        Creates a new Encoder instance.

        Args:
            encoder: Encoder instance class

        Returns:
            Encoder
        """

        if encoder is True:
            return Encoder()

        if encoder in ["messagepack", "pickle"]:
            return SerializeEncoder(encoder)

        return EncoderFactory.get(encoder)()
