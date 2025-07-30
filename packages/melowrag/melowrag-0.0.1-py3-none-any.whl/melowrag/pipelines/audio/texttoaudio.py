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

from ..hfpipeline import HFPipeline
from .signal import SCIPY, Signal


class TextToAudio(HFPipeline):
    """
    Generates audio from text.
    """

    def __init__(self, path=None, quantize=False, gpu=True, model=None, rate=None, **kwargs):
        if not SCIPY:
            raise ImportError('TextToAudio pipeline is not available - install "pipeline" extra to enable.')

        super().__init__("text-to-audio", path, quantize, gpu, model, **kwargs)

        self.rate = rate

    def __call__(self, text, maxlength=512):
        """
        Generates audio from text.

        This method supports text as a string or a list. If the input is a string,
        the return type is a single audio output. If text is a list, the return type is a list.

        Args:
            text: text|list
            maxlength: maximum audio length to generate

        Returns:
            list of (audio, sample rate)
        """

        texts = [text] if isinstance(text, str) else text

        results = [self.convert(x) for x in self.pipeline(texts, forward_params={"max_new_tokens": maxlength})]

        return results[0] if isinstance(text, str) else results

    def convert(self, result):
        """
        Converts audio result to target sample rate for this pipeline, if set.

        Args:
            result: dict with audio samples and sample rate

        Returns:
            (audio, sample rate)
        """

        audio, rate = result["audio"].squeeze(), result["sampling_rate"]
        return (Signal.resample(audio, rate, self.rate), self.rate) if self.rate else (audio, rate)
