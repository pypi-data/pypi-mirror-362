import os
import tempfile

from ...serialization import SerializeFactory


class Documents:
    """
    Streams documents to temporary storage. Allows queuing large volumes of content for later indexing.
    """

    def __init__(self):
        """
        Creates a new documents stream.
        """

        self.documents = None
        self.batch = 0
        self.size = 0

        self.serializer = SerializeFactory.create("pickle", allowpickle=True)

    def __len__(self):
        """
        Returns total number of queued documents.
        """

        return self.size

    def __iter__(self):
        """
        Streams all queued documents.
        """

        self.documents.close()

        with open(self.documents.name, "rb") as queue:
            for _ in range(self.batch):
                documents = self.serializer.loadstream(queue)

                yield from documents

    def add(self, documents):
        """
        Adds a batch of documents for indexing.

        Args:
            documents: list of (id, data, tag) tuples

        Returns:
            documents
        """

        # pylint: disable=R1732
        if not self.documents:
            self.documents = tempfile.NamedTemporaryFile(mode="wb", suffix=".docs", delete=False)

        self.serializer.savestream(documents, self.documents)
        self.batch += 1
        self.size += len(documents)

        return documents

    def close(self):
        """
        Closes and resets this instance. New sets of documents can be added with additional calls to add.
        """

        os.remove(self.documents.name)

        self.documents = None
        self.batch = 0
        self.size = 0
