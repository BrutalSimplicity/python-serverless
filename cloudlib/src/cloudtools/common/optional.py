
from typing import Any, Generic, Mapping, Sequence, TypeVar, cast

T = TypeVar('T')


class OptionalHandler(Generic[T]):
    def __init__(self, obj: T):
        self._src = obj

    def value(self, default=None) -> Any:
        return self._src or default

    def __getitem__(self, key):
        if not self._src:
            return OptionalHandler(None)

        try:
            return OptionalHandler(cast(Mapping, self._src).get(key))
        except AttributeError:
            try:
                return OptionalHandler(cast(Sequence, self._src)[key])
            except Exception:
                return OptionalHandler(None)

    def __getattr__(self, name: str):
        try:
            return OptionalHandler(getattr(self._src, name))
        except AttributeError:
            return OptionalHandler(None)

    def __bool__(self):
        return bool(self._src)
