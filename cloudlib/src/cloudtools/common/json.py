from enum import Enum
from dataclasses import asdict, is_dataclass
from typing import Any

import simplejson

from cloudtools.common.utils import isnamedtupleinstance

def encoder_handler(obj):
    if is_dataclass(obj):
        return asdict(obj)
    if isnamedtupleinstance(obj):
        return obj._asdict()
    if isinstance(obj, Enum):
        return obj.value

    return str(obj)

def encoder(value: Any) -> str:
    """Encodes a value as json

    Args:
        value: object to be converted to json

    Result:
        object as json
    """
    return simplejson.dumps(value, separators=(',', ':'), default=encoder_handler)


def decoder(value: str) -> Any:
    """Decodes a json string into an object

    Args:
        value: string to be converted to object

    Result:
        object: object decoded from json
    """
    return simplejson.loads(value)
