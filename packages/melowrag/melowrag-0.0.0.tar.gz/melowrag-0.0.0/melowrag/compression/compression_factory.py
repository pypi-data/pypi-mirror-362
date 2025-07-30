from .base_compression import Archive


class ArchiveFactory:
    """
    Methods to create Archive instances.
    """

    @staticmethod
    def create(directory=None):
        """
        Create a new Archive instance.

        Args:
            directory: optional default working directory, otherwise uses a temporary directory

        Returns:
            Archive
        """

        return Archive(directory)

    def __repr__(self):
        """
        Returns a detailed string representation of the ArchiveFactory class.
        """
        return f"{self.__class__.__name__}(factory for Archive instances)"

    def __str__(self):
        """
        Returns a user-friendly string representation of the ArchiveFactory class.
        """
        return "ArchiveFactory: use .create(directory) to get an Archive instance"
