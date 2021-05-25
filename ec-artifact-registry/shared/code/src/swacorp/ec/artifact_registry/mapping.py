from typing import Any, List, Mapping, Type, TypeVar
from swawesomo.common.models.mapping import from_dict as internal_from_dict
from dacite.config import Config

config = Config(type_hooks={List[str]: lambda v: [v] if isinstance(v, str) else v})

T = TypeVar("T")


def from_dict(data_class: Type[T], data: Mapping[str, Any]) -> T:
    return internal_from_dict(data_class, data, config)
