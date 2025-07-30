from qiskit.algorithms.optimizers import Optimizer
from qmetagpt.utils.logger import get_logger

logger = get_logger(__name__)

# Plugin registry
OPTIMIZER_PLUGINS = {}

def register_optimizer(name, optimizer_class):
    if not issubclass(optimizer_class, Optimizer):
        raise TypeError("Optimizer class must be a subclass of qiskit.algorithms.optimizers.Optimizer")
    OPTIMIZER_PLUGINS[name] = optimizer_class
    logger.info(f"Registered optimizer plugin: {name}")

def get_optimizer_plugin(name, **kwargs):
    plugin = OPTIMIZER_PLUGINS.get(name)
    if not plugin:
        logger.error(f"Optimizer plugin '{name}' not found")
        raise ValueError(f"Optimizer plugin '{name}' not found. Available plugins: {list(OPTIMIZER_PLUGINS.keys())}")
    return plugin(**kwargs)

# Example plugin registration (would be called from external code)
# register_optimizer("MyOptimizer", MyCustomOptimizerClass)