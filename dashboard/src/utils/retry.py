import asyncio
import logging
from functools import wraps
from typing import Tuple, Type, Optional, Callable, Any


def async_retry_decorator(
        retries: int = 3,
        delay: float = 0.1,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
        logger: Optional[logging.Logger] = None,
):
    """Decorator for retrying async functions.

    Args:
        retries: Number of retries.
        delay: Delay between retries.
        exceptions: Tuple of exceptions to catch.
        logger: Logger to use. If None, print.

    Returns:
        Decorated function.
    """
    if not logger:
        logger = logging.getLogger(__name__)

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            mtries = retries
            while mtries > 1:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    msg = f"{func.__name__}: {e}, Retrying in {delay} seconds..."
                    logger.warning(msg)
                    await asyncio.sleep(delay)
                    mtries -= 1
            return await func(*args, **kwargs)

        return wrapper

    return decorator
