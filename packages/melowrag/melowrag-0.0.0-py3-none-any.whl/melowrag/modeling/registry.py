from transformers import AutoModel, AutoModelForQuestionAnswering, AutoModelForSequenceClassification
from transformers.models.auto.tokenization_auto import TOKENIZER_MAPPING


class Registry:
    """
    Methods to register models and fully support pipelines.
    """

    @staticmethod
    def register(model, config=None):
        """
        Registers a model with auto model and tokenizer configuration to fully support pipelines.

        Args:
            model: model to register
            config: config class name
        """

        config = config if config else model.__class__

        if hasattr(model.__class__, "config_class") and not model.__class__.config_class:
            model.__class__.config_class = config

        for mapping in [AutoModel, AutoModelForQuestionAnswering, AutoModelForSequenceClassification]:
            mapping.register(config, model.__class__)

        if hasattr(model, "config") and type(model.config) not in TOKENIZER_MAPPING:
            TOKENIZER_MAPPING.register(type(model.config), type(model.config).__name__)
