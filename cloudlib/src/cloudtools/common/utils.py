# type: noqa
from copy import copy
from dataclasses import asdict
from datetime import datetime
import functools
import logging
import time
from typing import (
    Any, Callable, Dict, List, Mapping, NamedTuple, Optional, Tuple,
    Type, TypeVar, Union, cast, overload
)

F = TypeVar("F", bound=Callable[..., Any])

class DictConversionError(Exception):
    pass

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def generate_timestamp() -> str:
    return datetime.utcnow().isoformat(timespec='microseconds') + 'Z'

def pluck(obj, *args) -> Tuple[Optional[Any], ...]:
    return tuple([obj[key] if key in obj else None for key in args])

def filter_empty_properties(mapping: Mapping[Any, Any]) -> Dict[Any, Any]:
    return {k: v for k, v in mapping.items() if v}

def response_asdict(fn=None):
    @functools.wraps(fn)
    def _wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        result = convert_to_dict(result)
        return result
    return _wrapper

def isnamedtupleinstance(x) -> bool:
    t = type(x)
    b = t.__bases__
    if (len(b) != 1
       or b[0] != tuple):
        return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)

def is_dataclass_instance(obj):
    return hasattr(type(obj), '__dataclass_fields__')

def convert_to_dict(data) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    if data is None:
        return data
    if isinstance(data, dict):
        return cast(Dict[str, Any], dict(data))
    if is_dataclass_instance(data):
        return asdict(data)
    if isnamedtupleinstance(data):
        return cast(NamedTuple, data)._asdict()
    if isinstance(data, list) or isinstance(data, tuple):
        return cast(List[Dict[str, Any]], [convert_to_dict(item) for item in data])
    raise DictConversionError(f'Failed to convert to dictionary: {data}')

@overload
def retry(_func: F) -> F:
    ...

@overload
def retry(*, max_retries: int = 3, delay_seconds: int = 5,
          allowable_exceptions: List[Type[Exception]] = []) -> Callable[[F], F]:
    ...

def retry(fn=None, *, max_retries=3, delay_seconds=5, allowable_exceptions: List[Type[Exception]] = []):

    @functools.wraps(fn)
    def retry_decorator(_fn):

        @functools.wraps(_fn)
        def _wrapper(*args, **kwargs):
            num_tries = 1
            while True:
                try:
                    return _fn(*args, **kwargs)
                except Exception as ex:
                    if num_tries >= max_retries:
                        raise ex
                    if not allowable_exceptions or any([exc == type(ex) for exc in allowable_exceptions]):
                        time.sleep(delay_seconds)
                        LOGGER.warning(f'Calling {_fn.__name__}, Number of tries: {num_tries}')
                        LOGGER.warning(f'{ex}')
                        num_tries += 1
                        continue
                    raise ex

        return _wrapper

    if fn:
        return retry_decorator(fn)
    else:
        return retry_decorator

def walk_keys(mappings: Union[Mapping[str, Any], List[Mapping[str, Any]]],
              apply_fn: Callable[[str, Any], Optional[Tuple[Optional[str], Any]]]
              ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    if isinstance(mappings, Mapping):
        new_mappings = {}
        for key, value in mappings.items():
            new_value = copy(value)
            item = apply_fn(key, new_value)
            if not item:
                continue

            next_key = item[0] if item[0] else key
            next_value = item[1] if item[1] else value
            if isinstance(next_value, Mapping) or isinstance(next_value, List):
                new_mappings[next_key] = walk_keys(next_value, apply_fn)
            else:
                new_mappings[next_key] = next_value

        return new_mappings

    elif isinstance(mappings, List):
        new_mappings = []
        for value in mappings:
            new_mappings.append(walk_keys(value, apply_fn))

        return new_mappings

    return mappings
