import sys
import os
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../euriai')))
from langchain_llm import EuriaiLangChainLLM

@pytest.fixture(autouse=True)
def patch_dependencies():
    # Patch EuriaiClient and LLM in langchain_llm's namespace
    with patch('langchain_llm.EuriaiClient', MagicMock(name='EuriaiClient')) as client_mock, \
         patch('langchain_llm.LLM', MagicMock(name='LLM')) as llm_mock:
        yield

def test_constructor():
    llm = EuriaiLangChainLLM(api_key='test-key', model='test-model', temperature=0.5, max_tokens=123)
    assert llm.model == 'test-model'
    assert llm.temperature == 0.5
    assert llm.max_tokens == 123
    assert hasattr(llm, '_client')

def test_llm_type_property():
    llm = EuriaiLangChainLLM(api_key='test-key')
    assert llm._llm_type == 'euriai'

def test_call_method():
    llm = EuriaiLangChainLLM(api_key='test-key')
    # Patch the _client.generate_completion method
    llm._client.generate_completion = MagicMock(return_value={
        'choices': [
            {'message': {'content': 'Hello, world!'}}
        ]
    })
    result = llm._call('Say hello')
    assert result == 'Hello, world!'
    llm._client.generate_completion.assert_called_once() 