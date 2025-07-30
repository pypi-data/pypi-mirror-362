import functools
from qmetagpt.utils.logger import get_logger

logger = get_logger(__name__)

def handle_quantum_error(func):
    """Decorator for handling quantum computation errors"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Quantum operation failed: {e}")
            # Add error mitigation or recovery logic here
            raise
    return wrapper

def handle_llm_error(func):
    """Decorator for handling LLM API errors"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"LLM operation failed: {e}")
            # Implement fallback to another model or cached response
            return f"Error: {str(e)}"
    return wrapper

def retry_on_failure(max_retries=3, delay=1):
    """Decorator for retrying operations on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Retry {attempt+1}/{max_retries} for {func.__name__}")
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator