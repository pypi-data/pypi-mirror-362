import json
import os

from huggingface_hub.errors import HFValidationError
from transformers.utils import cached_file

from .base import Pooling
from .cls import ClsPooling
from .mean import MeanPooling


class PoolingFactory:
    """
    Method to create pooling models.
    """

    @staticmethod
    def create(config):
        """
        Create a Pooling model.

        Args:
            config: pooling configuration

        Returns:
            Pooling
        """

        method, path, device, tokenizer, maxlength, modelargs = [
            config.get(x) for x in ["method", "path", "device", "tokenizer", "maxlength", "modelargs"]
        ]

        maxlength = PoolingFactory.maxlength(path) if isinstance(maxlength, bool) and maxlength else maxlength

        if isinstance(path, bytes) or (isinstance(path, str) and os.path.isfile(path)) or method == "pooling":
            return Pooling(path, device, tokenizer, maxlength, modelargs)

        if (not method or method not in ("clspooling", "meanpooling")) and (
            isinstance(path, str) and not os.path.exists(path)
        ):
            method = PoolingFactory.method(path)

        if method == "clspooling":
            return ClsPooling(path, device, tokenizer, maxlength, modelargs)

        return MeanPooling(path, device, tokenizer, maxlength, modelargs)

    @staticmethod
    def method(path):
        """
        Determines the pooling method using the sentence transformers pooling config.

        Args:
            path: model path

        Returns:
            pooling method
        """

        method = "meanpooling"

        config = PoolingFactory.load(path, "1_Pooling/config.json")

        if config and config["pooling_mode_cls_token"] and not config["pooling_mode_mean_tokens"]:
            method = "clspooling"

        return method

    @staticmethod
    def maxlength(path):
        """
        Reads the max_seq_length parameter from sentence transformers config.

        Args:
            path: model path

        Returns:
            max sequence length
        """

        maxlength = None

        config = PoolingFactory.load(path, "sentence_bert_config.json")
        maxlength = config.get("max_seq_length") if config else maxlength

        return maxlength

    @staticmethod
    def load(path, name):
        """
        Loads a JSON config file from the Hugging Face Hub.

        Args:
            path: model path
            name: file to load

        Returns:
            config
        """

        config = None
        try:
            path = cached_file(path_or_repo_id=path, filename=name)
            if path:
                with open(path, encoding="utf-8") as f:
                    config = json.load(f)

        except (HFValidationError, OSError):
            pass

        return config
