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

from ..base import Pipeline
from .signal import SCIPY, Signal


class AudioMixer(Pipeline):
    """
    Mixes multiple audio streams into a single stream.
    """

    def __init__(self, rate=None):
        """
        Creates an AudioMixer pipeline.

        Args:
            rate: optional target sample rate, otherwise uses input target rate with each audio segment
        """

        if not SCIPY:
            raise ImportError('AudioMixer pipeline is not available - install "pipeline" extra to enable.')

        self.rate = rate

    def __call__(self, segment, scale1=1, scale2=1):
        """
        Mixes multiple audio streams into a single stream.

        Args:
            segment: ((audio1, sample rate), (audio2, sample rate))|list
            scale1: optional scaling factor for segment1
            scale2: optional scaling factor for segment2

        Returns:
            list of (audio, sample rate)
        """

        segments = [segment] if isinstance(segment, tuple) else segment

        results = []
        for segment1, segment2 in segments:
            audio1, rate1 = segment1
            audio2, rate2 = segment2

            target = self.rate if self.rate else rate1
            audio1 = Signal.resample(audio1, rate1, target)
            audio2 = Signal.resample(audio2, rate2, target)

            results.append((Signal.mix(audio1, audio2, scale1, scale2), target))

        return results[0] if isinstance(segment, tuple) else results
