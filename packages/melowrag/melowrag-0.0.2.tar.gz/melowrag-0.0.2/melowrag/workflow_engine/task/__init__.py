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
from .console import ConsoleTask
from .export import ExportTask
from .factory import TaskFactory
from .file import FileTask
from .image import ImageTask
from .retrieve import RetrieveTask
from .service import ServiceTask
from .storage import StorageTask
from .stream import StreamTask
from .template import Formatter, RagTask, TemplateFormatter, TemplateTask
from .template import RagTask as ExtractorTask
from .url import UrlTask
from .workflow import WorkflowTask

__all__ = (
    "ConsoleTask",
    "ExportTask",
    "ExtractorTask",
    "FileTask",
    "Formatter",
    "ImageTask",
    "RagTask",
    "RetrieveTask",
    "ServiceTask",
    "StorageTask",
    "StreamTask",
    "Task",
    "TaskFactory",
    "TemplateFormatter",
    "TemplateTask",
    "UrlTask",
    "WorkflowTask",
)
