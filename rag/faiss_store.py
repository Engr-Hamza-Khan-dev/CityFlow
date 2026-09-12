from pathlib import Path
from typing import List, Optional, Tuple

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from .embeddings import EmbeddingProvider


class FAISSStore:
    """Thin persistence/query wrapper around a LangChain FAISS vector store."""

    def __init__(self, index_dir: Path, embedding_provider: EmbeddingProvider):
        self.index_dir = Path(index_dir)
        self.embedding_provider = embedding_provider
        self.store: Optional[FAISS] = None

    def build(self, documents: List[Document]) -> None:
        if not documents:
            raise ValueError("Cannot build FAISS index from zero documents.")

        self.store = FAISS.from_documents(
            documents,
            self.embedding_provider.langchain_embeddings,
        )
        self.save()

    def save(self) -> None:
        if self.store is None:
            raise RuntimeError("FAISS store has not been built or loaded.")

        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.store.save_local(str(self.index_dir))

    def load(self) -> None:
        if not self.index_exists():
            raise FileNotFoundError(
                f"FAISS index not found at {self.index_dir}. Build it first."
            )

        self.store = FAISS.load_local(
            str(self.index_dir),
            self.embedding_provider.langchain_embeddings,
            allow_dangerous_deserialization=True,
        )

    def index_exists(self) -> bool:
        return (
            (self.index_dir / "index.faiss").exists()
            and (self.index_dir / "index.pkl").exists()
        )

    def similarity_search(
        self,
        query: str,
        k: int = 5,
    ) -> List[Tuple[Document, float]]:
        if self.store is None:
            self.load()

        return self.store.similarity_search_with_score(query, k=k)

    def count(self) -> int:
        if self.store is None:
            if not self.index_exists():
                return 0
            self.load()

        return len(self.store.index_to_docstore_id)
