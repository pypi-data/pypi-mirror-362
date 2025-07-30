import gym
import numpy as np
from gym import spaces
from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import state_fidelity, random_statevector
from qmetagpt.utils.logger import get_logger

logger = get_logger(__name__)

class QuantumCircuitEnv(gym.Env):
    def __init__(self, target_state=None, num_qubits=2, max_gates=50):
        super().__init__()
        self.num_qubits = num_qubits
        self.max_gates = max_gates
        
        # Use random state if target not provided
        self.target_state = target_state or random_statevector(2**num_qubits)
        
        # Define action space
        self.action_space = spaces.Dict({
            "gate_type": spaces.Discrete(8),  # 0: H, 1: X, 2: Y, 3: Z, 4: CX, 5: RX, 6: RY, 7: RZ
            "qubits": spaces.MultiDiscrete([num_qubits, num_qubits]),
            "parameters": spaces.Box(low=-np.pi, high=np.pi, shape=(1,))
        })
        
        # Observation space: statevector amplitudes (real + imag)
        self.observation_space = spaces.Box(
            low=-1, high=1, 
            shape=(2 * (2 ** num_qubits),),
            dtype=np.float32
        )
        
        self.current_circuit = QuantumCircuit(num_qubits)
        self.simulator = Aer.get_backend('statevector_simulator')
        
    def reset(self):
        self.current_circuit = QuantumCircuit(self.num_qubits)
        return self._get_state()
        
    def step(self, action):
        # Apply gate based on action
        self._apply_gate(action)
        
        # Calculate reward
        current_state = self._get_statevector()
        fidelity = state_fidelity(current_state, self.target_state)
        reward = fidelity - 0.01 * len(self.current_circuit)  # Complexity penalty
        
        # Check termination
        done = fidelity > 0.98 or len(self.current_circuit.data) >= self.max_gates
        
        return self._get_state(), reward, done, {"fidelity": fidelity}
    
    def _apply_gate(self, action):
        gate_type = action["gate_type"]
        qubits = action["qubits"]
        param = action["parameters"][0]
        
        gate_map = {
            0: self.current_circuit.h,
            1: self.current_circuit.x,
            2: self.current_circuit.y,
            3: self.current_circuit.z,
            4: self.current_circuit.cx,
            5: self.current_circuit.rx,
            6: self.current_circuit.ry,
            7: self.current_circuit.rz
        }
        
        try:
            if gate_type in [0, 1, 2, 3]:  # Single qubit gates
                gate_map[gate_type](qubits[0])
            elif gate_type == 4:  # CNOT
                gate_map[gate_type](qubits[0], qubits[1])
            elif gate_type in [5, 6, 7]:  # Parameterized gates
                gate_map[gate_type](param, qubits[0])
        except Exception as e:
            logger.error(f"Error applying gate: {e}")
    
    def _get_statevector(self):
        result = execute(self.current_circuit, self.simulator).result()
        return result.get_statevector()
    
    def _get_state(self):
        statevector = self._get_statevector()
        # Convert to real and imag arrays
        state_real = statevector.real
        state_imag = statevector.imag
        return np.concatenate([state_real, state_imag]).astype(np.float32)