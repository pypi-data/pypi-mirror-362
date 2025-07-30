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

from queue import Queue
from threading import Thread

try:
    import sounddevice as sd  # type:ignore

    from .signal import SCIPY, Signal

    AUDIOSTREAM = SCIPY
except (ImportError, OSError):
    AUDIOSTREAM = False

from ..base import Pipeline


class AudioStream(Pipeline):
    """
    Threaded pipeline that streams audio segments to an output audio device. This pipeline is designed
    to run on local machines given that it requires access to write to an output device.
    """

    COMPLETE = (1, None)

    def __init__(self, rate=None):
        """
        Creates an AudioStream pipeline.

        Args:
            rate: optional target sample rate, otherwise uses input target rate with each audio segment
        """

        if not AUDIOSTREAM:
            raise ImportError(
                'AudioStream pipeline is not available - install "pipeline" extra to enable. '
                "Also check that the portaudio system library is available."
            )

        self.rate = rate

        self.queue = Queue()
        self.thread = Thread(target=self.play)
        self.thread.start()

    def __call__(self, segment):
        """
        Queues audio segments for the audio player.

        Args:
            segment: (audio, sample rate)|list

        Returns:
            segment
        """

        segments = [segment] if isinstance(segment, tuple) else segment

        for x in segments:
            self.queue.put(x)

        return segments[0] if isinstance(segment, tuple) else segments

    def wait(self):
        """
        Waits for all input audio segments to be played.
        """

        self.thread.join()

    def play(self):
        """
        Reads audio segments from queue. This method runs in a separate non-blocking thread.
        """

        audio, rate = self.queue.get()
        while not isinstance(audio, int) or (audio, rate) != AudioStream.COMPLETE:
            audio, rate = (Signal.resample(audio, rate, self.rate), self.rate) if self.rate else (audio, rate)

            sd.play(audio, rate, blocking=True)

            audio, rate = self.queue.get()
