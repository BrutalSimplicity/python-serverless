import functools
import inspect
from cloudtools.common.cache import Empty, GlobalScopedCache, ScopeId
from typing import (
    Any, Callable,
    Optional, TypeVar, cast, overload
)

F = TypeVar("F", bound=Callable[..., Any])

_cache: Optional[GlobalScopedCache] = None

@overload
def request_cache(func: F) -> F:
    ...

def request_cache(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        global _cache
        request_cache = _cache.get()
        if not request_cache:
            return func(*args, **kwargs)

        keys = (func.__name__, *args, *sorted(kwargs.values()))
        cached_result = request_cache.get(keys)
        if isinstance(cached_result, Empty):
            result = func(*args, **kwargs)
            request_cache.save(keys, result)
            return result

        return cached_result

    return decorator

@overload
def use_request_cache(*, max_concurrent_requests: Optional[int] = None):
    ...

@overload
def use_request_cache(_func: F) -> F:
    ...

def use_request_cache(_func=None, *, max_concurrent_requests: Optional[int] = None):
    @functools.wraps(_func)
    def decorator(func):
        global _cache
        _cache = _cache if _cache else GlobalScopedCache(max_concurrent_requests)

        def _wrapper(*args, **kwargs):
            scope_id = cast(ScopeId, id(inspect.currentframe()))
            _cache.create(scope_id)
            try:
                return func(*args, **kwargs)
            finally:
                _cache.remove(scope_id)

        return _wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

def _get_global_request_cache():
    global _cache
    return _cache
