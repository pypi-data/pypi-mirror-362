from .base import Pooling


class ClsPooling(Pooling):
    """
    Builds CLS pooled vectors using outputs from a transformers model.
    """

    def forward(self, **inputs):
        """
        Runs CLS pooling on token embeddings.

        Args:
            inputs: model inputs

        Returns:
            CLS pooled embeddings using output token embeddings (i.e. last hidden state)
        """

        tokens = super().forward(**inputs)

        return tokens[:, 0]
