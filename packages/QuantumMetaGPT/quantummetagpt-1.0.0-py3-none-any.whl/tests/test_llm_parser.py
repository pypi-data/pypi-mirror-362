import pytest
from qmetagpt.llm_paper_parser import arxiv_parser, llm_integration
from unittest.mock import patch

@patch('arxiv.Client')
def test_parse_arxiv_paper(mock_client):
    # Mock arXiv response
    class MockPaper:
        title = "Quantum Machine Learning"
        summary = "Abstract about quantum ML"
        authors = [type('Author', (), {'name': 'John Doe'})]
        published = "2023-01-01"
        pdf_url = "http://arxiv.org/pdf/1234.5678"
    
    mock_client.return_value.results.return_value = iter([MockPaper()])
    
    paper = arxiv_parser.parse_arxiv_paper("quant-ph/12345678")
    assert paper['title'] == "Quantum Machine Learning"
    assert "quantum ML" in paper['abstract']
    assert paper['authors'] == ['John Doe']

@patch('openai.ChatCompletion.create')
def test_llm_summarize(mock_openai):
    mock_openai.return_value = type('Response', (), {
        'choices': [type('Choice', (), {
            'message': type('Message', (), {'content': 'Summary text'})
        })]
    })
    
    processor = llm_integration.LLMProcessor()
    summary = processor.summarize("Long text about quantum computing")
    assert summary == "Summary text"