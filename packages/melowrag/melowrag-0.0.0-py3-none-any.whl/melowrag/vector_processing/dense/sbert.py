try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS = True
except ImportError:
    SENTENCE_TRANSFORMERS = False

from ...modeling import Models
from ..base import Vectors


class STVectors(Vectors):
    """
    Builds vectors using sentence-transformers (aka SBERT).
    """

    def __init__(self, config, scoring, models):
        if not SENTENCE_TRANSFORMERS:
            raise ImportError('sentence-transformers is not available - install "vectors" extra to enable')

        self.pool = None

        super().__init__(config, scoring, models)

    def loadmodel(self, path):
        gpu, pool = self.config.get("gpu", True), False

        if isinstance(gpu, str) and gpu == "all":
            devices = Models.acceleratorcount()

            gpu, pool = devices <= 1, devices > 1

        deviceid = Models.deviceid(gpu)

        modelargs = self.config.get("vectors", {})

        model = self.loadencoder(path, device=Models.device(deviceid), **modelargs)

        if pool:
            self.pool = model.start_multi_process_pool()

        return model

    def encode(self, data, category=None):
        encode = (
            self.model.encode_query
            if category == "query"
            else self.model.encode_document
            if category == "data"
            else self.model.encode
        )

        encodeargs = self.config.get("encodeargs", {})

        return encode(data, pool=self.pool, batch_size=self.encodebatch, **encodeargs)

    def close(self):
        if self.pool:
            self.model.stop_multi_process_pool(self.pool)
            self.pool = None

        super().close()

    def loadencoder(self, path, device, **kwargs):
        """
        Loads the embeddings encoder model from path.

        Args:
            path: model path
            device: tensor device
            kwargs: additional keyword args

        Returns:
            embeddings encoder
        """

        return SentenceTransformer(path, device=device, **kwargs)
