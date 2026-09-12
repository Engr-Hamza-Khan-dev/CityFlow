from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


class GovernmentDocumentLoader:
    """Loads supported government source files using LangChain loaders."""

    def __init__(self, knowledge_base_dir: Path):
        self.knowledge_base_dir = Path(knowledge_base_dir)

    def load(self) -> List[Document]:
        documents: List[Document] = []

        for path in sorted(self.knowledge_base_dir.iterdir()):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            if path.suffix.lower() == ".pdf":
                loaded = PyPDFLoader(str(path)).load()
            else:
                loaded = TextLoader(
                    str(path),
                    encoding="utf-8",
                    autodetect_encoding=True,
                ).load()

            for doc in loaded:
                doc.metadata = {
                    **doc.metadata,
                    "source_file": path.name,
                    "file_type": path.suffix.lower().lstrip("."),
                }
                documents.append(doc)

        if not documents:
            raise FileNotFoundError(
                f"No supported PDF/TXT documents found in {self.knowledge_base_dir}"
            )

        return documents
