from langchain_core.documents import Document

from rag.chunker import GovernmentChunker


def test_chunker_adds_evidence_ids():
    docs = [Document(page_content="A " * 1000, metadata={"source_file": "x.txt"})]
    chunks = GovernmentChunker(chunk_size=700, chunk_overlap=100).split(docs)
    assert chunks
    assert all("evidence_id" in d.metadata for d in chunks)
    assert all(len(d.page_content) <= 700 for d in chunks)
