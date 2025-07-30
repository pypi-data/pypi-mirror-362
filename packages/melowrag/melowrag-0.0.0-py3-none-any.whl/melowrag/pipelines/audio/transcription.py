"""
Transcription module
"""

import numpy as np

try:
    import soundfile as sf  # type:ignore

    from .signal import SCIPY, Signal  # type:ignore

    TRANSCRIPTION = SCIPY
except (ImportError, OSError):
    TRANSCRIPTION = False

from ..hfpipeline import HFPipeline


class Transcription(HFPipeline):
    """
    Transcribes audio files or data to text.
    """

    def __init__(self, path=None, quantize=False, gpu=True, model=None, **kwargs):
        if not TRANSCRIPTION:
            raise ImportError(
                "Transcription pipeline is not available "
                'install "pipeline" extra to enable. Also check that libsndfile is available.'
            )

        super().__init__("automatic-speech-recognition", path, quantize, gpu, model, **kwargs)

    def __call__(self, audio, rate=None, chunk=10, join=True, **kwargs):
        """
        Transcribes audio files or data to text.

        This method supports a single audio element or a list of audio. If the input is audio, the return
        type is a string. If text is a list, a list of strings is returned

        Args:
            audio: audio|list
            rate: sample rate, only required with raw audio data
            chunk: process audio in chunk second sized segments
            join: if True (default), combine each chunk back together into a single text output.
                  When False, chunks are returned as a list of dicts, each having raw associated audio and
                  sample rate in addition to text
            kwargs: generate keyword arguments

        Returns:
            list of transcribed text
        """

        values = [audio] if self.isaudio(audio) else audio

        speech = self.read(values, rate)

        results = (
            self.batchprocess(speech, chunk, **kwargs) if chunk and not join else self.process(speech, chunk, **kwargs)
        )

        return results[0] if self.isaudio(audio) else results

    def isaudio(self, audio):
        """
        Checks if input is a single audio element.

        Args:
            audio: audio|list

        Returns:
            True if input is an audio element, False otherwise
        """

        return isinstance(audio, str | tuple | np.ndarray) or hasattr(audio, "read")

    def read(self, audio, rate):
        """
        Read audio to raw waveforms and sample rates.

        Args:
            audio: audio|list
            rate: optional sample rate

        Returns:
            list of (audio data, sample rate)
        """

        speech = []
        for x in audio:
            if isinstance(x, str) or hasattr(x, "read"):
                raw, samplerate = sf.read(x)
            elif isinstance(x, tuple):
                raw, samplerate = x
            else:
                raw, samplerate = x, rate

            speech.append((raw, samplerate))

        return speech

    def process(self, speech, chunk, **kwargs):
        """
        Standard processing loop. Runs a single pipeline call for all speech inputs along
        with the chunk size. Returns text for each input.

        Args:
            speech: list of (audio data, sample rate)
            chunk: split audio into chunk seconds sized segments for processing
            kwargs: generate keyword arguments

        Returns:
            list of transcribed text
        """

        results = []
        for result in self.pipeline(
            [self.convert(*x) for x in speech], chunk_length_s=chunk, ignore_warning=True, generate_kwargs=kwargs
        ):
            results.append(self.clean(result["text"]))

        return results

    def batchprocess(self, speech, chunk, **kwargs):
        """
        Batch processing loop. Runs a pipeline call per speech input. Each speech input is split
        into chunk duration segments. Each segment is individually transcribed and returned along with
        the raw wav snippets.

        Args:
            speech: list of (audio data, sample rate)
            chunk: split audio into chunk seconds sized segments for processing
            kwargs: generate keyword arguments

        Returns:
            list of lists of dicts - each dict has text, raw wav data for text and sample rate
        """

        results = []

        for raw, rate in speech:
            segments = self.segments(raw, rate, chunk)

            sresults = []
            for x, result in enumerate(self.pipeline([self.convert(*x) for x in segments], generate_kwargs=kwargs)):
                sresults.append({"text": self.clean(result["text"]), "raw": segments[x][0], "rate": segments[x][1]})

            results.append(sresults)

        return results

    def segments(self, raw, rate, chunk):
        """
        Builds chunk duration batches.

        Args:
            raw: raw audio data
            rate: sample rate
            chunk: chunk duration size
        """

        segments = []

        for segment in self.batch(raw, rate * chunk):
            segments.append((segment, rate))

        return segments

    def convert(self, raw, rate):
        """
        Converts input audio to mono with a sample rate equal to the pipeline model's
        sample rate.

        Args:
            raw: raw audio data
            rate: target sample rate

        Returns:
            audio data ready for pipeline model
        """

        raw = Signal.mono(raw)

        target = self.pipeline.feature_extractor.sampling_rate
        return {"raw": Signal.resample(raw, rate, target), "sampling_rate": target}

    def clean(self, text):
        """
        Applies text normalization rules.

        Args:
            text: input text

        Returns:
            clean text
        """

        text = text.strip()

        return text.capitalize() if text.isupper() else text
