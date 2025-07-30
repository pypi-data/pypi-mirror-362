import json

from .base import Task


class ConsoleTask(Task):
    """
    Task that prints task elements to the console.
    """

    def __call__(self, elements, executor=None):
        outputs = super().__call__(elements, executor)

        print("Inputs:", json.dumps(elements, indent=2))
        print("Outputs:", json.dumps(outputs, indent=2))

        return outputs
