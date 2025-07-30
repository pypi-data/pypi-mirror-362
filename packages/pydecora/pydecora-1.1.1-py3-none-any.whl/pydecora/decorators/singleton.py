from typing import Any, Type
from functools import wraps

def singleton(cls: Type[Any]):
    """A class decorator that ensures only one instance of the decorated class
    is ever created.
    
    All subsequent instantiations return the same cached instance.
    
    :param cls: The class to decorate.
    """
    instance = None

    def inner(*args, **kwargs):

        nonlocal instance

        if not instance:
            instance = cls(*args, **kwargs)

        return instance
    
    return inner
