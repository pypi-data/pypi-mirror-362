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

"""
Database imports
"""

from .base import Database
from .client import Client
from .db_encoder import Encoder, EncoderFactory, ImageEncoder, SerializeEncoder
from .db_schema import Base, Batch, Document, Object, Score, Section, SectionBase, Statement, idcolumn
from .db_sql import SQL, Aggregate, Expression, SQLError, Token
from .duckdb import DuckDB
from .embedded import Embedded
from .factory import DatabaseFactory
from .rdbms import RDBMS
from .sqlite import SQLite

__all__ = (
    "RDBMS",
    "SQL",
    "Aggregate",
    "Base",
    "Batch",
    "Client",
    "Database",
    "DatabaseFactory",
    "Document",
    "DuckDB",
    "Embedded",
    "Encoder",
    "EncoderFactory",
    "Expression",
    "ImageEncoder",
    "Object",
    "SQLError",
    "SQLite",
    "Score",
    "Section",
    "SectionBase",
    "SerializeEncoder",
    "Statement",
    "Token",
    "idcolumn",
)
