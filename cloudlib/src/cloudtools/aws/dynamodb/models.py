import base64
from dataclasses import dataclass
from typing import (Any, Callable, Generic, Mapping,
                    Optional, Sequence, Tuple, TypeVar, cast)

from cloudtools.common.json import decoder, encoder

T = TypeVar('T')

LastEvaluatedKey = Optional[Mapping[str, Any]]

DynamodbResource = Any

@dataclass
class ScanPagingParameters:
    limit: int = 10
    last_evaluated_key: LastEvaluatedKey = None

@dataclass
class PagingParameters:
    limit: int = 10
    ascending: bool = False
    last_evaluated_key: LastEvaluatedKey = None

@dataclass
class DynamodbCollection(Generic[T]):
    items: Sequence[T]
    last_evaluated_key: Optional[Mapping[str, Any]]

@dataclass
class DynamodbPaginator(DynamodbCollection[T]):
    def __init__(self, items: Sequence[T], last_evaluated_key: Optional[Mapping[str, Any]],
                 next: Callable[[LastEvaluatedKey], Tuple[Sequence[T], LastEvaluatedKey]]):
        super().__init__(items, last_evaluated_key)
        self.next_items = self.items
        self.next = next
        self.idx = 0

    def __next__(self):
        if self.next_items:
            if self.idx < len(self.next_items):
                return_value = self.next_items[self.idx]
                self.idx += 1
                return return_value

            if self.last_evaluated_key:
                self.next_items, self.last_evaluated_key = self.next(self.last_evaluated_key)
                if self.next_items:
                    return_value = self.next_items[0]
                    self.idx = 1
                    return return_value

        raise StopIteration()

    def __iter__(self):
        return self

    def to_list(self):
        return cast(DynamodbCollection[T], list(self))

def encode_paging_key(key: Optional[Mapping[str, Any]]) -> Optional[str]:
    return base64.urlsafe_b64encode(encoder(key).encode()).decode() if key else None

def decode_paging_key(key: Optional[str]) -> Optional[str]:
    return decoder(base64.urlsafe_b64decode(key.encode()).decode()) if key else None
