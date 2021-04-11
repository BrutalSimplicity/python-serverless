import inspect
from time import perf_counter
from typing import Any, Dict, NewType, Optional, Protocol, Union, cast
from threading import Lock

ScopeId = NewType('ScopeId', int)

class SupportsHash(Protocol):
    def __hash__(self) -> int:
        ...

class Empty:
    pass

class ScopedCacheEntry:
    def __init__(self, item: Any):
        self.item = item
        self.created_at = perf_counter()
        self.last_accessed = perf_counter()

class ScopedCache:
    def __init__(self):
        self.cache: Dict[SupportsHash, ScopedCacheEntry] = {}
        self.created_at = perf_counter()
        self.last_accessed = perf_counter()

    def get(self, key: SupportsHash) -> Union[Empty, Any]:
        if key not in self.cache:
            return Empty()
        entry = self.cache[key]
        entry.last_accessed = perf_counter()
        return entry.item

    def save(self, key: SupportsHash, item: Any):
        entry = self.cache[key] if key in self.cache else ScopedCacheEntry(item)
        entry.last_accessed = perf_counter()
        self.cache[key] = entry

class GlobalScopedCache:

    def __init__(self, max_requests: Optional[int] = None):
        self._cache: Dict[ScopeId, ScopedCache] = {}
        self._max_requests = max_requests
        self._lock = Lock()

    def get(self) -> Optional[ScopedCache]:
        frames = inspect.getouterframes(inspect.currentframe())
        request_id = None
        for fi in frames:
            frame_id = cast(ScopeId, id(fi.frame))
            if frame_id in self._cache:
                request_id = frame_id
                break

        if request_id:
            with self._lock:
                if request_id in self._cache:
                    entry = self._cache[request_id]
                    entry.last_accessed = perf_counter()
                    return entry

        return None

    def create(self, request_id: ScopeId):
        request_cache = ScopedCache()
        with self._lock:
            self._cache[request_id] = request_cache
        self._remove_oldest_scoped_caches()

    def remove(self, id: ScopeId):
        with self._lock:
            if id in self._cache:
                del self._cache[id]

    def _remove_oldest_scoped_caches(self):
        if self._max_requests and len(self._cache) > self._max_requests:
            items_by_oldest = sorted(self._cache.items(), key=lambda pair: pair[1].last_accessed)
            num_to_remove = len(self._cache) - self._max_requests
            for i in range(num_to_remove):
                item = items_by_oldest[i]
                id = item[0]
                self.remove(id)

    def __bool__(self):
        return bool(self._cache)
