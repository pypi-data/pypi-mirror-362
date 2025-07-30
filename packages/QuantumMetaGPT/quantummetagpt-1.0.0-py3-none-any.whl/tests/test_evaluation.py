import pytest
from qiskit import QuantumCircuit
from qmetagpt.evaluation_engine.quantum_evaluator import QuantumEvaluator

class TestEvaluation:
    @pytest.fixture
    def test_circuit(self):
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()
        return circuit

    def test_simulator_evaluation(self, test_circuit):
        evaluator = QuantumEvaluator(use_hardware=False)
        results = evaluator.evaluate(test_circuit, shots=1000)
        
        assert 'counts' in results
        assert '00' in results['counts'] or '11' in results['counts']
        assert results['time'] > 0
        assert 0.95 <= results['fidelity'] <= 1.0

    @pytest.mark.skip(reason="Requires real quantum hardware")
    def test_hardware_evaluation(self, test_circuit):
        evaluator = QuantumEvaluator(use_hardware=True)
        results = evaluator.evaluate(test_circuit, shots=1000)
        assert 'counts' in results
        assert results['time'] > 0