from pathlib import Path
from typing import Any, Dict, List

from .embeddings import EmbeddingProvider
from .faiss_store import FAISSStore


class CityFlowRetriever:
    """Public Member-1 interface consumed by Member 2 and the final app."""

    def __init__(
        self,
        index_dir: Path,
        embedding_model: str,
        top_k: int = 5,
    ):
        self.top_k = top_k
        self.embeddings = EmbeddingProvider(embedding_model)
        self.store = FAISSStore(index_dir, self.embeddings)

    def retrieve(self, query: str, k: int | None = None) -> List[Dict[str, Any]]:
        """Return ranked evidence records for a natural-language permit question.

        Contract for Member 2:
        [
          {
            "evidence_id": "...",
            "text": "...",
            "source": "...",
            "metadata": {...},
            "distance": 0.123
          }
        ]
        Lower FAISS distance means a closer semantic match.
        """
        if not query or not query.strip():
            return []

        results = self.store.similarity_search(query.strip(), k=k or self.top_k)

        evidence = []
        for document, distance in results:
            metadata = dict(document.metadata)
            evidence.append(
                {
                    "evidence_id": metadata.get("evidence_id", "unknown"),
                    "text": document.page_content.strip(),
                    "source": metadata.get("source_file", "unknown"),
                    "metadata": metadata,
                    "distance": float(distance),
                }
            )

        return evidence

    def is_ready(self) -> bool:
        return self.store.index_exists()

    def indexed_chunks(self) -> int:
        return self.store.count()
