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

from ..utilities import Resolver
from .hub import HuggingFaceHub
from .storage import LIBCLOUD, ObjectStorage


class CloudFactory:
    """
    Methods to create Cloud instances.
    """

    @staticmethod
    def create(config):
        """
        Creates a Cloud instance.

        Args:
            config: cloud configuration

        Returns:
            Cloud
        """

        cloud = None

        provider = config.get("provider", "")

        if provider.lower() == "huggingface-hub":
            cloud = HuggingFaceHub(config)

        elif ObjectStorage.isprovider(provider):
            cloud = ObjectStorage(config)

        elif provider:
            cloud = CloudFactory.resolve(provider, config)

        return cloud

    @staticmethod
    def resolve(backend, config):
        """
        Attempt to resolve a custom cloud backend.

        Args:
            backend: backend class
            config: configuration parameters

        Returns:
            Cloud
        """

        try:
            return Resolver()(backend)(config)

        except Exception as e:
            message = f'Unable to resolve cloud backend: "{backend}".'

            message += ' Cloud storage is not available - install "cloud" extra to enable' if not LIBCLOUD else ""

            raise ImportError(message) from e
