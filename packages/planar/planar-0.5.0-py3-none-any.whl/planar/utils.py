import asyncio
import functools
import inspect
import random
from datetime import UTC, datetime
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

from inflection import pluralize, underscore


def snake_case_to_camel_case(snake_case: str) -> str:
    return "".join(word.capitalize() for word in snake_case.split("_"))


def create_path_prefix(model_name: str) -> str:
    """
    Create a URL path prefix from a model name.

    Example: 'Supplier' -> 'suppliers'
    """
    return f"{pluralize(underscore(model_name))}"


P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar("U")
R = TypeVar("R")


def asyncify(
    func: Callable[P, R],
) -> Callable[P, Coroutine[Any, Any, R]]:
    if inspect.iscoroutinefunction(func):
        raise ValueError("Function is already async")

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def exponential_backoff_with_jitter(
    attempt: int, base_delay: int = 1, max_delay: int = 60, jitter_factor=0.1
):
    """
    Calculate exponential backoff delay with random jitter.

    Args:
        attempt: Current attempt number (starts at 0)
        base_delay: Initial delay in seconds (default: 1)
        max_delay: Maximum delay in seconds (default: 60)
        jitter_factor: Fraction of delay to use for jitter (default: 0.1)

    Returns:
        Delay in seconds with jitter applied. Minimum possible delay is 1
        second.
    """
    # Calculate exponential backoff: base_delay * 2^attempt
    delay = min(base_delay * (2**attempt), max_delay)

    # Add random jitter: ±jitter_factor * delay
    jitter = delay * jitter_factor
    actual_delay = delay + random.uniform(-jitter, jitter)

    return max(1, actual_delay)  # Ensure at least 1 second
