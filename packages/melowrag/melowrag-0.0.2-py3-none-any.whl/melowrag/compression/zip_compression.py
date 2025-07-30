# Copyright 2025 The MelowRAG Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
