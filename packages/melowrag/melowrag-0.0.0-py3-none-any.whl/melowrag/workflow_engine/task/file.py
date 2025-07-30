import os
import re

from .base import Task


class FileTask(Task):
    """
    Task that processes file paths
    """

    FILE = r"file:\/\/"

    def accept(self, element):
        element = re.sub(FileTask.FILE, "", element)

        return super().accept(element) and isinstance(element, str) and os.path.exists(element)

    def prepare(self, element):
        return re.sub(FileTask.FILE, "", element)
