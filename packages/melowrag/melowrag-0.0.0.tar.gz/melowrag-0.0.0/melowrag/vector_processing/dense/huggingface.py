from ...modeling import Models, PoolingFactory
from ..base import Vectors


class HFVectors(Vectors):
    """
    Builds vectors using the Hugging Face transformers library.
    """

    @staticmethod
    def ismethod(method):
        """
        Checks if this method uses local transformers-based models.

        Args:
            method: input method

        Returns:
            True if this is a local transformers-based model, False otherwise
        """

        return method in ("transformers", "pooling", "clspooling", "meanpooling")

    def loadmodel(self, path):
        return PoolingFactory.create(
            {
                "method": self.config.get("method"),
                "path": path,
                "device": Models.deviceid(self.config.get("gpu", True)),
                "tokenizer": self.config.get("tokenizer"),
                "maxlength": self.config.get("maxlength"),
                "modelargs": self.config.get("vectors", {}),
            }
        )

    def encode(self, data, category=None):
        return self.model.encode(data, batch=self.encodebatch)
