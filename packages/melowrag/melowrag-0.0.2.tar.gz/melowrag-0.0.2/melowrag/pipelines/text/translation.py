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

"""
Translation module
"""

try:
    from staticvectors import StaticVectors

    STATICVECTORS = True
except ImportError:
    STATICVECTORS = False

from huggingface_hub.hf_api import HfApi
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from ...modeling import Models
from ..hfmodel import HFModel


class Translation(HFModel):
    """
    Translates text from source language into target language.
    """

    DEFAULT_LANG_DETECT = "neuml/language-id-quantized"

    def __init__(self, path=None, quantize=False, gpu=True, batch=64, langdetect=None, findmodels=True):
        """
        Constructs a new language translation pipeline.

        Args:
            path: optional path to model, accepts Hugging Face model hub id or local path,
                  uses default model for task if not provided
            quantize: if model should be quantized, defaults to False
            gpu: True/False if GPU should be enabled, also supports a GPU device id
            batch: batch size used to incrementally process content
            langdetect: set a custom language detection function, method must take a list of strings and return
                        language codes for each, uses default language detector if not provided
            findmodels: True/False if the Hugging Face Hub will be searched for source-target translation models
        """

        super().__init__(path if path else "facebook/m2m100_418M", quantize, gpu, batch)

        self.detector = None
        self.langdetect = langdetect
        self.findmodels = findmodels

        self.models = {}
        self.ids = None

    def __call__(self, texts, target="en", source=None, showmodels=False):
        """
        Translates text from source language into target language.

        This method supports texts as a string or a list. If the input is a string,
        the return type is string. If text is a list, the return type is a list.

        Args:
            texts: text|list
            target: target language code, defaults to "en"
            source: source language code, detects language if not provided

        Returns:
            list of translated text
        """

        values = [texts] if not isinstance(texts, list) else texts

        languages = self.detect(values) if not source else [source] * len(values)
        unique = set(languages)

        langdict = {}
        for x, lang in enumerate(languages):
            if lang not in langdict:
                langdict[lang] = []
            langdict[lang].append((x, values[x]))

        results = {}
        for language in unique:
            inputs = langdict[language]

            outputs = []
            for chunk in self.batch([text for _, text in inputs], self.batchsize):
                outputs.extend(self.translate(chunk, language, target, showmodels))

            for y, (x, _) in enumerate(inputs):
                if showmodels:
                    model, op = outputs[y]
                    results[x] = (op.strip(), language, model)
                else:
                    results[x] = outputs[y].strip()

        results = [results[x] for x in sorted(results)]
        return results[0] if isinstance(texts, str) else results

    def modelids(self):
        """
        Runs a query to get a list of available language models from the Hugging Face API.

        Returns:
            list of source-target language model ids
        """

        ids = [x.id for x in HfApi().list_models(author="Helsinki-NLP")] if self.findmodels else []
        return set(ids)

    def detect(self, texts):
        """
        Detects the language for each element in texts.

        Args:
            texts: list of text

        Returns:
            list of languages
        """

        if not self.langdetect or isinstance(self.langdetect, str):
            return self.defaultdetect(texts)

        return self.langdetect(texts)

    def defaultdetect(self, texts):
        """
        Default language detection model.

        Args:
            texts: list of text

        Returns:
            list of languages
        """

        if not self.detector:
            if not STATICVECTORS:
                raise ImportError('Language detection is not available - install "pipeline" extra to enable')

            path = self.langdetect if self.langdetect else Translation.DEFAULT_LANG_DETECT

            self.detector = StaticVectors(path)

        texts = [x.lower().replace("\n", " ").replace("\r\n", " ") for x in texts]

        return [x[0][0] for x in self.detector.predict(texts)]

    def translate(self, texts, source, target, showmodels=False):
        """
        Translates text from source to target language.

        Args:
            texts: list of text
            source: source language code
            target: target language code

        Returns:
            list of translated text
        """

        if source == target:
            return texts

        path, model, tokenizer = self.lookup(source, target)

        model.to(self.device)
        indices = None
        maxlength = Models.maxlength(model, tokenizer)

        with self.context():
            if hasattr(tokenizer, "lang_code_to_id"):
                source = self.langid(tokenizer.lang_code_to_id, source)
                target = self.langid(tokenizer.lang_code_to_id, target)

                tokenizer.src_lang = source
                tokens, indices = self.tokenize(tokenizer, texts)

                translated = model.generate(
                    **tokens, forced_bos_token_id=tokenizer.lang_code_to_id[target], max_length=maxlength
                )
            else:
                tokens, indices = self.tokenize(tokenizer, texts)
                translated = model.generate(**tokens, max_length=maxlength)

        translated = tokenizer.batch_decode(translated, skip_special_tokens=True)

        results, last = [], -1
        for x, i in enumerate(indices):
            v = (path, translated[x]) if showmodels else translated[x]
            if i == last:
                results[-1] += v
            else:
                results.append(v)

            last = i

        return results

    def lookup(self, source, target):
        """
        Retrieves a translation model for source->target language. This method caches each model loaded.

        Args:
            source: source language code
            target: target language code

        Returns:
            (model, tokenizer)
        """

        path = self.modelpath(source, target)
        if path not in self.models:
            self.models[path] = self.load(path)

        return (path,) + self.models[path]

    def modelpath(self, source, target):
        """
        Derives a translation model path given source and target languages.

        Args:
            source: source language code
            target: target language code

        Returns:
            model path
        """

        if self.ids is None:
            self.ids = self.modelids()

        template = "Helsinki-NLP/opus-mt-%s-%s"
        path = template % (source, target)
        if path in self.ids:
            return path

        if self.findmodels and target == "en":
            return template % ("mul", target)

        return self.path

    def load(self, path):
        """
        Loads a model specified by path.

        Args:
            path: model path

        Returns:
            (model, tokenizer)
        """

        model = AutoModelForSeq2SeqLM.from_pretrained(path)
        tokenizer = AutoTokenizer.from_pretrained(path)

        model = self.prepare(model)

        return (model, tokenizer)

    def langid(self, languages, target):
        """
        Searches a list of languages for a prefix match on target.

        Args:
            languages: list of languages
            target: target language code

        Returns:
            best match or None if no match found
        """

        for lang in languages:
            if lang.startswith(target):
                return lang

        return None
