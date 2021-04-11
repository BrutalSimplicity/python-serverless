# type: noqa
import functools
import inspect
from typing import Any, Callable, Dict, Optional, TypeVar, cast, overload

from cloudtools.common.cache import Empty, GlobalScopedCache, ScopeId

CONTEXT_KEY = 'context'
CONTEXT_ERROR = ' '.join([
    'Logging context was not found. Check that you are using the use_logging_context decorator,',
    'and that you are within its scope.'
])


class MissingContextError(Exception):
    pass

class LoggingContext:
    '''A logging context for shared logging metadata.
    '''
    def __init__(self):
        self._context: Dict[str, Any] = {}

    def add_metadata(self, key: str, value: Any):
        '''Add metadata to the logging context.

        Args:
            key: Metadata key.
            value: Metadata value.
        '''
        self._context[key] = value
        return self

    def remove_metadata(self, key: str):
        '''Remove metadata from the logging context.

        Args:
            key: Key to be removed.
        '''
        if key in self._context:
            del self._context[key]
        return self

    def clear(self):
        '''Clears all metadata.

        Caution: This clears all metadata and will affect all subsequent
        logs sharing the same context.
        '''
        self._context = {}

F = TypeVar("F", bound=Callable[..., Any])

_cache: Optional[GlobalScopedCache] = None
def _get_cache():
    global _cache
    return _cache

@overload
def use_logging_context(func: F) -> F:
    ...

def use_logging_context(func):
    '''Creates a logging context that is shared by all logs captured by the `@log_it` decorator.

    The logging context can be used to share common metadata between logs captured within this context.
    The context is an cached object that stays within "context" for the duration of the decorated
    function call. This means that subsequent `@log_it` calls that happen further down the call chain
    will still share the same context.

    Examples:
    ```python
        @log_it(level=logging.INFO)
        def fetch_data(params):
            return {'data': True}

        @use_logging_context
        def lambda_handler(event, context):
            get_logging_context()
            .add_metadata('module', 'EventHandler')
            .add_metadata('uuid', event['detail']['uuid'])
            .add_metadata('correlation_id', event['detail']['correlation_id'])

            return fetch_data(event['detail'])
    ```
    '''
    global _cache
    _cache = _cache if _cache else GlobalScopedCache()

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        scope_id = cast(ScopeId, id(inspect.currentframe()))
        _cache.create(scope_id)
        context_cache = _cache.get()
        context_cache.save(CONTEXT_KEY, LoggingContext())
        try:
            return func(*args, **kwargs)
        finally:
            _cache.remove(scope_id)

    return decorator

def get_logging_context() -> Optional[LoggingContext]:
    '''Gets the logging context that is within scope.

    This method ensures that in a concurrent or multithreaded environment, any
    logging context returned will be appropriate for its scope.

    Raises:
        MissingContextError: If the context has not been created due to a
                             missing call to `use_logging_context`

    Returns:
        Returns a `LoggingContext` object
    '''
    global _cache
    context_cache = _cache.get()
    if context_cache:
        context = context_cache.get(CONTEXT_KEY)
        if isinstance(context, Empty):
            return None
        return context
    raise MissingContextError(CONTEXT_ERROR)
