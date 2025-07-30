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

try:
    import onnxruntime as ort
    import soundfile as sf
    from ttstokenizer import IPATokenizer, TTSTokenizer  # type:ignore

    from .signal import SCIPY, Signal

    TTS = SCIPY
except ImportError:
    TTS = False

import json
import logging
from io import BytesIO

import numpy as np
import torch
import yaml
from huggingface_hub.errors import HFValidationError
from transformers import SpeechT5Processor
from transformers.utils import cached_file

from ..base import Pipeline

logger = logging.getLogger(__name__)


class TextToSpeech(Pipeline):
    """
    Generates speech from text.
    """

    def __init__(self, path=None, maxtokens=512, rate=22050):
        """
        Creates a new TextToSpeech pipeline.

        Args:
            path: optional model path
            maxtokens: maximum number of tokens model can process, defaults to 512
            rate: target sample rate, defaults to 22050
        """

        if not TTS:
            raise ImportError('TextToSpeech pipeline is not available - install "pipeline" extra to enable')

        path = path if path else "neuml/ljspeech-jets-onnx"

        self.rate = rate

        self.pipeline = None
        if self.hasfile(path, "model.onnx") and self.hasfile(path, "config.yaml"):
            self.pipeline = ESPnet(path, maxtokens, self.providers())
        elif self.hasfile(path, "model.onnx") and self.hasfile(path, "voices.json"):
            self.pipeline = Kokoro(path, maxtokens, self.providers())
        else:
            self.pipeline = SpeechT5(path, maxtokens, self.providers())

    def __call__(self, text, stream=False, speaker=1, encoding=None, **kwargs):
        """
        Generates speech from text. Text longer than maxtokens will be batched and returned
        as a single waveform per text input.

        This method supports text as a string or a list. If the input is a string,
        the return type is audio. If text is a list, the return type is a list.

        Args:
            text: text|list
            stream: stream response if True, defaults to False
            speaker: speaker id, defaults to 1
            encoding: optional audio encoding format
            kwargs: additional keyword args

        Returns:
            list of (audio, sample rate) or list of audio depending on encoding parameter
        """

        texts = [text] if isinstance(text, str) else text

        if stream:
            return self.stream(texts, speaker, encoding)

        results = [self.execute(x, speaker, encoding, **kwargs) for x in texts]

        return results[0] if isinstance(text, str) else results

    def providers(self):
        """
        Returns a list of available and usable providers.

        Returns:
            list of available and usable providers
        """

        if torch.cuda.is_available() and "CUDAExecutionProvider" in ort.get_available_providers():
            return [("CUDAExecutionProvider", {"cudnn_conv_algo_search": "DEFAULT"}), "CPUExecutionProvider"]

        return ["CPUExecutionProvider"]

    def hasfile(self, path, name):
        """
        Tests if a file exists in a local or remote repo.

        Args:
            path: model path
            name: file name

        Returns:
            True if name exists in path, False otherwise
        """

        exists = False
        try:
            exists = cached_file(path_or_repo_id=path, filename=name) is not None
        except (HFValidationError, OSError):
            return False

        return exists

    def stream(self, texts, speaker, encoding):
        """
        Iterates over texts, splits into segments and yields snippets of audio.
        This method is designed to integrate with streaming LLM generation.

        Args:
            texts: list of input texts
            speaker: speaker id
            encoding: audio encoding format

        Returns:
            snippets of audio as NumPy arrays or audio bytes depending on encoding parameter
        """

        buffer = []
        for x in texts:
            buffer.append(x)

            if x == "\n" or (x.strip().endswith(".") and len([y for y in buffer if y]) > 2):
                data, buffer = "".join(buffer), []
                yield self.execute(data, speaker, encoding)

        if buffer:
            data = "".join(buffer)
            yield self.execute(data, speaker, encoding)

    def execute(self, text, speaker, encoding, **kwargs):
        """
        Executes model run for an input array of tokens. This method will build batches
        of tokens when len(tokens) > maxtokens.

        Args:
            text: text to tokenize and pass to model
            speaker: speaker id
            encoding: audio encoding format
            kwargs: additional keyword args

        Returns:
            (audio, sample rate) or audio bytes depending on encoding parameter
        """

        audio, rate = self.pipeline(text, speaker, **kwargs)

        audio, rate = (Signal.resample(audio, rate, self.rate), self.rate) if self.rate else (audio, rate)

        if encoding:
            data = BytesIO()
            sf.write(data, audio, rate, format=encoding)
            return data.getvalue()

        return (audio, rate)


