# Lateness - Modern ColBERT for Late Interaction

A Python package for Modern ColBERT (late interaction) embeddings with native multi-vector support for efficient retrieval using Qdrant vector database.

## Features

- **Dual Backend Architecture**: ONNX for fast retrieval, PyTorch for GPU indexing
- **Native Multi-Vector Support**: Optimized for Qdrant's MaxSim comparator
- **Smart Installation**: Lightweight retrieval or heavy indexing based on your needs
- **Production Ready**: Separate deployment targets for different workloads

## Quick Start

### Installation

```bash
# Lightweight retrieval (ONNX + Qdrant)
pip install lateness

# Heavy indexing (PyTorch + Transformers + ONNX + Qdrant)
pip install lateness[index]
```

### Backend Selection

### Basic Usage

**Default Installation (ONNX Backend):**
```python

# pip install lateness
from lateness import ModernColBERT
colbert = ModernColBERT("prithivida/modern_colbert_base_en_v1")
# Output:
# 🚀 Using ONNX backend Using ONNX backend (default, for GPU accelerated indexing, install lateness[index] and set LATENESS_USE_TORCH=true)
# 🔄 Downloading model: prithivida/modern_colbert_base_en_v1
# ✅ ONNX ColBERT loaded with providers: ['CPUExecutionProvider']
# Query max length: 256, Document max length: 300
```

**Index Installation (PyTorch Backend):**
```python
# pip install lateness[index]
import os
os.environ['LATENESS_USE_TORCH'] = 'true'
from lateness import ModernColBERT

colbert = ModernColBERT("prithivida/modern_colbert_base_en_v1")
# Output:
# 🚀 Using PyTorch backend (LATENESS_USE_TORCH=true)
# 🔄 Downloading model: prithivida/modern_colbert_base_en_v1
# Loading model from: /root/.cache/huggingface/hub/models--prithivida--modern_colbert_base_en_v1/...
# ✅ PyTorch ColBERT loaded on cuda
# Query max length: 256, Document max length: 300
```

**Complete Example with Qdrant:**

For a complete working example with Qdrant integration, environment setup, and testing instructions, see the [examples/qdrant folder](./examples/qdrant/).

The examples include:
- Environment setup and testing
- Local Qdrant server management
- Complete indexing and retrieval workflows
- Both ONNX and PyTorch backend examples

## Architecture

### Two Deployment Models

**Retrieval Service (Lightweight)**
```bash
pip install lateness
```
- ONNX backend (fast CPU inference)
- Qdrant integration
- ~50MB total dependencies
- Perfect for user-facing search APIs

**Indexing Service (Heavy)**
```bash
pip install lateness[index]
```
- PyTorch backend (GPU acceleration)
- Full Transformers support
- ~2GB+ dependencies
- Perfect for batch document processing

### Backend Selection

The package uses environment variables for backend control:

- **Default behavior** → ONNX backend (CPU retrieval)
- **`LATENESS_USE_TORCH=true`** → PyTorch backend (GPU indexing)

**Note:** PyTorch backend requires `pip install lateness[index]` to install PyTorch dependencies.

## API Reference

### ModernColBERT

```python
from lateness import ModernColBERT

# Initialize
colbert = ModernColBERT("prithivida/modern_colbert_base_en_v1")

# Encode queries
query_embeddings = colbert.encode_queries(["What is AI?"])

# Encode documents  
doc_embeddings = colbert.encode_documents(["AI is artificial intelligence"])

# Compute similarity
scores = ModernColBERT.compute_similarity(query_embeddings, doc_embeddings)
```

### Qdrant Integration

```python
from lateness import QdrantIndexer, QdrantRetriever
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

# Indexing
indexer = QdrantIndexer(client, "documents")
indexer.create_collection()
indexer.index_documents_simple(documents)

# Retrieval
retriever = QdrantRetriever(client, "documents")
results = retriever.search_simple("query", top_k=10)
```

## License

Apache License 2.0

## Contributing

Contributions welcome! Please check our [contributing guidelines](CONTRIBUTING.md).
