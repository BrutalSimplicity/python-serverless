from typing import (
    Any, Callable, Dict, Generator, Generic, Iterator, List, Optional,
    Protocol, Tuple, Type, TypeVar, Iterable, cast, overload
)

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

class SupportsLessThan(Protocol):
    def __lt__(self, __other: Any) -> bool:
        ...

class SupportsHash(Protocol):
    def __hash__(self) -> int:
        ...

class PipelineError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Pipeline(Generic[T], Iterator):

    def __init__(self, iterable: Iterable[T]):
        self._pipeline: Generator[Any, None, None] = (item for item in iterable)

    def map(self, selector: Callable[[T], U]) -> "Pipeline[U]":
        self._pipeline = (selector(item) for item in self._pipeline)
        return Pipeline(self._pipeline)

    def mapopt(self, selector: Callable[[T], Optional[U]]) -> "Pipeline[U]":
        def inner(pipeline):
            for item in pipeline:
                new_item = selector(item)
                if new_item:
                    yield new_item
        self._pipeline = inner(self._pipeline)
        return Pipeline(self._pipeline)

    def flat_map(self, selector: Callable[[T], Iterable[U]]) -> "Pipeline[U]":
        self._pipeline = (item for group in (selector(item)
                                             for item in self._pipeline) for item in group)

        return Pipeline(self._pipeline)

    def filter(self, predicate: Callable[[T], Any]) -> "Pipeline[T]":
        self._pipeline = (item for item in self._pipeline if predicate(item))
        return Pipeline(self._pipeline)

    def head(self) -> T:
        for item in self._pipeline:
            return item
        raise PipelineError('head of empty generator')

    def headopt(self) -> Optional[T]:
        first = None
        for item in self._pipeline:
            first = item
            return first

    def tail(self) -> T:
        tail = None
        for item in self._pipeline:
            tail = item
        if not tail:
            raise PipelineError('tail of empty generator')
        return tail

    def tailopt(self) -> Optional[T]:
        last = None
        for item in self._pipeline:
            last = item
        return last

    def order_by(self, selector: Callable[[T], SupportsLessThan],
                 ascending: bool = True) -> "Pipeline[T]":
        items = sorted(self._pipeline, key=selector, reverse=not ascending)
        self._pipeline = (item for item in items)

        return Pipeline(self._pipeline)

    def group_by(self, selector: Callable[[T], U]) -> "Pipeline[Tuple[U, List[T]]]":
        mapping = {}
        for item in self._pipeline:
            key = selector(item)
            if key in mapping:
                mapping[key].append(item)
            else:
                mapping[key] = [item]

        self._pipeline = ((k, v) for k, v in mapping.items())

        return Pipeline(self._pipeline)

    def tap(self, applicator: Callable[[T], Any]):
        def apply(item, applicator):
            applicator(item)
            return item

        self._pipeline = (apply(item, applicator) for item in self._pipeline)

        return Pipeline[T](self._pipeline)

    def take(self, count: int):
        def take_pipeline(iterator):
            curr_count = 0
            for item in iterator:
                if curr_count >= count:
                    break
                yield item
                curr_count += 1

        self._pipeline = take_pipeline(self._pipeline)

        return Pipeline(self._pipeline)

    def batch(self, count: int) -> "Pipeline[List[T]]":

        def batch_pipeline(iterator):
            buffer = []
            for item in iterator:
                buffer.append(item)
                if len(buffer) >= count:
                    yield buffer
                    buffer = []

            if len(buffer) > 0:
                yield buffer

        self._pipeline = batch_pipeline(self._pipeline)

        return Pipeline(self._pipeline)

    def collect(self, applicator: Callable[[Iterable[T]], U]) -> "Pipeline[U]":
        result = applicator(self._pipeline)
        self._pipeline = (item for item in ([result] if result else []))

        return Pipeline(self._pipeline)

    def consume(self, applicator: Callable[[Iterable[T]], U]) -> U:
        result = applicator(self._pipeline)

        return result

    def reduce(self, reducingFn: Callable[[U, T], U], seed: U = None) -> U:
        iterator = iter(self._pipeline)
        acc: Any = seed if seed else next(iterator)
        if seed:
            for item in self._pipeline:
                acc = reducingFn(acc, item)
        else:
            for item in iterator:
                acc = reducingFn(acc, item)

        return acc

    def join(self, right: Iterable[U],
             selector_left: Callable[[T], SupportsHash],
             selector_right: Callable[[U], SupportsHash],
             result_selector: Callable[[T, U], V]) -> "Pipeline[V]":

        right_frequency_map = {}
        for val in right:
            key = selector_right(val)
            pair = right_frequency_map.get(key)
            if pair:
                right_frequency_map[key] = (1 + pair[0], pair[1])
            else:
                right_frequency_map[key] = (1, val)

        def generator(iterator):
            for left_item in iterator:
                left_val = selector_left(left_item)
                pair = right_frequency_map.get(left_val)
                if pair:
                    freq, right_item = pair[0], pair[1]
                    for _ in range(freq):
                        yield result_selector(left_item, right_item)

        self._pipeline = generator(self._pipeline)

        return Pipeline[V](self._pipeline)

    def group_join(self, right: Iterable[U],
             selector_left: Callable[[T], SupportsHash],
             selector_right: Callable[[U], SupportsHash],
             result_selector: Callable[[T, Iterable[U]], V]) -> "Pipeline[V]":
        right_group: Dict[SupportsHash, List[U]] = {}
        for val in right:
            key = selector_right(val)
            group = right_group.get(key)
            if group:
                group.append(val)
            else:
                right_group[key] = [val]

        def generator(iterator):
            for left_item in iterator:
                left_val = selector_left(left_item)
                group = right_group.get(left_val, [])
                yield result_selector(left_item, group)

        self._pipeline = generator(self._pipeline)

        return Pipeline[V](self._pipeline)

    def distinct(self, selector: Callable[[T], SupportsHash]):
        self._pipeline = (item for item in {selector(item): item for item in self._pipeline}.values())
        return Pipeline[T](self._pipeline)

    def concat(self, items: Iterable[U]) -> "Pipeline[U]":

        def generator(pipeline):
            for item in pipeline:
                yield item
            for item in items:
                yield item

        self._pipeline = generator(self._pipeline)

        return Pipeline[U](self._pipeline)

    def cast(self, type: Type[U]) -> "Pipeline[U]":
        self._pipeline = (cast(type, item) for item in self._pipeline)
        return Pipeline[U](self._pipeline)

    def to_list(self) -> List[T]:
        return self.consume(list)

    def __next__(self) -> T:
        return self._pipeline.__next__()

    def __iter__(self):
        return self

