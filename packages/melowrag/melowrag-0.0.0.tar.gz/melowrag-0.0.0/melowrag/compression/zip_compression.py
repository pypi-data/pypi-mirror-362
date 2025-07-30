import os
from zipfile import ZIP_DEFLATED, ZipFile

from .compress import Compress


class Zip(Compress):
    """
    Zip compression
    """

    def pack(self, path, output):
        with ZipFile(output, "w", ZIP_DEFLATED) as zfile:
            for root, _, files in sorted(os.walk(path)):
                for f in files:
                    name = os.path.join(os.path.relpath(root, path), f)

                    zfile.write(os.path.join(root, f), arcname=name)

    def unpack(self, path, output):
        with ZipFile(path, "r") as zfile:
            for fullpath in zfile.namelist():
                fullpath = os.path.join(path, fullpath)
                if os.path.dirname(fullpath) and not self.validate(path, fullpath):
                    raise OSError(f"Invalid zip entry: {fullpath}")

            zfile.extractall(output)
