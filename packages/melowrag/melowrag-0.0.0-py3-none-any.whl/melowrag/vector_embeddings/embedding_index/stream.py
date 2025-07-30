from .autoid import AutoId
from .transform import Action


class Stream:
    """
    Yields input document as standard (id, data, tags) tuples.
    """

    def __init__(self, embeddings, action=None):
        """
        Create a new stream.

        Args:
            embeddings: embeddings instance
            action: optional index action
        """

        self.embeddings = embeddings
        self.action = action

        self.config = embeddings.config

        self.offset = self.config.get("offset", 0) if action == Action.UPSERT else 0
        autoid = self.config.get("autoid", self.offset)

        autoid = 0 if isinstance(autoid, int) and action != Action.UPSERT else autoid
        self.autoid = AutoId(autoid)

    def __call__(self, documents):
        """
        Yield (id, data, tags) tuples from a stream of documents.

        Args:
            documents: input documents
        """

        for document in documents:
            if isinstance(document, dict):
                document = document.get("id"), document, document.get("tags")
            elif isinstance(document, tuple):
                document = document if len(document) >= 3 else (document[0], document[1], None)
            else:
                document = None, document, None

            if self.action and document[0] is None:
                document = (self.autoid(document[1]), document[1], document[2])

            yield document

        current = self.autoid.current()
        if self.action and current:
            self.config["autoid"] = current
