import os
import tempfile
from urllib.parse import urlparse
from urllib.request import urlretrieve

from .url import UrlTask


class RetrieveTask(UrlTask):
    """
    Task that retrieves urls (local or remote) to a local directory.
    """

    def register(self, directory=None, flatten=True):
        """
        Adds retrieve parameters to task.

        Args:
            directory: local directory used to store retrieved files
            flatten: flatten input directory structure, defaults to True
        """

        # pylint: disable=W0201
        if not directory:
            # pylint: disable=R1732
            self.tempdir = tempfile.TemporaryDirectory()
            directory = self.tempdir.name

        os.makedirs(directory, exist_ok=True)

        self.directory = directory
        self.flatten = flatten

    def prepare(self, element):
        path = urlparse(element).path

        if self.flatten:
            path = os.path.join(self.directory, os.path.basename(path))
        else:
            path = os.path.join(self.directory, os.path.normpath(path.lstrip("/")))
            directory = os.path.dirname(path)

            os.makedirs(directory, exist_ok=True)

        urlretrieve(element, path)

        return path
