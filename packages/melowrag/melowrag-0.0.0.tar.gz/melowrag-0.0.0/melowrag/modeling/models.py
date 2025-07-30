import os

import torch
from transformers import (
    AutoConfig,
    AutoModel,
    AutoModelForQuestionAnswering,
    AutoModelForSeq2SeqLM,
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
from transformers.models.auto.modeling_auto import MODEL_FOR_IMAGE_TEXT_TO_TEXT_MAPPING_NAMES

from .onnx import OnnxModel


class Models:
    """
    Utility methods for working with machine learning models
    """

    @staticmethod
    def checklength(config, tokenizer):
        """
        Checks the length for a Hugging Face Transformers tokenizer using a Hugging Face Transformers config. Copies the
        max_position_embeddings parameter if the tokenizer has no max_length set. This helps with backwards compatibility
        with older tokenizers.

        Args:
            config: transformers config
            tokenizer: transformers tokenizer
        """

        if hasattr(config, "config"):
            config = config.config

        if (
            hasattr(config, "max_position_embeddings")
            and tokenizer
            and hasattr(tokenizer, "model_max_length")
            and tokenizer.model_max_length == int(1e30)
        ):
            tokenizer.model_max_length = config.max_position_embeddings

    @staticmethod
    def maxlength(config, tokenizer):
        """
        Gets the best max length to use for generate calls. This method will return config.max_length if it's set.
        Otherwise, it will return tokenizer.model_max_length.

        Args:
            config: transformers config
            tokenizer: transformers tokenizer
        """

        if hasattr(config, "config"):
            config = config.config

        keys = config.to_diff_dict()

        return (
            config.max_length
            if "max_length" in keys or not hasattr(tokenizer, "model_max_length")
            else tokenizer.model_max_length
        )

    @staticmethod
    def deviceid(gpu):
        """
        Translates input gpu argument into a device id.

        Args:
            gpu: True/False if GPU should be enabled, also supports a device id/string/instance

        Returns:
            device id
        """

        # pylint: disable=E1101
        if isinstance(gpu, torch.device):
            return gpu

        if gpu is None or not Models.hasaccelerator():
            return -1

        if isinstance(gpu, bool):
            return 0 if gpu else -1

        return int(gpu)

    @staticmethod
    def device(deviceid):
        """
        Gets a tensor device.

        Args:
            deviceid: device id

        Returns:
            tensor device
        """

        # pylint: disable=E1101
        return deviceid if isinstance(deviceid, torch.device) else torch.device(Models.reference(deviceid))

    @staticmethod
    def reference(deviceid):
        """
        Gets a tensor device reference.

        Args:
            deviceid: device id

        Returns:
            device reference
        """

        return (
            deviceid
            if isinstance(deviceid, str)
            else (
                "cpu"
                if deviceid < 0
                else f"cuda:{deviceid}"
                if torch.cuda.is_available()
                else "mps"
                if Models.hasmpsdevice()
                else Models.finddevice()
            )
        )

    @staticmethod
    def acceleratorcount():
        """
        Gets the number of accelerator devices available.

        Returns:
            number of accelerators available
        """

        return max(torch.cuda.device_count(), int(Models.hasaccelerator()))

    @staticmethod
    def hasaccelerator():
        """
        Checks if there is an accelerator device available.

        Returns:
            True if an accelerator device is available, False otherwise
        """

        return torch.cuda.is_available() or Models.hasmpsdevice() or bool(Models.finddevice())

    @staticmethod
    def hasmpsdevice():
        """
        Checks if there is a MPS device available.

        Returns:
            True if a MPS device is available, False otherwise
        """

        return os.environ.get("PYTORCH_MPS_DISABLE") != "1" and torch.backends.mps.is_available()

    @staticmethod
    def finddevice():
        """
        Attempts to find an alternative accelerator device.

        Returns:
            name of first alternative accelerator available or None if not found
        """

        return next(
            (device for device in ["xpu"] if hasattr(torch, device) and getattr(torch, device).is_available()), None
        )

    @staticmethod
    def load(path, config=None, task="default", modelargs=None):
        """
        Loads a machine learning model. Handles multiple model frameworks (ONNX, Transformers).

        Args:
            path: path to model
            config: path to model configuration
            task: task name used to lookup model type

        Returns:
            machine learning model
        """

        if isinstance(path, bytes) or (isinstance(path, str) and os.path.isfile(path)):
            return OnnxModel(path, config)

        if not isinstance(path, str):
            return path

        models = {
            "default": AutoModel.from_pretrained,
            "question-answering": AutoModelForQuestionAnswering.from_pretrained,
            "summarization": AutoModelForSeq2SeqLM.from_pretrained,
            "text-classification": AutoModelForSequenceClassification.from_pretrained,
            "zero-shot-classification": AutoModelForSequenceClassification.from_pretrained,
        }

        modelargs = modelargs if modelargs else {}

        return models[task](path, **modelargs) if task in models else path

    @staticmethod
    def tokenizer(path, **kwargs):
        """
        Loads a tokenizer from path.

        Args:
            path: path to tokenizer
            kwargs: optional additional keyword arguments

        Returns:
            tokenizer
        """

        return AutoTokenizer.from_pretrained(path, **kwargs) if isinstance(path, str) else path

    @staticmethod
    def task(path, **kwargs):
        """
        Attempts to detect the model task from path.

        Args:
            path: path to model
            kwargs: optional additional keyword arguments

        Returns:
            inferred model task
        """

        config = None
        if isinstance(path, list | tuple) and hasattr(path[0], "config"):
            config = path[0].config
        elif isinstance(path, str):
            config = AutoConfig.from_pretrained(path, **kwargs)

        task = None
        if config:
            architecture = config.architectures[0] if config.architectures else None
            if architecture:
                if architecture in MODEL_FOR_IMAGE_TEXT_TO_TEXT_MAPPING_NAMES.values():
                    task = "vision"
                elif any(x for x in ["LMHead", "CausalLM"] if x in architecture):
                    task = "language-generation"
                elif "QuestionAnswering" in architecture:
                    task = "question-answering"
                elif "ConditionalGeneration" in architecture:
                    task = "sequence-sequence"

        return task
