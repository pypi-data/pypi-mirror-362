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

import functools

from ...utilities import Resolver


class TaskFactory:
    """
    Task factory. Creates new Task instances.
    """

    @staticmethod
    def get(task):
        """
        Gets a new instance of task class.

        Args:
            task: Task instance class

        Returns:
            Task class
        """

        if "." not in task:
            task = ".".join(__name__.split(".")[:-1]) + "." + task.capitalize() + "Task"

        return Resolver()(task)

    @staticmethod
    def create(config, task):
        """
        Creates a new Task instance.

        Args:
            config: Task configuration
            task: Task instance class

        Returns:
            Task
        """

        if "args" in config:
            args = config.pop("args")
            action = config["action"]
            if action:
                if isinstance(action, list):
                    config["action"] = [Partial.create(a, args[i]) for i, a in enumerate(action)]
                else:
                    config["action"] = lambda x: action(x, **args) if isinstance(args, dict) else action(x, *args)

        return TaskFactory.get(task)(**config)


class Partial(functools.partial):
    """
    Modifies functools.partial to prepend arguments vs append.
    """

    @staticmethod
    def create(action, args):
        """
        Creates a new Partial function.

        Args:
            action: action to execute
            args: arguments

        Returns:
            Partial
        """

        return Partial(action, **args) if isinstance(args, dict) else Partial(action, *args) if args else Partial(action)

    def __call__(self, *args, **kwargs):
        kw = self.keywords.copy()
        kw.update(kwargs)

        return self.func(*(args + self.args), **kw)
