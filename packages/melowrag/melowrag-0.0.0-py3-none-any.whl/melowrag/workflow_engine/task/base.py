import logging
import re
import types

import numpy as np
import torch

logger = logging.getLogger(__name__)


class Task:
    """
    Base class for all workflow tasks.
    """

    def __init__(
        self,
        action=None,
        select=None,
        unpack=True,
        column=None,
        merge="hstack",
        initialize=None,
        finalize=None,
        concurrency=None,
        onetomany=True,
        **kwargs,
    ):
        """
        Creates a new task. A task defines two methods, type of data it accepts and the action to execute
        for each data element. Action is a callable function or list of callable functions.

        Args:
            action: action(s) to execute on each data element
            select: filter(s) used to select data to process
            unpack: if data elements should be unpacked or unwrapped from (id, data, tag) tuples
            column: column index to select if element is a tuple, defaults to all
            merge: merge mode for joining multi-action outputs, defaults to hstack
            initialize: action to execute before processing
            finalize: action to execute after processing
            concurrency: sets concurrency method when execute instance available
                         valid values: "thread" for thread-based concurrency, "process" for process-based concurrency
            onetomany: if one-to-many data transformations should be enabled, defaults to True
            kwargs: additional keyword arguments
        """

        if not action:
            action = []
        elif not isinstance(action, list):
            action = [action]

        self.action = action
        self.select = select
        self.unpack = unpack
        self.column = column
        self.merge = merge
        self.initialize = initialize
        self.finalize = finalize
        self.concurrency = concurrency
        self.onetomany = onetomany

        if hasattr(self, "register"):
            self.register(**kwargs)
        elif kwargs:
            kwargs = ", ".join(f"'{kw}'" for kw in kwargs)
            raise TypeError(f"__init__() got unexpected keyword arguments: {kwargs}")

    def __call__(self, elements, executor=None):
        """
        Executes action for a list of data elements.

        Args:
            elements: iterable data elements
            executor: execute instance, enables concurrent task actions

        Returns:
            transformed data elements
        """

        if isinstance(elements, list):
            return self.filteredrun(elements, executor)

        return self.run(elements, executor)

    def filteredrun(self, elements, executor):
        """
        Executes a filtered run, which will tag all inputs with a process id, filter elements down to elements the
        task can handle and execute on that subset. Items not selected for processing will be returned unmodified.

        Args:
            elements: iterable data elements
            executor: execute instance, enables concurrent task actions

        Returns:
            transformed data elements
        """

        indexed = list(enumerate(elements))

        data = [(x, self.upack(element)) for x, element in indexed if self.accept(self.upack(element, True))]

        ids = [x for x, _ in data]

        results = self.execute([self.prepare(element) for _, element in data], executor)

        if self.merge:
            elements = self.filteredpack(results, indexed, ids)
        else:
            elements = [self.filteredpack(r, indexed, ids) for r in results]

        return elements

    def filteredpack(self, results, indexed, ids):
        """
        Processes and packs results back into original input elements.

        Args:
            results: task results
            indexed: original elements indexed by process id
            ids: process ids accepted by this task

        Returns:
            packed elements
        """

        elements = []
        for x, element in indexed:
            if x in ids:
                result = results[ids.index(x)]

                if isinstance(result, OneToMany):
                    elements.extend([self.pack(element, r) for r in result])
                else:
                    elements.append(self.pack(element, result))
            else:
                elements.append(element)

        return elements

    def run(self, elements, executor):
        """
        Executes a task run for elements. A standard run processes all elements.

        Args:
            elements: iterable data elements
            executor: execute instance, enables concurrent task actions

        Returns:
            transformed data elements
        """

        results = self.execute(elements, executor)

        if isinstance(results, list):
            elements = []
            for result in results:
                if isinstance(result, OneToMany):
                    elements.extend(result)
                else:
                    elements.append(result)

            return elements

        return results

    def accept(self, element):
        """
        Determines if this task can handle the input data format.

        Args:
            element: input data element

        Returns:
            True if this task can process this data element, False otherwise
        """

        return (
            (isinstance(element, str) and re.search(self.select, element.lower()))
            if element is not None and self.select
            else True
        )

    def upack(self, element, force=False):
        """
        Unpacks data for processing.

        Args:
            element: input data element
            force: if True, data is unpacked even if task has unpack set to False

        Returns:
            data
        """

        if (self.unpack or force) and isinstance(element, tuple) and len(element) > 1:
            return element[1]

        return element

    def pack(self, element, data):
        """
        Packs data after processing.

        Args:
            element: transformed data element
            data: item to pack element into

        Returns:
            packed data
        """

        if self.unpack and isinstance(element, tuple) and len(element) > 1:
            if isinstance(data, tuple) and (len(self.action) <= 1 or self.merge != "hstack"):
                return data

            element = list(element)
            element[1] = data
            return tuple(element)

        return data

    def prepare(self, element):
        """
        Method that allows downstream tasks to prepare data element for processing.

        Args:
            element: input data element

        Returns:
            data element ready for processing
        """

        return element

    def execute(self, elements, executor):
        """
        Executes action(s) on elements.

        Args:
            elements: list of data elements
            executor: execute instance, enables concurrent task actions

        Returns:
            transformed data elements
        """

        if self.action:
            outputs = []
            for x, action in enumerate(self.action):
                index = self.column[x] if isinstance(self.column, dict) else self.column
                inputs = [self.extract(e, index) for e in elements] if index is not None else elements

                outputs.append((action, inputs) if executor else self.process(action, inputs))

            if executor:
                outputs = executor.run(self.concurrency, self.process, outputs)

            return self.postprocess(outputs)

        return elements

    def extract(self, element, index):
        """
        Extracts a column from element by index if the element is a tuple.

        Args:
            element: input element
            index: column index

        Returns:
            extracted column
        """

        if isinstance(element, tuple):
            if not self.unpack and len(element) == 3 and isinstance(element[1], tuple):
                return (element[0], element[1][index], element[2])

            return element[index]

        return element

    def process(self, action, inputs):
        """
        Executes action using inputs as arguments.

        Args:
            action: callable object
            inputs: action inputs

        Returns:
            action outputs
        """

        logger.debug("Inputs: %s", inputs)

        outputs = action(inputs)

        if isinstance(outputs, types.GeneratorType):
            outputs = list(outputs)

        logger.debug("Outputs: %s", outputs)

        return outputs

    def postprocess(self, outputs):
        """
        Runs post process routines after a task action.

        Args:
            outputs: task outputs

        Returns:
            postprocessed outputs
        """

        if len(self.action) == 1:
            return self.single(outputs[0])

        if not self.merge:
            return outputs

        if self.merge == "vstack":
            return self.vstack(outputs)
        if self.merge == "concat":
            return self.concat(outputs)

        return self.hstack(outputs)

    def single(self, outputs):
        """
        Post processes and returns single action outputs.

        Args:
            outputs: outputs from a single task

        Returns:
            post processed outputs
        """

        if self.onetomany and isinstance(outputs, list):
            outputs = [OneToMany(output) if isinstance(output, list) else output for output in outputs]

        return outputs

    def vstack(self, outputs):
        """
        Merges outputs row-wise. Returns a list of lists which will be interpreted as a one to many transformation.

        Row-wise merge example (2 actions)

          Inputs: [a, b, c]

          Outputs => [[a1, b1, c1], [a2, b2, c2]]

          Row Merge => [[a1, a2], [b1, b2], [c1, c2]] = [a1, a2, b1, b2, c1, c2]

        Args:
            outputs: task outputs

        Returns:
            list of aggregated/zipped outputs as one to many transforms (row-wise)
        """

        if all(isinstance(output, np.ndarray) for output in outputs):
            return np.concatenate(np.stack(outputs, axis=1))

        # pylint: disable=E1101
        if all(torch.is_tensor(output) for output in outputs):
            return torch.cat(tuple(torch.stack(outputs, axis=1)))

        merge = []
        for x in zip(*outputs, strict=False):
            combine = []
            for y in x:
                if isinstance(y, list):
                    combine.extend(y)
                else:
                    combine.append(y)

            merge.append(OneToMany(combine))

        return merge

    def hstack(self, outputs):
        """
        Merges outputs column-wise. Returns a list of tuples which will be interpreted as a one to one transformation.

        Column-wise merge example (2 actions)

          Inputs: [a, b, c]

          Outputs => [[a1, b1, c1], [a2, b2, c2]]

          Column Merge => [(a1, a2), (b1, b2), (c1, c2)]

        Args:
            outputs: task outputs

        Returns:
            list of aggregated/zipped outputs as tuples (column-wise)
        """

        if all(isinstance(output, np.ndarray) for output in outputs):
            return np.stack(outputs, axis=1)

        # pylint: disable=E1101
        if all(torch.is_tensor(output) for output in outputs):
            return torch.stack(outputs, axis=1)

        return list(zip(*outputs, strict=False))

    def concat(self, outputs):
        """
        Merges outputs column-wise and concats values together into a string. Returns a list of strings.

        Concat merge example (2 actions)

          Inputs: [a, b, c]

          Outputs => [[a1, b1, c1], [a2, b2, c2]]

          Concat Merge => [(a1, a2), (b1, b2), (c1, c2)] => ["a1. a2", "b1. b2", "c1. c2"]

        Args:
            outputs: task outputs

        Returns:
            list of concat outputs
        """

        return [". ".join([str(y) for y in x if y]) for x in self.hstack(outputs)]


class OneToMany:
    """
    Encapsulates list output for a one to many transformation.
    """

    def __init__(self, values):
        """
        Creates a new OneToMany transformation.

        Args:
            values: list of outputs
        """

        self.values = values

    def __iter__(self):
        return self.values.__iter__()
