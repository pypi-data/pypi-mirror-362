import requests
import numpy as np
from typing import List, Optional, Callable, Any
from llama_index.core.embeddings import BaseEmbedding

class EuriaiLlamaIndexEmbedding(BaseEmbedding):
    # Define class attributes as expected by Pydantic
    api_key: str
    model: str = "text-embedding-3-small"
    url: str = "https://api.euron.one/api/v1/euri/embeddings"

    def __init__(self, api_key: str, model: Optional[str] = None):
        """Initialize embedding model with API key and model name."""
        # Create parameters for the parent class with default values directly
        embed_params = {
            "api_key": api_key,
            "model": model if model is not None else "text-embedding-3-small",
        }
        
        # Initialize the parent class
        super().__init__(**embed_params)

    def _post_embedding(self, texts):
        """Helper method to post data to API and get embeddings."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "input": texts,
            "model": self.model
        }
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        return [np.array(obj["embedding"]).tolist() for obj in response.json()["data"]]

    def get_text_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        return self._post_embedding([text])[0]

    def get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for a query string."""
        return self.get_text_embedding(query)
        
    def get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts."""
        return self._post_embedding(texts)
        
    async def aget_query_embedding(self, query: str) -> List[float]:
        """Async version of get_query_embedding."""
        # We don't support async, so raise NotImplementedError
        raise NotImplementedError("Async embeddings not supported")