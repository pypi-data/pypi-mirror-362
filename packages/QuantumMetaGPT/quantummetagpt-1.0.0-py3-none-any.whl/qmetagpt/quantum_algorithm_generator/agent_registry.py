from .agents.ppo_agent import PPOAgent
from .agents.a2c_agent import A2CAgent
from .agents.ddpg_agent import DDPGAgent
from .agents.sac_agent import SACAgent
from ..utils.logger import get_logger
from ..licensing import require_license

logger = get_logger(__name__)

AGENT_REGISTRY = {
    "PPO": PPOAgent,
    "A2C": A2CAgent,
    "DDPG": DDPGAgent,
    "SAC": SACAgent
}

@require_license(features=['core'])
def get_agent(agent_name, state_dim, action_dim, **kwargs):
    agent_class = AGENT_REGISTRY.get(agent_name.upper())
    if not agent_class:
        error_msg = f"Unknown agent: {agent_name}. Available: {list(AGENT_REGISTRY.keys())}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    logger.info(f"Initializing {agent_name} agent")
    return agent_class(state_dim, action_dim, **kwargs)