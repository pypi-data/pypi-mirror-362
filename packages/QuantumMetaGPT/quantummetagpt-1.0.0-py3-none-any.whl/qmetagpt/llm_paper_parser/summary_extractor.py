import re
from ..utils.logger import get_logger
from .llm_integration import LLMProcessor

logger = get_logger(__name__)

class SummaryExtractor:
    def __init__(self, model_type="openai"):
        self.llm = LLMProcessor(model_type)
    
    def extract_key_points(self, text: str) -> list:
        """Extract key points from research paper text"""
        prompt = f"Extract the 5 most important quantum computing insights from:\n{text}"
        response = self.llm.summarize(prompt)
        return self._parse_bullet_points(response)
    
    def extract_problem_statement(self, text: str) -> str:
        """Extract the core problem statement from research paper"""
        prompt = f"Identify and extract the main quantum computing problem statement from:\n{text}"
        return self.llm.summarize(prompt)
    
    def _parse_bullet_points(self, text: str) -> list:
        """Parse bullet points from LLM response"""
        points = []
        for line in text.split('\n'):
            if re.match(r'^[-•*]\s+', line):
                points.append(re.sub(r'^[-•*]\s+', '', line))
            elif re.match(r'^\d+\.\s+', line):
                points.append(re.sub(r'^\d+\.\s+', '', line))
        return points if points else [text]