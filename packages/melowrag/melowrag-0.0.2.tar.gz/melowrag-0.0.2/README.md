# MelowRAG

MelowRAG is a modular Python framework for semantic search, vector indexing, and retrieval-augmented generation (RAG). It provides a unified interface for embedding, indexing, searching, and managing data using dense, sparse, and hybrid vector models.

## Features

- **Embeddings Management**: Transform data into embeddings using various backends.
- **Flexible Indexing**: Build, update, and search indexes with support for dense, sparse, and hybrid models.
- **Database Integration**: Store and retrieve content using pluggable database backends.
- **Graph Algorithms**: Advanced graph-based search and topic modeling.
- **Pipelines**: Modular pipelines for text, audio, and image processing.
- **Remote Storage**: Archive and load indexes from local or cloud storage.
- **Extensible**: Easily add new models, scoring functions, or storage backends.

## Quick Start

```python
from melowrag import Embeddings

# Initialize embeddings
embedding = Embeddings()

# Index some texts
texts = ["The cat sat on the mat.", "Dogs are wonderful companions."]
embedding.index(texts)

# Search for similar content
results = embedding.search("animal companions", 1)
for result in results:
    print(f"Index: {result.index}, Score: {result.score}")
```
 

## Installation

```bash
pip install -e .
```

## License

This project is licensed under the terms of the MIT license.
