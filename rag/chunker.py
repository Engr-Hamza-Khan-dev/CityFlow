from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class GovernmentChunker:
    """Splits source documents into retrieval-sized, overlapping chunks."""

    def __init__(self, chunk_size: int = 700, chunk_overlap: int = 100):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", "; ", " ", ""],
        )

    def split(self, documents: List[Document]) -> List[Document]:
        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            source = chunk.metadata.get("source_file", "unknown")
            page = chunk.metadata.get("page")
            page_part = f":page-{page + 1}" if isinstance(page, int) else ""
            chunk.metadata = {
                **chunk.metadata,
                "chunk_index": index,
                "evidence_id": f"{source}{page_part}:chunk-{index}",
            }

        return chunks
