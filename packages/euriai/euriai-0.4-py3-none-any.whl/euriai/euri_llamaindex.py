from typing import Optional, List, Any, Dict, Union

try:
    from llama_index.core import VectorStoreIndex, ServiceContext
    from llama_index.core.llms import LLM
    from llama_index.core.schema import Document
except ImportError:
    VectorStoreIndex = ServiceContext = LLM = Document = None

class EuriaiLlamaIndex:
    """
    Full-featured wrapper for LlamaIndex integration in the EURI SDK.
    Allows document ingestion, index building, and querying with advanced config.
    """
    def __init__(self, llm: Optional[Any] = None, service_context: Optional[Any] = None):
        """
        Initialize the LlamaIndex wrapper.
        Args:
            llm: LLM object (optional)
            service_context: ServiceContext object (optional)
        """
        if VectorStoreIndex is None:
            raise ImportError("LlamaIndex is not installed. Please install with `pip install llama_index`.")
        self.llm = llm
        self.service_context = service_context or (ServiceContext.from_defaults(llm=llm) if llm else ServiceContext.from_defaults())
        self.index: Optional[Any] = None
        self.documents: List[Any] = []

    def add_documents(self, docs: List[Union[str, Dict[str, Any]]]) -> None:
        """Add documents (as strings or dicts) to the index."""
        for doc in docs:
            if isinstance(doc, str):
                self.documents.append(Document(text=doc))
            elif isinstance(doc, dict):
                self.documents.append(Document(**doc))
            else:
                raise ValueError("Document must be str or dict.")

    def build_index(self) -> None:
        """Build the vector index from current documents."""
        self.index = VectorStoreIndex.from_documents(self.documents)

    def query(self, query: str, **kwargs) -> Any:
        """
        Query the index with a string. Returns the response object.
        """
        if self.index is None:
            self.build_index()
        query_engine = self.index.as_query_engine(service_context=self.service_context)
        return query_engine.query(query, **kwargs)

    def get_index(self) -> Optional[Any]:
        return self.index

    def reset(self):
        """Reset documents and index."""
        self.documents = []
        self.index = None 