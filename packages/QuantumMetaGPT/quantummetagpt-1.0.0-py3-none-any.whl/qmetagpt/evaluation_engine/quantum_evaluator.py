from qiskit import Aer, IBMQ, transpile
from qiskit.providers import Options
from qiskit.quantum_info import state_fidelity
from ..utils.logger import get_logger
from ..licensing import licensed_class
import time

logger = get_logger(__name__)

@licensed_class(features=['core'], protect_all_methods=True)
class QuantumEvaluator:
    def __init__(self, use_hardware=False, backend_name='ibmq_manila'):
        self.use_hardware = use_hardware
        self.simulator = Aer.get_backend('aer_simulator_statevector')
        
        if use_hardware:
            logger.info("Connecting to IBM Quantum")
            IBMQ.load_account()
            self.backend = IBMQ.get_backend(backend_name)
        else:
            self.backend = self.simulator
    
    def evaluate(self, circuit, shots=1024):
        logger.info(f"Evaluating circuit on {'hardware' if self.use_hardware else 'simulator'}")
        start_time = time.time()
        
        # Transpile for target backend
        transpiled = transpile(circuit, self.backend)
        
        # Execute
        job = self.backend.run(transpiled, shots=shots)
        result = job.result()
        
        # Calculate metrics
        execution_time = time.time() - start_time
        fidelity = self._calculate_fidelity(result, circuit) if not self.use_hardware else None
        
        return {
            "counts": result.get_counts(),
            "time": execution_time,
            "fidelity": fidelity,
            "success": job.status().name == 'DONE'
        }
    
    def _calculate_fidelity(self, result, original_circuit):
        try:
            statevector = result.get_statevector()
            ideal_sv = Aer.get_backend('statevector_simulator').run(original_circuit).result().get_statevector()
            return state_fidelity(statevector, ideal_sv)
        except Exception as e:
            logger.warning(f"Fidelity calculation failed: {e}")
            return None