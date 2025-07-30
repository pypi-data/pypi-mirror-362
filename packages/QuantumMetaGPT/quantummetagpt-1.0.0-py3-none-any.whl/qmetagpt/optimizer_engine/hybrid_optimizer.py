from qiskit.algorithms.optimizers import COBYLA, SPSA, NELDER_MEAD
from ..utils.logger import get_logger
from ..licensing import licensed_class

logger = get_logger(__name__)

@licensed_class(features=['pro'], protect_all_methods=True)
class HybridOptimizer:
    def __init__(self, optimizer_type="COBYLA"):
        self.optimizers = {
            "COBYLA": COBYLA(),
            "SPSA": SPSA(),
            "NELDER_MEAD": NELDER_MEAD()
        }
        self.optimizer = self.optimizers.get(optimizer_type.upper())
        if not self.optimizer:
            logger.error(f"Unsupported optimizer: {optimizer_type}")
            raise ValueError(f"Optimizer {optimizer_type} not supported")
        logger.info(f"Initialized {optimizer_type} optimizer")
    
    def optimize(self, circuit, cost_function):
        logger.info(f"Optimizing circuit with {self.optimizer.__class__.__name__}")
        try:
            result = self.optimizer.minimize(
                fun=cost_function,
                x0=circuit.parameters
            )
            return result.optimal_point
        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            raise