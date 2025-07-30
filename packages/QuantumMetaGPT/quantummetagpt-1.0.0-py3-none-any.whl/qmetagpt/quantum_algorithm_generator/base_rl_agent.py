from abc import ABC, abstractmethod
import numpy as np
from qiskit import QuantumCircuit
from ..utils.logger import get_logger
from ..licensing import licensed_class

logger = get_logger(__name__)

@licensed_class(features=['core'], protect_all_methods=True)
class BaseRLAgent(ABC):
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        
    @abstractmethod
    def build_model(self, policy_kwargs=None):
        pass
    
    @abstractmethod
    def generate_circuit(self, state):
        pass
    
    @abstractmethod
    def train(self, env, total_timesteps):
        pass
    
    @abstractmethod
    def save(self, path):
        pass
    
    @abstractmethod
    def load(self, path):
        pass
    
    def _action_to_circuit(self, action):
        logger.info("Converting RL action to quantum circuit")
        # Placeholder implementation
        return QuantumCircuit(2)
    
    def _preprocess_task(self, task_spec):
        logger.info(f"Preprocessing task: {task_spec['type']}")
        return np.zeros(self.state_dim)