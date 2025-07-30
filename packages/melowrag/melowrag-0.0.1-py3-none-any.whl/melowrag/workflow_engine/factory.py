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

from .base import Workflow
from .task import TaskFactory


class WorkflowFactory:
    """
    Workflow factory. Creates new Workflow instances.
    """

    @staticmethod
    def create(config, name):
        """
        Creates a new Workflow instance.

        Args:
            config: Workflow configuration
            name: Workflow name

        Returns:
            Workflow
        """

        tasks = []
        for tconfig in config["tasks"]:
            task = tconfig.pop("task") if "task" in tconfig else ""
            tasks.append(TaskFactory.create(tconfig, task))

        config["tasks"] = tasks

        if "stream" in config:
            sconfig = config["stream"]
            task = sconfig.pop("task") if "task" in sconfig else "stream"

            config["stream"] = TaskFactory.create(sconfig, task)

        return Workflow(**config, name=name)
