from collections import OrderedDict
from functools import _make_key, wraps
from time import time
from typing import Callable, Optional


def cache(
    max_size: Optional[int] = None,
    ttl: Optional[float] = None,
    typed: bool = False,
) -> Callable:
    """A decorator that caches function results based on arguments, with
    optional TTL and LRU-style eviction.

    :param max_size: Maximum number of items to store in the cache. When
        exceeded, the least recently used item is evicted. If None, the
        cache grows unbounded.
    :param ttl: Optional time-to-live in seconds. If set, cached items
        expire after this duration and are recomputed.
    :param typed: If True, function arguments of different types will be
        cached separately (e.g., 1 and 1.0 are distinct).
    """

    def dec(fn: Callable):
        cache_dict: OrderedDict = OrderedDict()

        def is_outdated(key):
            return ttl and key in cache_dict and (time() - cache_dict[key][0]) > ttl

        @wraps(fn)
        def inner(*args, **kwargs):
            if is_outdated(key := _make_key(args, kwargs, typed)):
                cache_dict.pop(key)
            if key not in cache_dict:
                result = fn(*args, **kwargs)

                if max_size and max_size <= len(cache_dict):
                    cache_dict.popitem(last=False)
                if ttl:
                    result = (time(), result)
                cache_dict[key] = result

            return cache_dict[key] if not ttl else cache_dict[key][1]

        return inner

    return dec
