from pathlib import Path

from .chunker import GovernmentChunker
from .document_loader import GovernmentDocumentLoader
from .embeddings import EmbeddingProvider
from .faiss_store import FAISSStore


class RAGIndexer:
    """Orchestrates loading -> chunking -> embedding -> FAISS persistence."""

    def __init__(
        self,
        knowledge_base_dir: Path,
        index_dir: Path,
        embedding_model: str,
        chunk_size: int = 700,
        chunk_overlap: int = 100,
    ):
        self.loader = GovernmentDocumentLoader(knowledge_base_dir)
        self.chunker = GovernmentChunker(chunk_size, chunk_overlap)
        self.embeddings = EmbeddingProvider(embedding_model)
        self.store = FAISSStore(index_dir, self.embeddings)

    def build(self) -> int:
        documents = self.loader.load()
        chunks = self.chunker.split(documents)
        self.store.build(chunks)
        return len(chunks)
