from pathlib import Path

from rag.document_loader import GovernmentDocumentLoader


def test_loader_reads_pdf_and_text():
    kb = Path(__file__).resolve().parents[1] / "knowledge_base"
    docs = GovernmentDocumentLoader(kb).load()
    assert len(docs) > 0
    assert any(d.metadata.get("file_type") == "pdf" for d in docs)
    assert any(d.metadata.get("file_type") == "txt" for d in docs)
