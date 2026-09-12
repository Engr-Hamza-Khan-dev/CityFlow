from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class RAGSettings:
    knowledge_base_dir: Path = ROOT_DIR / os.getenv("KNOWLEDGE_BASE_DIR", "knowledge_base")
    faiss_index_dir: Path = ROOT_DIR / os.getenv("FAISS_INDEX_DIR", "storage/faiss_index")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    top_k: int = int(os.getenv("RAG_TOP_K", "5"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "700"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))


settings = RAGSettings()
