import pytest
from unittest.mock import MagicMock
from qmetagpt.quantum_algorithm_generator import get_agent
from qmetagpt.quantum_algorithm_generator.circuit_environment import QuantumCircuitEnv

class TestQuantumGenerator:
    @pytest.fixture
    def mock_env(self):
        env = MagicMock(spec=QuantumCircuitEnv)
        env.observation_space.shape = (8,)
        env.action_space = MagicMock()
        env.action_space.shape = (3,)
        return env

    def test_ppo_agent_initialization(self, mock_env):
        agent = get_agent("PPO", state_dim=8, action_dim=3)
        agent.build_model()
        assert agent.model is not None

    def test_a2c_agent_initialization(self, mock_env):
        agent = get_agent("A2C", state_dim=8, action_dim=3)
        agent.build_model()
        assert agent.model is not None

    def test_agent_registry_failure(self):
        with pytest.raises(ValueError):
            get_agent("INVALID_AGENT", state_dim=8, action_dim=3)