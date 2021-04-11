from dataclasses import dataclass, is_dataclass, asdict
from typing import Any, Mapping, Optional, Type, TypeVar, cast
from cloudtools.common.json import encoder, decoder
from dacite.config import Config
from .mapping import from_dict

class InvalidEventModelType(Exception):
    pass

T = TypeVar('T', bound="BaseModel")

@dataclass
class BaseModel(object):

    def to_dict(self):
        if is_dataclass(self):
            return asdict(self)
        raise InvalidEventModelType('Only instances of a dataclass are valid for this method')

    def to_json(self):
        return encoder(self)

    @classmethod
    def from_dict(cls: Type[T], data: Mapping[str, Any], config: Optional[Config] = None) -> T:
        return from_dict(cls, dict(data), config)

    @classmethod
    def from_json(cls: Type[T], json: str, config: Optional[Config] = None) -> T:
        data = decoder(json)
        return cast(Any, cls.from_dict(data, config))
