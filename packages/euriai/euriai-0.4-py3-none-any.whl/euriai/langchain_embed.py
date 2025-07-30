try:
    from langchain_core.embeddings import Embeddings
except ImportError:
    raise ImportError("LangChain is not installed. Please install with 'pip install euriai[langchain]' or 'pip install langchain'.")
from typing import List
from euriai.embedding import EuriaiEmbeddingClient


class EuriaiEmbeddings(Embeddings):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = EuriaiEmbeddingClient(api_key=api_key, model=model)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [embedding.tolist() for embedding in self.client.embed_batch(texts)]

    def embed_query(self, text: str) -> List[float]:
        return self.client.embed(text).tolist()
