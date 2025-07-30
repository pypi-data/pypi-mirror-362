import openai
from transformers import pipeline
from ..utils.error_handling import handle_llm_error
from ..utils.logger import get_logger
from ..licensing import licensed_class

logger = get_logger(__name__)

@licensed_class(features=['pro'], protect_all_methods=True)
class LLMProcessor:
    def __init__(self, model_type="openai", model_name="gpt-4"):
        self.model_type = model_type
        self.model_name = model_name
        
        if model_type == "llama":
            logger.info(f"Loading LLaMA model: {model_name}")
            self.model = pipeline("text-generation", model=model_name)
    
    @handle_llm_error
    def summarize(self, text: str) -> str:
        if self.model_type == "openai":
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": f"Summarize this quantum research paper:\n{text}"}]
            )
            return response.choices[0].message.content.strip()
        else:
            return self.model(text, max_length=512)[0]['generated_text']
    
    @handle_llm_error
    def extract_pseudocode(self, text: str) -> str:
        if self.model_type == "openai":
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": f"Extract quantum algorithm pseudocode from:\n{text}"}]
            )
            return response.choices[0].message.content.strip()
        else:
            return self.model(f"EXTRACT PSEUDOCODE: {text}")[0]['generated_text']