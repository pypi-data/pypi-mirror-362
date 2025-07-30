import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def timer(func):
    """A decorator that prints how long a function took to run."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} ran in {end_time - start_time:.4f}s")
        return result
    return wrapper