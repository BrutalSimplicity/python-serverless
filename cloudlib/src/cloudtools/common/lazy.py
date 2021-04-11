
from typing import Any, Callable, Generic, List, Mapping, Optional, TypeVar, Union, cast

T = TypeVar('T')

class Lazy(Generic[T]):
    def __init__(self, value_fn: Callable[[], T]):
        self.value_fn = value_fn
        self.resolve_value: Optional[T] = None

    @property
    def value(self) -> T:
        return self._get_value()

    def cast(self) -> T:
        return cast(Any, self)

    def __getattr__(self, name: str):
        return self._get_value().__getattribute__(name)

    def __getitem__(self, key):
        return cast(Union[Mapping, List], self._get_value())[key]

    def __call__(self):
        return self._get_value()

    def _get_value(self):
        if self.resolve_value:
            return self.resolve_value
        self.resolve_value = self.value_fn()
        return self.resolve_value
