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