class SpeechPipeline(Pipeline):
    """
    Base class for speech pipelines
    """

    # pylint: disable=W0221
    def chunk(self, data, size, punctids):
        """
        Batching method that takes punctuation into account. This method splits data up to size
        chunks. But it also searches the batch and splits on the last punctuation token id.

        Args:
            data: data
            size: batch size
            punctids: list of punctuation token ids

        Returns:
            yields batches of data
        """

        punct, index = 0, 0
        for i, x in enumerate(data):
            if x in punctids:
                punct = i

            if i - index >= (size - 1):
                end = (punct if punct > index else i) + 1
                yield data[index:end]
                index = end

        if index < len(data):
            yield data[index : len(data)]


class ESPnet(SpeechPipeline):
    """
    Text to Speech pipeline with an ESPnet ONNX model.
    """

    def __init__(self, path, maxtokens, providers):
        """
        Creates a new ESPnet pipeline.

        Args:
            path: model path
            maxtokens: maximum number of tokens model can process
            providers: list of supported ONNX providers
        """

        config = cached_file(path_or_repo_id=path, filename="config.yaml")
        model = cached_file(path_or_repo_id=path, filename="model.onnx")

        with open(config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        tokens = config.get("token", {}).get("list")
        self.tokenizer = TTSTokenizer(tokens)

        self.model = ort.InferenceSession(model, ort.SessionOptions(), providers)

        self.maxtokens = maxtokens

        self.input = self.model.get_inputs()[0].name

        self.params = set(x.name for x in self.model.get_inputs())

    def __call__(self, text, speaker):
        """
        Executes a model run. This method will build batches of tokens when len(tokens) > maxtokens.

        Args:
            text: text to tokenize and pass to model
            speaker: speaker id

        Returns:
            (audio, sample rate)
        """

        logger.debug("%s", text)

        rate = 22050

        tokens = self.tokenizer(text)

        results = []
        for i, x in enumerate(self.chunk(tokens, self.maxtokens, self.tokenizer.punctuation())):
            params = {self.input: x}
            params = {**params, **{"sids": np.array([speaker])}} if "sids" in self.params else params

            output = self.model.run(None, params)
            results.append(Signal.trim(output[0], rate, trailing=False) if i > 0 else output[0])

        return (np.concatenate(results), rate)


class Kokoro(SpeechPipeline):
    """
    Text to Speech pipeline with an Kokoro ONNX model.
    """

    def __init__(self, path, maxtokens, providers):
        """
        Creates a new Kokoro pipeline.

        Args:
            path: model path
            maxtokens: maximum number of tokens model can process
            providers: list of supported ONNX providers
        """

        voices = cached_file(path_or_repo_id=path, filename="voices.json")
        model = cached_file(path_or_repo_id=path, filename="model.onnx")

        with open(voices, "r", encoding="utf-8") as f:
            self.voices = json.load(f)

        self.tokenizer = IPATokenizer()

        self.model = ort.InferenceSession(model, ort.SessionOptions(), providers)

        self.maxtokens = min(maxtokens, 510)

        self.input = self.model.get_inputs()[0].name

        self.params = set(x.name for x in self.model.get_inputs())

    def __call__(self, text, speaker=None, speed=1.0, transcribe=True):
        """
        Executes a model run. This method will build batches of tokens when len(tokens) > maxtokens.

        Args:
            text: text to tokenize and pass to model
            speaker: speaker id, defaults to first speaker
            speed: defaults to 1.0
            transcribe: if text should be transcriped to IPA text, defaults to True

        Returns:
            (audio, sample rate)
        """

        logger.debug("%s", text)

        rate = 24000

        speaker = speaker if speaker in self.voices else next(iter(self.voices))
        speaker = np.array(self.voices[speaker], dtype=np.float32)

        self.tokenizer.transcribe = transcribe
        tokens = self.tokenizer(text)

        results = []
        for i, x in enumerate(self.chunk(tokens, self.maxtokens, self.tokenizer.punctuation())):
            params = {self.input: [[0, *x, 0]], "style": speaker[len(x)], "speed": np.ones(1, dtype=np.float32) * speed}

            output = self.model.run(None, params)
            results.append(Signal.trim(output[0], rate, trailing=False) if i > 0 else output[0])

        return (np.concatenate(results), rate)


class SpeechT5(SpeechPipeline):
    """
    Text to Speech pipeline with a SpeechT5 ONNX model.
    """

    def __init__(self, path, maxtokens, providers):
        """
        Creates a new SpeechT5 pipeline.

        Args:
            path: model path
            maxtokens: maximum number of tokens model can process
            providers: list of supported ONNX providers
        """

        self.encoder = ort.InferenceSession(
            cached_file(path_or_repo_id=path, filename="encoder_model.onnx"), providers=providers
        )
        self.decoder = ort.InferenceSession(
            cached_file(path_or_repo_id=path, filename="decoder_model_merged.onnx"), providers=providers
        )
        self.vocoder = ort.InferenceSession(
            cached_file(path_or_repo_id=path, filename="decoder_postnet_and_vocoder.onnx"), providers=providers
        )

        self.processor = SpeechT5Processor.from_pretrained(path)
        self.defaultspeaker = np.load(cached_file(path_or_repo_id=path, filename="speaker.npy"), allow_pickle=False)

        self.maxtokens = maxtokens

        # pylint: disable=E1101
        self.punctids = [v for k, v in self.processor.tokenizer.get_vocab().items() if k in ".,!?;"]

    def __call__(self, text, speaker):
        """
        Executes a model run. This method will build batches of tokens when len(tokens) > maxtokens.

        Args:
            text: text to tokenize and pass to model
            speaker: speaker embeddings

        Returns:
            (audio, sample rate)
        """

        logger.debug("%s", text)

        rate = 16000

        inputs = self.processor(text=text, return_tensors="np", normalize=True)

        results = []
        for i, x in enumerate(self.chunk(inputs["input_ids"][0], self.maxtokens, self.punctids)):
            chunk = self.process(np.array([x], dtype=np.int64), speaker)
            results.append(Signal.trim(chunk, rate, trailing=False) if i > 0 else chunk)

        return (np.concatenate(results), rate)

    def process(self, inputs, speaker):
        """
        Runs model inference.

        Args:
            inputs: input token ids
            speaker: speaker embeddings

        Returns:
            waveform as NumPy array
        """

        outputs = self.encoder.run(None, {"input_ids": inputs})
        outputs = {key.name: outputs[x] for x, key in enumerate(self.encoder.get_outputs())}

        hiddenstate, attentionmask = outputs["encoder_outputs"], outputs["encoder_attention_mask"]
        minlenratio, maxlenratio = 0.0, 20.0
        reduction, threshold, melbins = 2, 0.5, 80

        maxlen = int(hiddenstate.shape[1] * maxlenratio / reduction)
        minlen = int(hiddenstate.shape[1] * minlenratio / reduction)

        spectrogram, index, crossattention, branch, outputs = [], 0, None, False, {}
        while True:
            index += 1

            inputs = {
                "use_cache_branch": np.array([branch]),
                "encoder_attention_mask": attentionmask,
                "speaker_embeddings": speaker
                if speaker is not None and isinstance(speaker, np.ndarray)
                else self.defaultspeaker,
            }

            if index == 1:
                inputs = self.placeholders(inputs)
                inputs["output_sequence"] = np.zeros((1, 1, melbins)).astype(np.float32)
                inputs["encoder_hidden_states"] = hiddenstate
                branch = True
            else:
                inputs = self.inputs(inputs, outputs, crossattention)
                inputs["output_sequence"] = outputs["output_sequence_out"]
                inputs["encoder_hidden_states"] = np.zeros((1, 0, 768)).astype(np.float32)

            outputs = self.decoder.run(None, inputs)
            outputs = {key.name: outputs[x] for x, key in enumerate(self.decoder.get_outputs())}

            if index == 1:
                crossattention = {key: val for key, val in outputs.items() if ("encoder" in key and "present" in key)}

            prob = outputs["prob"]
            spectrum = outputs["spectrum"]
            spectrogram.append(spectrum)

            if index >= minlen and (int(sum(prob >= threshold)) > 0 or index >= maxlen):
                spectrogram = np.concatenate(spectrogram)
                return self.vocoder.run(None, {"spectrogram": spectrogram})[0]

    def placeholders(self, inputs):
        """
        Creates decoder model inputs for initial inference pass.

        Args:
            inputs: current decoder inputs

        Returns:
            updated decoder inputs
        """

        length = inputs["encoder_attention_mask"].shape[1]

        for x in range(6):
            inputs[f"past_key_values.{x}.encoder.key"] = np.zeros((1, 12, length, 64)).astype(np.float32)
            inputs[f"past_key_values.{x}.encoder.value"] = np.zeros((1, 12, length, 64)).astype(np.float32)
            inputs[f"past_key_values.{x}.decoder.key"] = np.zeros((1, 12, 1, 64)).astype(np.float32)
            inputs[f"past_key_values.{x}.decoder.value"] = np.zeros((1, 12, 1, 64)).astype(np.float32)

        return inputs

    def inputs(self, inputs, previous, crossattention):
        """
        Creates decoder model inputs for follow-on inference passes.

        Args:
            inputs: current decoder inputs
            previous: previous decoder outputs
            crossattention: crossattention parameters

        Returns:
            updated decoder inputs
        """

        for x in range(6):
            inputs[f"past_key_values.{x}.encoder.key"] = crossattention[f"present.{x}.encoder.key"]
            inputs[f"past_key_values.{x}.encoder.value"] = crossattention[f"present.{x}.encoder.value"]
            inputs[f"past_key_values.{x}.decoder.key"] = previous[f"present.{x}.decoder.key"]
            inputs[f"past_key_values.{x}.decoder.value"] = previous[f"present.{x}.decoder.value"]

        return inputs
