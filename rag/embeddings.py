from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingProvider:
    """Creates the shared embedding model used by indexing and retrieval."""

    def __init__(self, model_name: str):
        self.model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def embed_documents(self, texts):
        return self.model.embed_documents(texts)

    def embed_query(self, text):
        return self.model.embed_query(text)

    @property
    def langchain_embeddings(self):
        return self.model
