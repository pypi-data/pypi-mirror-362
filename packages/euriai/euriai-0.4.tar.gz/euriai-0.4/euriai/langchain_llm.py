try:
    from langchain.llms.base import LLM
except ImportError:
    raise ImportError("LangChain is not installed. Please install with 'pip install euriai[langchain]' or 'pip install langchain'.")
from typing import Optional, List
from euriai import EuriaiClient


class EuriaiLangChainLLM(LLM):
    model: str = "gpt-4.1-nano"
    temperature: float = 0.7
    max_tokens: int = 300

    def __init__(self, api_key: str, model: str = "gpt-4.1-nano", temperature: float = 0.7, max_tokens: int = 300, **kwargs):
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens, **kwargs)
        object.__setattr__(self, "_client", EuriaiClient(api_key=api_key, model=model))

    @property
    def _llm_type(self) -> str:
        return "euriai"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self._client.generate_completion(
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stop=stop
        )
        return response.get("choices", [{}])[0].get("message", {}).get("content", "")
