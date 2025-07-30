import pytest
from qiskit.circuit.library import RealAmplitudes
from qmetagpt.optimizer_engine.hybrid_optimizer import HybridOptimizer

class TestOptimizer:
    @pytest.fixture
    def test_circuit(self):
        circuit = RealAmplitudes(2, reps=1)
        return circuit

    def test_cobyla_optimizer(self, test_circuit):
        optimizer = HybridOptimizer("COBYLA")
        
        # Simple cost function (mock)
        def cost_function(params):
            return sum(p**2 for p in params)
        
        result = optimizer.optimize(test_circuit, cost_function)
        assert len(result) == test_circuit.num_parameters

    def test_invalid_optimizer(self):
        with pytest.raises(ValueError):
            HybridOptimizer("INVALID_OPTIMIZER")