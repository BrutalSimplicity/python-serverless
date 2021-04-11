import functools
import inspect
import logging
import traceback
from logging import Logger
from time import perf_counter
from typing import Any, Callable, TypeVar, overload

from cloudtools.common.logging.logging_context import (_get_cache,
                                                      get_logging_context)
from cloudtools.common.utils import convert_to_dict, generate_timestamp

F = TypeVar("F", bound=Callable[..., Any])

@overload
def log_it(_func: F) -> F:
    ...

@overload
def log_it(*, event: str = None, message: str = None,
           level: int = logging.getLogger().level, timeit: bool = False,
           logger: Logger = logging.getLogger(), only_on_error: bool = False) -> Callable[[F], F]:
    ...

def _get_func_parameters(func):
    try:
        return str(inspect.signature(func))
    except Exception:
        return None

def _try_get_dict(data):
    try:
        return convert_to_dict(data)
    except Exception:
        return data

def _log_results(func, args, kwargs, result, event, message, level, timeit,
                 logger, duration):
    actual_event = event or func.__name__
    actual_message = message or f'{func.__name__} was called'
    event_details = {
        'event': actual_event,
        'message': actual_message,
        'level': logging.getLevelName(level),
        'caller': func.__name__,
        'parameters': _get_func_parameters(func),
        'input': {
            'args': tuple([_try_get_dict(arg) for arg in args]),
            'kwargs': {key: _try_get_dict(value) for key, value in kwargs.items()}
        },
        'output': _try_get_dict(result),
        'timestamp': generate_timestamp()
    }

    if timeit:
        event_details['duration_secs'] = duration

    if _get_cache():
        context = get_logging_context()
        if context._context:
            event_details['context'] = {**context._context}

    logger.log(level, event_details)

def _log_error(func, args, kwargs, err, logger):
    # Only log the exception if you are the first
    # to handle it - else - just pass it along.
    # This prevents logging the same exception
    # multiple times.
    if not hasattr(err, '_already_handled'):
        try:
            setattr(err, '_already_handled', True)
            event_details = {
                'event': type(err).__name__,
                'message': err,
                'level': 'ERROR',
                'stack_trace': traceback.format_exc(),
                'caller': func.__name__,
                'parameters': _get_func_parameters(func),
                'input': {
                    'args': [_try_get_dict(arg) for arg in args],
                    'kwargs': [_try_get_dict(kwarg) for kwarg in kwargs]
                },
                'timestamp': generate_timestamp()
            }

            if _get_cache():
                context = get_logging_context()
                if context._context:
                    event_details['context'] = {**context._context}

            logger.log(logging.ERROR, event_details)
        except Exception as ex:
            logger.log(logging.ERROR, {
                'event': type(err).__name__,
                'caller': func.__name__,
                'message': str(err),
                'level': 'ERROR_IN_LOGGER',
                'additionalError': str(ex),
                'args': args,
                'kwargs': kwargs,
            })

def log_it(_func=None, *, event: str = None, message: str = None,
           level: int = logging.getLogger().level, timeit: bool = False,
           logger: Logger = logging.getLogger(), only_on_error: bool = False) -> Any:
    '''Logs the results of the decorated function.

    Will log the results of a function as a dictionary so that it can easily
    be converted to json for structured logging. The json conversion happens
    automatically as a handler is automatically added to the default logger
    when importing this module.

    This attempts to be a universal logger by logging both the input and output
    of a function. It should automatically convert most basic types, but will
    log the string conversion of an object if conversion is not possible.

    Args:
        event: Event name to log. Defaults to the decorated function name.
        message: Message to log. Defaults to '{func name} was called'.
        level: Event level. Defaults to default logger level.
        timeit: Whether to include timing metrics. Defaults to false.
        logger: The `logging.Logger` to use. Defaults to root logger.
        only_on_error: Whether to only log errors. Defaults to false.

    Returns:
        Result of the decorated function

    Examples:
    ```python
    @log_it(level=logging.DEBUG)
    def some_concerning_function(a: int, b: str):
        result = {'a': a, 'b': b}
        return result
    ```
    '''
    @functools.wraps(_func)
    def logit_decorator(func):

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                start = perf_counter()
                result = func(*args, **kwargs)
                stop = perf_counter()

                if only_on_error:
                    return result

                _log_results(func, args, kwargs, result, event,
                             message, level, timeit, logger,
                             stop - start)

                return result

            except Exception as err:
                _log_error(func, args, kwargs, err, logger)
                raise err

        return _wrapper

    if _func is None:
        return logit_decorator
    else:
        return logit_decorator(_func)
