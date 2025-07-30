import re

from .base import Task


class UrlTask(Task):
    """
    Task that processes urls
    """

    PREFIX = r"\w+:\/\/"

    def accept(self, element):
        return super().accept(element) and re.match(UrlTask.PREFIX, element.lower())
