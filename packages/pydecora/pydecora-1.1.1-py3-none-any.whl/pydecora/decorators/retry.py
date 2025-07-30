from random import uniform
import time
from functools import wraps
from typing import Callable, Any, Optional


def retry(
    times: int,
    exceptions: tuple[type[Exception]] = (Exception,),
    delay: float = 0,
    backoff_multiplier: float = 1,
    delay_cap: float = 30 * 60,
    jitter: float = 0,
    callback: Optional[Callable[[int, Exception], None]] = None,
) -> Callable:
    """A decorator that retries a function call upon specified exceptions.

    Retries up to `times` times, with optional delay, exponential backoff, jitter,
    and a callback on failure.

    :param times: Total number of attempts (including the initial call).
    :param exceptions: Tuple of exception types to catch and retry on.
    :param delay: Initial delay in seconds before retrying.
    :param backoff_multiplier: Multiplier applied to delay after each failure.
    :param delay_cap: Maximum delay allowed between retries.
    :param jitter: Max random jitter (in seconds) to add to delay.
    :param callback: Optional function called after each failure.
        Receives (attempt number, exception instance).
    """

    def dec(fn: Callable[..., Any]) -> Callable:

        @wraps(fn)
        def inner(*args, **kwargs) -> Any:
            current_delay = delay

            for i in range(1, times):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    if callback:
                        callback(i, e)

                time.sleep(min(current_delay + uniform(0, jitter), delay_cap))
                current_delay *= backoff_multiplier

            return fn(*args, **kwargs)

        return inner

    return dec
