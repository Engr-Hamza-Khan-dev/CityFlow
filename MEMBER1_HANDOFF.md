# CityFlow — Member 1 Handoff

## Ownership

Member 1 owns only the RAG layer:
1. Government document ingestion
2. Chunking
3. Embeddings
4. FAISS vector store
5. Retrieval
6. Retrieval tests
7. Stable interface for Member 2

This matches the team division: Member 1 owns the government-document pipeline, chunking, embeddings, vector database, and retrieval.

## Tech decisions

- Document loading: LangChain `PyPDFLoader` and `TextLoader`
- Chunking: LangChain `RecursiveCharacterTextSplitter`
- Embeddings: HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- Vector store: FAISS
- LLM/reasoning: NOT owned by Member 1
- UI: NOT owned by Member 1
- QA/integration: Member 4

The development outline explicitly allows FAISS/ChromaDB and recommends LangChain loaders, 500–800 character chunks, and `all-MiniLM-L6-v2`.

## Interface for Member 2

```python
from rag.pipeline import Member1RAGPipeline

rag = Member1RAGPipeline()
rag.ensure_index()

evidence = rag.retrieve(
    "What documents are required for a restaurant registration in Lahore?",
    k=5,
)
```

Each evidence item is:

```python
{
    "evidence_id": "source.pdf:page-1:chunk-3",
    "text": "...",
    "source": "source.pdf",
    "metadata": {
        "source_file": "source.pdf",
        "file_type": "pdf",
        "page": 0,
        "chunk_index": 3,
        "evidence_id": "source.pdf:page-1:chunk-3"
    },
    "distance": 0.123
}
```

Do not make Member 2 depend on FAISS internals. Member 2 should call only `Member1RAGPipeline.retrieve()`.

## Cloud behavior

`ensure_index()` automatically builds the FAISS index when the index files do not exist. This is important for Streamlit Community Cloud, where the runtime may start without the local `storage/` directory.

For a hackathon MVP, the source documents in `knowledge_base/` are the source of truth. If the knowledge base changes, rebuild the index.

## Manual commands

Install:

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Build:

```bash
python scripts/build_faiss_index.py
```

Test retrieval:

```bash
python scripts/test_retrieval.py "What documents are required for restaurant registration?"
```

Run tests:

```bash
pytest -q
```

## Integration rule

Member 2 should integrate with this RAG layer early, as the team document explicitly says Member 1 and Member 2 should integrate early because RAG retrieval and AI reasoning are the core of CityFlow.

Member 3 can build the Streamlit UI against the retrieval/answer contract without changing this package.

Member 4 should test retrieval quality and source grounding.
