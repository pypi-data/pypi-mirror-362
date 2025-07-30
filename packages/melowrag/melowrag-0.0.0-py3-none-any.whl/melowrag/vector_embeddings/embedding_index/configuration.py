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
