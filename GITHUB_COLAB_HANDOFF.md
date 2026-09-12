# CityFlow Member 1 — GitHub & Colab Handoff

## What this branch contains

Member 1's RAG component:
- Government PDF/TXT loading
- Chunking
- `all-MiniLM-L6-v2` embeddings
- FAISS vector store
- Source/evidence-aware retrieval
- Retrieval tests

## GitHub structure

```text
knowledge_base/
rag/
scripts/
tests/
README.md
MEMBER1_HANDOFF.md
requirements.txt
.gitignore
.env.example
```

## Colab workflow

From `/content`, after extracting this project:

```python
!pip install -q -r /content/requirements.txt
```

Then build:

```python
!PYTHONPATH=/content python /content/scripts/build_faiss_index.py
```

Test:

```python
!PYTHONPATH=/content python /content/scripts/test_retrieval.py "What documents are required for hotel registration?"
```

## Important

Do not commit:
- `.env`
- API keys/tokens
- `.venv`
- `storage/faiss_index/`

The FAISS index is generated locally from the documents. A teammate can rebuild it with the build script.

## Member 2 interface

Use:

```python
from rag.pipeline import Member1RAGPipeline

rag = Member1RAGPipeline()
results = rag.retrieve("your question", k=5)
```

Each result contains:
- `evidence_id`
- `text`
- `source`
- `metadata`
- `distance`

Member 2 should consume this interface rather than accessing FAISS internals.
