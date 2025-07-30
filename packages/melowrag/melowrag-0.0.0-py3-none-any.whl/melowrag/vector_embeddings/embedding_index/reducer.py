from zipfile import BadZipFile

try:
    import skops.io as sio  # type:ignore
    from sklearn.decomposition import TruncatedSVD

    REDUCER = True
except ImportError:
    REDUCER = False

from ...serialization import SerializeFactory


class Reducer:
    """
    LSA dimensionality reduction model
    """

    def __init__(self, embeddings=None, components=None):
        """
        Creates a dimensionality reduction model.

        Args:
            embeddings: input embeddings matrix
            components: number of model components
        """

        if not REDUCER:
            raise ImportError('Dimensionality reduction is not available - install "vectors" extra to enable')

        self.model = self.build(embeddings, components) if embeddings is not None and components else None

    def __call__(self, embeddings):
        """
        Applies a dimensionality reduction model to embeddings, removed the top n principal components. Operation applied
        directly on array.

        Args:
            embeddings: input embeddings matrix
        """

        pc = self.model.components_
        factor = embeddings.dot(pc.transpose())

        if pc.shape[0] == 1:
            embeddings -= factor * pc
        elif len(embeddings.shape) > 1:
            for x in range(embeddings.shape[0]):
                embeddings[x] -= factor[x].dot(pc)
        else:
            embeddings -= factor.dot(pc)

    def build(self, embeddings, components):
        """
        Builds a LSA model. This model is used to remove the principal component within embeddings. This helps to
        smooth out noisy embeddings (common words with less value).

        Args:
            embeddings: input embeddings matrix
            components: number of model components

        Returns:
            LSA model
        """

        model = TruncatedSVD(n_components=components, random_state=0)
        model.fit(embeddings)

        return model

    def load(self, path):
        """
        Loads a Reducer object from path.

        Args:
            path: directory path to load model
        """

        try:
            self.model = sio.load(path)
        except (BadZipFile, KeyError):
            self.model = SerializeFactory.create("pickle").load(path)

    def save(self, path):
        """
        Saves a Reducer object to path.

        Args:
            path: directory path to save model
        """

        sio.dump(self.model, path)
