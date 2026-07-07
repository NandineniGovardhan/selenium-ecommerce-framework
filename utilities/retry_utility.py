"""
retry_utility.py
------------------
Generic retry mechanism for flaky operations (e.g. transient stale-element
errors, network blips). This is NOT a substitute for explicit waits — it
is a last-resort safety net around otherwise-correct synchronized code.
"""

import functools
import time
from typing import Any, Callable, Tuple, Type

from utilities.logger_utility import get_logger

log = get_logger(__name__)


def retry_on_exception(
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
):
    """
    Decorator that retries a function call on the given exception types.

    Args:
        exceptions: Tuple of exception types that should trigger a retry.
        max_attempts: Maximum number of attempts before raising.
        delay_seconds: Fixed delay between attempts.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:  # noqa: BLE001 - intentional broad catch
                    last_exception = exc
                    log.warning(
                        "Attempt %d/%d failed for '%s': %s",
                        attempt, max_attempts, func.__name__, exc,
                    )
                    if attempt < max_attempts:
                        time.sleep(delay_seconds)
            log.error("All %d attempts failed for '%s'", max_attempts, func.__name__)
            raise last_exception

        return wrapper

    return decorator


class RetryUtility:
    """Programmatic (non-decorator) retry helper for inline use."""

    @staticmethod
    def run_with_retry(
        func: Callable,
        max_attempts: int = 3,
        delay_seconds: float = 1.0,
        exceptions: Tuple[Type[BaseException], ...] = (Exception,),
        *args,
        **kwargs,
    ) -> Any:
        """Runs `func(*args, **kwargs)` with retry logic and returns its result."""
        last_exception = None
        for attempt in range(1, max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:  # noqa: BLE001
                last_exception = exc
                log.warning("Retry attempt %d/%d failed: %s", attempt, max_attempts, exc)
                if attempt < max_attempts:
                    time.sleep(delay_seconds)
        raise last_exception
