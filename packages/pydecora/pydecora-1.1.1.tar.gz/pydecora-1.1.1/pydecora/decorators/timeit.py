import time
import logging
from functools import wraps
from typing import Optional, Literal, Callable


def timeit(
    label: Optional[str] = None,
    log_args: bool = False,
    log_result: bool = False,
    log_level: int = logging.INFO,
    unit: Literal["ms", "s"] = "s",
) -> Callable:
    """A decorator that logs the execution time of a function.

    Optionally includes arguments, result, custom label, and time unit.
    Useful for performance diagnostics and debugging.

    :param label: Optional custom label to use instead of the function
        name.
    :param log_args: If True, logs function arguments.
    :param log_result: If True, logs the returned value of the function.
    :param log_level: Logging level to use (e.g., logging.INFO,
        logging.DEBUG).
    :param unit: Unit for measuring execution time: "s" (seconds) or
        "ms" (milliseconds).
    """

    def dec(fn: Callable):

        @wraps(fn)
        def inner(*args, **kwargs):
            if unit not in ("ms", "s"):
                raise ValueError(f"'{unit}' is an unknown unit")

            start = time.perf_counter()
            result = fn(*args, **kwargs)
            end = time.perf_counter()

            name = label or fn.__name__

            if log_args and (args or kwargs):
                args_string = [str(arg) for arg in args]
                kwargs_string = [f"{k}={v}" for k, v in kwargs.items()]
                params_string = f"{', '.join(args_string)}, {', '.join(kwargs_string)}"
            else:
                params_string = ""

            total_time = end - start
            if unit == "ms":
                total_time *= 1000
            result_string = f" and returned: \n {result}" if log_result else ""

            message = (
                f"{name}({params_string}) took {total_time:.7f}{unit}{result_string}"
            )

            logging.log(log_level, message)

            return result

        return inner

    return dec
