from pathlib import Path

from .config import RAGSettings, settings
from .indexer import RAGIndexer
from .retriever import CityFlowRetriever


class Member1RAGPipeline:
    """High-level API for building and querying the Member-1 RAG layer."""

    def __init__(self, config: RAGSettings = settings):
        self.config = config
        self.indexer = RAGIndexer(
            knowledge_base_dir=config.knowledge_base_dir,
            index_dir=config.faiss_index_dir,
            embedding_model=config.embedding_model,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )
        self.retriever = CityFlowRetriever(
            index_dir=config.faiss_index_dir,
            embedding_model=config.embedding_model,
            top_k=config.top_k,
        )

    def build_index(self) -> int:
        return self.indexer.build()

    def ensure_index(self) -> int:
        """Build the index if it does not exist; otherwise return chunk count."""
        if not self.retriever.is_ready():
            self.build_index()
        return self.retriever.indexed_chunks()

    def retrieve(self, query: str, k: int | None = None):
        self.ensure_index()
        return self.retriever.retrieve(query, k)
