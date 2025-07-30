from ..utils.logger import get_logger

logger = get_logger(__name__)

PROBLEM_TYPES = ["QAOA", "VQE", "Grover", "QFT", "QuantumChemistry", "Optimization"]

class TaskSynthesizer:
    def __init__(self):
        self.problem_mapping = {
            "QAOA": self._handle_qaoa,
            "VQE": self._handle_vqe,
            "Grover": self._handle_grover
        }
    
    def synthesize(self, paper_data: dict) -> dict:
        problem_type = self._detect_problem_type(paper_data['abstract'])
        logger.info(f"Detected problem type: {problem_type}")
        
        handler = self.problem_mapping.get(problem_type, self._generic_handler)
        return handler(paper_data)
    
    def _detect_problem_type(self, text: str) -> str:
        text_lower = text.lower()
        for ptype in PROBLEM_TYPES:
            if ptype.lower() in text_lower:
                return ptype
        return "Generic"
    
    def _handle_qaoa(self, paper_data) -> dict:
        return {
            "type": "QAOA",
            "qubits": 4,
            "cost_operator": "Ising model",
            "mixer": "X mixer",
            "layers": 3
        }
    
    def _handle_vqe(self, paper_data) -> dict:
        return {
            "type": "VQE",
            "molecule": "H2",
            "ansatz": "UCCSD",
            "qubits": 4
        }
    
    def _handle_grover(self, paper_data) -> dict:
        return {
            "type": "Grover",
            "oracle": "custom function",
            "qubits": 5,
            "iterations": 2
        }
    
    def _generic_handler(self, paper_data) -> dict:
        return {"type": "Generic", "qubits": 4}