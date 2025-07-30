import numpy as np
from qiskit.quantum_info import state_fidelity
from ..utils.logger import get_logger

logger = get_logger(__name__)

class RewardCalculator:
    def __init__(self, strategy="fidelity", weights=(0.7, 0.2, 0.1)):
        self.strategy = strategy
        self.weights = weights
        
    def calculate(self, results: dict, target=None) -> float:
        """Calculate reward based on evaluation results"""
        if self.strategy == "fidelity":
            return self._fidelity_reward(results.get('fidelity', 0))
        elif self.strategy == "cost":
            return self._cost_reward(results.get('cost_value', 1))
        elif self.strategy == "composite":
            return self._composite_reward(
                results.get('fidelity', 0),
                results.get('cost_value', 1),
                results.get('depth', 1)
            )
        elif self.strategy == "hardware":
            return self._hardware_aware_reward(
                results.get('fidelity', 0),
                results.get('execution_time', 1),
                results.get('error_rate', 0.1)
            )
        else:
            logger.warning(f"Unknown reward strategy: {self.strategy}. Using fidelity.")
            return self._fidelity_reward(results.get('fidelity', 0))
    
    def _fidelity_reward(self, fidelity: float) -> float:
        return np.clip(fidelity, 0, 1)
    
    def _cost_reward(self, cost_value: float) -> float:
        return np.exp(-cost_value)
    
    def _composite_reward(self, fidelity: float, cost: float, depth: int) -> float:
        return (
            self.weights[0] * self._fidelity_reward(fidelity) +
            self.weights[1] * self._cost_reward(cost) +
            self.weights[2] * (1 / depth)
        )
    
    def _hardware_aware_reward(self, fidelity: float, execution_time: float, error_rate: float) -> float:
        return fidelity * (1 - error_rate) / np.log(execution_time + 1)