from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass
class Node(Generic[T]):
    key: str
    data: T
    order: int
