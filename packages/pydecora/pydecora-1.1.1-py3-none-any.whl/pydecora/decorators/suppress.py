import logging
from functools import wraps
from typing import Any, Callable, Tuple, Type


def suppress(
    exceptions: Type[Exception] | Tuple[Type[Exception]],
    default_value: Any = None,
    log: bool = False,
    log_level: int = logging.INFO,
) -> Callable:
    """Decorator to suppress specified exceptions, optionally returning default
    values and logging suppressions.

    :param exceptions: Exception or tuple of exceptions to suppress.
    :param default_value: Value to return when exception is suppressed.
    :param log: Whether or not to log the suppression.
    :param log_level: Logging level to use if log is True.
    """

    if not isinstance(exceptions, tuple):
        exceptions = (exceptions,)

    def dec(fn: Callable):

        @wraps(fn)
        def inner(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except exceptions as e:
                if log:
                    logging.log(
                        level=log_level,
                        msg=f"{e} was raised, returning default_value={default_value}",
                    )
                return default_value

        return inner

    return dec
