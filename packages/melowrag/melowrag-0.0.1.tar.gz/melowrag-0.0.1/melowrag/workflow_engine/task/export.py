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

import datetime
import os

try:
    import pandas as pd

    PANDAS = True
except ImportError:
    PANDAS = False

from .base import Task


class ExportTask(Task):
    """
    Task that exports task elements using Pandas.
    """

    def register(self, output=None, timestamp=None):
        """
        Add export parameters to task. Checks if required dependencies are installed.

        Args:
            output: output file path
            timestamp: true if output file should be timestamped
        """

        if not PANDAS:
            raise ImportError('ExportTask is not available - install "workflow" extra to enable')

        # pylint: disable=W0201
        self.output = output
        self.timestamp = timestamp

    def __call__(self, elements, executor=None):
        outputs = super().__call__(elements, executor)

        output = self.output
        parts = list(os.path.splitext(output))
        extension = parts[-1].lower()

        if self.timestamp:
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            parts[-1] = timestamp + parts[-1]

            output = ".".join(parts)

        if extension == ".xlsx":
            pd.DataFrame(outputs).to_excel(output, index=False)
        else:
            pd.DataFrame(outputs).to_csv(output, index=False)

        return outputs
