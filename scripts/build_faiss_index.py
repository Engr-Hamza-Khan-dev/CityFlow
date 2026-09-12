from rag.config import settings
from rag.indexer import RAGIndexer


def main():
    indexer = RAGIndexer(
        knowledge_base_dir=settings.knowledge_base_dir,
        index_dir=settings.faiss_index_dir,
        embedding_model=settings.embedding_model,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    count = indexer.build()
    print(f"FAISS index built successfully. Indexed chunks: {count}")
    print(f"Index directory: {settings.faiss_index_dir}")


if __name__ == "__main__":
    main()