def identity(x: T) -> T:
    return x

A1 = TypeVar('A1')
A2 = TypeVar('A2')
A3 = TypeVar('A3')
A4 = TypeVar('A4')
A5 = TypeVar('A5')
A6 = TypeVar('A6')
A7 = TypeVar('A7')

@overload
def compose(fn1: Callable[[A1], A2], fn2: Callable[[A2], A3]) -> Callable[[A1], A3]:
    ...

@overload
def compose(fn1: Callable[[A1], A2], fn2: Callable[[A2], A3],
            fn3: Callable[[A3], A4]) -> Callable[[A1], A4]:
    ...

@overload
def compose(fn1: Callable[[A1], A2], fn2: Callable[[A2], A3],
            fn3: Callable[[A3], A4], fn4: Callable[[A4], A5]) -> Callable[[A1], A5]:
    ...

@overload
def compose(fn1: Callable[[A1], A2], fn2: Callable[[A2], A3],
            fn3: Callable[[A3], A4], fn4: Callable[[A4], A5],
            fn5: Callable[[A5], A6]) -> Callable[[A1], A6]:
    ...

@overload
def compose(fn1: Callable[[A1], A2], fn2: Callable[[A2], A3],
            fn3: Callable[[A3], A4], fn4: Callable[[A4], A5],
            fn5: Callable[[A5], A6], fn6: Callable[[A6], A7]) -> Callable[[A1], A7]:
    ...

@overload
def compose(fn1: Callable[[A1], A2], fn2: Callable[[A2], A3],
            fn3: Callable[[A3], A4], fn4: Callable[[A4], A5],
            fn5: Callable[[A5], A6], fn6: Callable[[A6], Any],
            *fns: Callable[[Any], Any]) -> Callable[[A1], Any]:
    ...

def compose(*fns):
    return (
        Pipeline(reversed(fns))
        .reduce(lambda fn, next: lambda arg: fn(next(arg)))
    )

def fallback(*fns: Callable[..., Any]) -> Callable[..., Any]:
    def fallback_fn(*args, **kwargs):
        for fn in fns:
            result = fn(*args, **kwargs)
            if result:
                return result
        return False

    return fallback_fn
