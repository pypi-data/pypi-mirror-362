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
