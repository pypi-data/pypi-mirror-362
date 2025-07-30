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

from .base import Task


class StreamTask(Task):
    """
    Task that calls a task action and yields results.
    """

    def register(self, batch=False):
        """
        Adds stream parameters to task.

        Args:
            batch: all elements are passed to a single action call if True, otherwise
                        an action call is executed per element, defaults to False
        """

        # pylint: disable=W0201
        self.batch = batch

    def __call__(self, elements, executor=None):
        for action in self.action:
            if self.batch:
                yield from action(elements)
            else:
                for x in elements:
                    yield from action(x)
