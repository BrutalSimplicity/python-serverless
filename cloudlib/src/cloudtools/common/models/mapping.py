from enum import Enum
from typing import Any, Mapping, Optional, Type, TypeVar

from dacite import from_dict as internal_from_dict
from dacite.config import Config

default_config = Config(cast=[Enum])

T = TypeVar('T')
def from_dict(data_class: Type[T], data: Mapping[str, Any], config: Optional[Config] = None) -> T:
    final_config = default_config
    if config:
        final_config = config
        final_config.cast = [*default_config.cast, *config.cast]
    return internal_from_dict(data_class, dict(data), final_config)
