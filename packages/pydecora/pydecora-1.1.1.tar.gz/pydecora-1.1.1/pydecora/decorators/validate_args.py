import inspect
import logging
from typing import Any, Callable, Iterable, Type, get_origin, Union, get_args
from functools import wraps

def validate_args(
    check_return: bool = False,
    raise_exception: Type[Exception] = TypeError,
    exclusions: Iterable[str] = (),
    strict: bool = True,
    warn_only: bool = False,
) -> Callable:

    """Decorator that validates function arguments (and optionally return
    values) against their type hints.

    Supports generic types like List, Dict, Union, Optional, and nested
    combinations. Can raise an exception or log a warning on validation
    failure. Also supports skipping specific argument names and
    enforcing strict type checks.

    :param check_return: If True, also validate the function's return
        value against its return annotation.
    :param raise_exception: The exception type to raise on validation
        failure.
    :param exclusions: Iterable of argument names to exclude from
        validation (e.g., 'self').
    :param strict: If True, uses exact type match (type(x) is T). If
        False, allows subclasses (isinstance(x, T)).
    :param warn_only: If True, logs a warning instead of raising an
        exception on validation failure.
    """

    def dec(fn: Callable):

        def validate(arg: Any, type_hint: Type[Any]) -> bool:

            if not type_hint or type_hint == Any:
                return True

            origin = get_origin(type_hint)
            args = get_args(type_hint)

            if origin is tuple and len(args) > 1 and args[1] is not Ellipsis:
                if len(args) != len(arg):
                    return False
                for pair in zip(arg, args):
                    if not validate(pair[0], pair[1]):
                        return False

            elif origin in (list, set, tuple):
                if args:
                    for elem in arg:
                        if not validate(elem, args[0]):
                            return False

            elif origin is Union:
                return any(validate(arg, option) for option in args)

            elif origin is dict:
                if args:
                    if len(args) != 2:
                        return False
                    for key, value in arg.items():
                        if not validate(key, args[0]):
                            return False
                        if not validate(value, args[1]):
                            return False

            return isinstance(arg, origin or type_hint) if not strict else type(arg) is (origin or type_hint)

        def raise_error(name: str, type_hint: Type[Any], value: Any) -> None:
            if not warn_only:
                raise raise_exception(f"{name} is not the expected type {type_hint.__name__}")
            logging.warning(f"{name} failed type check: expected {type_hint.__name__}, got {type(value).__name__}")


        @wraps(fn)
        def inner(*args, **kwargs):

            sign = inspect.signature(fn)
            bound = sign.bind(*args, **kwargs)
            bound.apply_defaults()
            for name, value in bound.arguments.items():

                if name in exclusions:
                    continue

                if (annot := sign.parameters[name].annotation) is inspect._empty:
                    annot = Any

                if not validate(value, annot):
                    raise_error(name, annot, value)

            result = fn(*args, **kwargs)

            if check_return and (annot := sign.return_annotation) is not inspect._empty:
                if not validate(result, annot):
                    raise_error("return value", annot, result)

            return result

        return inner

    return dec
