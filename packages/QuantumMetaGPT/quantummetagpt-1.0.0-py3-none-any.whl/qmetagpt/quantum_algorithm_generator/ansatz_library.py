from qiskit.circuit.library import (
    EfficientSU2, RealAmplitudes, QAOAAnsatz,
    TwoLocal, NLocal, ExcitationPreserving
)
from ..utils.logger import get_logger

logger = get_logger(__name__)

class AnsatzLibrary:
    def __init__(self):
        self.templates = {
            "EfficientSU2": EfficientSU2,
            "RealAmplitudes": RealAmplitudes,
            "QAOA": QAOAAnsatz,
            "TwoLocal": TwoLocal,
            "NLocal": NLocal,
            "ExcitationPreserving": ExcitationPreserving,
            "HardwareEfficient": self._hardware_efficient_ansatz
        }
    
    def get_ansatz(self, name: str, num_qubits: int, **kwargs):
        """Retrieve parameterized quantum circuit template"""
        constructor = self.templates.get(name)
        if not constructor:
            logger.error(f"Unknown ansatz: {name}")
            raise ValueError(f"Unknown ansatz template: {name}")
        
        logger.info(f"Building {name} ansatz with {num_qubits} qubits")
        return constructor(num_qubits, **kwargs) if name != "HardwareEfficient" else constructor(num_qubits, **kwargs)
    
    def _hardware_efficient_ansatz(self, num_qubits: int, reps: int = 2, entanglement: str = "linear"):
        """Create hardware-efficient ansatz with alternating rotation and entanglement layers"""
        from qiskit.circuit.library import TwoLocal
        return TwoLocal(
            num_qubits,
            rotation_blocks=["rx", "ry", "rz"],
            entanglement_blocks="cz",
            entanglement=entanglement,
            reps=reps,
            insert_barriers=True
        )