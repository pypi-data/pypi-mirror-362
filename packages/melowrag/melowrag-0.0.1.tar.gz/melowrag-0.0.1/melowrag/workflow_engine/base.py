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

import logging
import time
import traceback
from datetime import datetime

try:
    from croniter import croniter  # type:ignore

    CRONITER = True
except ImportError:
    CRONITER = False

from .execute import Execute

logger = logging.getLogger(__name__)


class Workflow:
    """
    Base class for all workflows.
    """

    def __init__(self, tasks, batch=100, workers=None, name=None, stream=None):
        """
        Creates a new workflow. Workflows are lists of tasks to execute.

        Args:
            tasks: list of workflow tasks
            batch: how many items to process at a time, defaults to 100
            workers: number of concurrent workers
            name: workflow name
            stream: workflow stream processor
        """

        self.tasks = tasks
        self.batch = batch
        self.workers = workers
        self.name = name
        self.stream = stream

        self.workers = max(len(task.action) for task in self.tasks) if not self.workers else self.workers

    def __call__(self, elements):
        """
        Executes a workflow for input elements. This method returns a generator that yields transformed
        data elements.

        Args:
            elements: iterable data elements

        Returns:
            generator that yields transformed data elements
        """

        with Execute(self.workers) as executor:
            self.initialize()

            elements = self.stream(elements) if self.stream else elements

            for batch in self.chunk(elements):
                yield from self.process(batch, executor)

            self.finalize()

    def schedule(self, cron, elements, iterations=None):
        """
        Schedules a workflow using a cron expression and elements.

        Args:
            cron: cron expression
            elements: iterable data elements passed to workflow each call
            iterations: number of times to run workflow, defaults to run indefinitely
        """

        if not CRONITER:
            raise ImportError('Workflow scheduling is not available - install "workflow" extra to enable')

        logger.info("'%s' scheduler started with schedule %s", self.name, cron)

        maxiterations = iterations
        while iterations is None or iterations > 0:
            schedule = croniter(cron, datetime.now().astimezone()).get_next(datetime)
            logger.info("'%s' next run scheduled for %s", self.name, schedule.isoformat())
            time.sleep(schedule.timestamp() - time.time())

            # pylint: disable=W0703
            try:
                for _ in self(elements):
                    pass
            except Exception:
                logger.error(traceback.format_exc())

            if iterations is not None:
                iterations -= 1

        logger.info("'%s' max iterations (%d) reached", self.name, maxiterations)

    def initialize(self):
        """
        Runs task initializer methods (if any) before processing data.
        """

        for task in self.tasks:
            if task.initialize:
                task.initialize()

    def chunk(self, elements):
        """
        Splits elements into batches. This method efficiently processes both fixed size inputs and
        dynamically generated inputs.

        Args:
            elements: iterable data elements

        Returns:
            evenly sized batches with the last batch having the remaining elements
        """

        if hasattr(elements, "__len__") and hasattr(elements, "__getitem__"):
            for x in range(0, len(elements), self.batch):
                yield elements[x : x + self.batch]

        else:
            batch = []
            for x in elements:
                batch.append(x)

                if len(batch) == self.batch:
                    yield batch
                    batch = []

            if batch:
                yield batch

    def process(self, elements, executor):
        """
        Processes a batch of data elements.

        Args:
            elements: iterable data elements
            executor: execute instance, enables concurrent task actions

        Returns:
            transformed data elements
        """

        for x, task in enumerate(self.tasks):
            logger.debug("Running Task #%d", x)
            elements = task(elements, executor)

        yield from elements

    def finalize(self):
        """
        Runs task finalizer methods (if any) after all data processed.
        """

        for task in self.tasks:
            if task.finalize:
                task.finalize()
