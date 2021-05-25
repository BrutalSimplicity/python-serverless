from typing import Dict, Generic, Iterable, List, Set, TypeVar
from swawesomo.common.errors import BaseFormattedError
from swawesomo.common.pipeline import Pipeline as _
from .models import Node

T = TypeVar('T')

class DependencyDoesNotExistError(BaseFormattedError):
    fmt = 'The dependency ({}) does not exist.'

    def __init__(self, key: str):
        super().__init__(key)
        self.status_code = 401

class MissingDependenciesError(BaseFormattedError):
    fmt = 'Missing dependencies: {}'

    def __init__(self, keys: List[str]):
        super().__init__(keys)
        self.status_code = 401

class DependencyCycleError(BaseFormattedError):
    fmt = 'Dependency cycle detected: {} -> {}'

    def __init__(self, key, dependency):
        super().__init__(key, dependency)
        self.status_code = 401

class DependencyLoopError(BaseFormattedError):
    fmt = 'Dependency loop detected. A node cannot list itself as a dependency.'

    def __init__(self):
        super().__init__()
        self.status_code = 401

class ExistingDependentsError(BaseFormattedError):
    fmt = 'Existing dependents: {}. You must remove the existing dependents first.'

    def __init__(self, keys: List[str]):
        super().__init__(keys)
        self.status_code = 401

class _Node(Generic[T]):
    def __init__(self, key: str, data: T):
        self._dependencies: Dict[str, _Node[T]] = {}
        self._dependents: Dict[str, _Node[T]] = {}
        self._data: T = data
        self._key: str = key
        self._max_path_length: int = 0

    def add_dependency(self, node: "_Node[T]"):
        # We must ensure the max path length is always
        # the length of the greatest dependency node's path + 1.
        # This is what maintains the dependency order
        if node._max_path_length + 1 > self._max_path_length:
            self._max_path_length = node._max_path_length + 1
        self._dependencies[node.key] = node
        node._dependents[self.key] = self

    def remove_dependency(self, key: str):
        if parent := self._dependencies.get(key):
            del self._dependencies[key]
            del parent._dependents[self.key]
        
        self._max_path_length = max([node._max_path_length for node in self.dependencies], default=0)

    def remove_dependent(self, key: str):
        if child := self._dependents.get(key):
            del self._dependents[key]
            del child._dependencies[self.key]

    def has_dependency(self, key: str):
        return key in self._dependencies

    @property
    def data(self):
        return self._data

    @property
    def dependencies(self):
        return tuple(self._dependencies.values())

    @property
    def dependents(self):
        return tuple(self._dependents.values())

    @property
    def dependencies_keys(self):
        return list(self._dependencies.keys())
    
    @property
    def dependents_keys(self):
        return list(self._dependents.keys())

    @property
    def max_path_length(self):
        return self._max_path_length

    @property
    def key(self):
        return self._key
        
    @property
    def is_root(self):
        return not self._dependencies

    @property
    def is_stem(self):
        return not (self.is_root and self.is_leaf)

    @property
    def is_leaf(self):
        return not self._dependents

class DependencyGraph(Generic[T]):

    def __init__(self):
        self._nodes: Dict[str, _Node[T]] = {}

    def add_node(self, key: str, data: T, dependencies: List[str]):
        if key in self._nodes:
            return self.update_node(key, data, dependencies)
        self._validate_if_dependencies_exist(dependencies)
        new_node = _Node[T](key, data)
        if dependencies:
            dependencies = list(set(dependencies))
            for dependency in dependencies:
                node = self._nodes[dependency]
                new_node.add_dependency(node)
                
        self._nodes[key] = new_node

    def update_node(self, key: str, data: T, dependencies: List[str]):
        self._validate_if_key_exists(key)
        self._validate_if_dependencies_exist(dependencies)
        self._validate_no_cycles(key, dependencies)
        node = self._nodes[key]
        new = set(dependencies)
        existing = set(node.dependencies_keys)
        self._update_node_dependency_linkages(node, existing, new)

    def remove_node(self, key: str):
        self._validate_if_key_exists(key)
        self._validate_is_leaf(key)
        node = self._nodes[key]

        # remove the linkage between the node and its dependencies
        for dependency in node.dependencies:
            dependency.remove_dependent(key)
        
        del self._nodes[key]
        
    def generate_evaluation_order(self):
        nodes = [Node(node.key, node.data, node.max_path_length + 1) for node in self._nodes.values()]
        return sorted(nodes, key=lambda node: node.order)

    def _update_node_dependency_linkages(self, node: _Node[T], existing_dependencies: Set[str], new_dependencies: Set[str]):
        dependencies_to_remove = existing_dependencies - new_dependencies
        dependencies_to_add = new_dependencies - existing_dependencies

        for dependency in dependencies_to_remove:
            node.remove_dependency(dependency)

        for dependency in dependencies_to_add:
            node.add_dependency(self._nodes[dependency])

    def _validate_is_leaf(self, key: str):
        if not self._nodes[key].is_leaf:
            dependents = self._nodes[key].dependents_keys
            raise ExistingDependentsError(dependents)

    def _validate_if_key_exists(self, key: str):
        if key not in self._nodes:
            raise DependencyDoesNotExistError(key)

    def _validate_if_dependencies_exist(self, dependencies: List[str]):
        missing_dependencies = [dep for dep in dependencies if dep not in self._nodes]
        if missing_dependencies:
            raise MissingDependenciesError(missing_dependencies)

    def _validate_no_cycles(self, key: str, dependencies: List[str]):
        # For each dependency we can determine a cycle by walking to the root
        # of the graph. A cycle occurs if we visit a node with the same key
        def recurse(key, nodes: Iterable[_Node[T]], dependency: str):
            if not nodes:
                return
            for node in nodes:
                if node.key == key:
                    raise DependencyCycleError(key, dependency)
                recurse(key, node.dependencies, dependency)
        
        for dependency in dependencies:
            node = self._nodes[dependency]
            if key == node.key:
                raise DependencyLoopError()
            recurse(key, node.dependencies, dependency)
