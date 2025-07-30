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

import json
import os

from ...serialization import SerializeFactory


class Configuration:
    """
    Loads and saves index configuration.
    """

    def load(self, path):
        """
        Loads index configuration. This method supports both config.json and config pickle files.

        Args:
            path: path to directory

        Returns:
            dict
        """

        config = None

        jsonconfig = os.path.exists(f"{path}/config.json")

        name = "config.json" if jsonconfig else "config"

        with open(f"{path}/{name}", "r" if jsonconfig else "rb", encoding="utf-8" if jsonconfig else None) as handle:
            config = json.load(handle) if jsonconfig else SerializeFactory.create("pickle").loadstream(handle)

        config["format"] = "json" if jsonconfig else "pickle"

        return config

    def save(self, config, path):
        """
        Saves index configuration. This method defaults to JSON and falls back to pickle.

        Args:
            config: configuration to save
            path: path to directory

        Returns:
            dict
        """

        jsonconfig = config.get("format", "json") == "json"

        name = "config.json" if jsonconfig else "config"

        with open(f"{path}/{name}", "w" if jsonconfig else "wb", encoding="utf-8" if jsonconfig else None) as handle:
            if jsonconfig:
                json.dump(config, handle, default=str, indent=2)
            else:
                SerializeFactory.create("pickle").savestream(config, handle)
