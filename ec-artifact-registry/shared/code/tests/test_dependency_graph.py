import unittest
from dataclasses import asdict

import pytest
from swacorp.ec.artifact_registry.dependency_graph.graph import (
    DependencyCycleError, DependencyDoesNotExistError, DependencyGraph,
    DependencyLoopError, ExistingDependentsError, MissingDependenciesError)


class DependencyGraphTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_should_add_node(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        nodes = graph.generate_evaluation_order()

        actual = [asdict(x) for x in nodes]
        expected = [
            {
                'key': 'a',
                'data': 'a',
                'order': 1
            }
        ]

        self.assertCountEqual(actual, expected)

    def test_should_add_sequential_nodes(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        graph.add_node('b', 'b', ['a'])
        graph.add_node('c', 'c', ['b'])
        nodes = graph.generate_evaluation_order()

        actual = [asdict(x) for x in nodes]
        expected = [
            {
                'key': 'a',
                'data': 'a',
                'order': 1
            },
            {
                'key': 'b',
                'data': 'b',
                'order': 2
            },
            {
                'key': 'c',
                'data': 'c',
                'order': 3
            },
        ]

        self.assertCountEqual(actual, expected)

    def test_should_add_nodes_at_multiple_depths(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        graph.add_node('b', 'b', ['a'])
        graph.add_node('c', 'c', ['b'])
        graph.add_node('d', 'd', ['a', 'b'])
        graph.add_node('e', 'e', ['c'])
        graph.add_node('f', 'f', ['a', 'b', 'c', 'd', 'e'])
        nodes = graph.generate_evaluation_order()

        actual = [asdict(x) for x in nodes]
        expected = [
            {
                'key': 'a',
                'data': 'a',
                'order': 1
            },
            {
                'key': 'b',
                'data': 'b',
                'order': 2
            },
            {
                'key': 'c',
                'data': 'c',
                'order': 3
            },
            {
                'key': 'd',
                'data': 'd',
                'order': 3
            },
            {
                'key': 'e',
                'data': 'e',
                'order': 4
            },
            {
                'key': 'f',
                'data': 'f',
                'order': 5
            }
        ]

        self.assertCountEqual(actual, expected)

    def test_should_fail_when_adding_non_existent_nodes(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        graph.add_node('b', 'b', [])
        graph.add_node('c', 'c', ['a','b'])

        with self.assertRaises(MissingDependenciesError) as err:
            graph.add_node('d', 'd', ['e', 'f'])
        
        self.assertEqual(err.exception.message, f"Missing dependencies: ['e', 'f']")

    def test_should_fail_when_removing_non_existent_nodes(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        graph.add_node('b', 'b', [])
        graph.add_node('c', 'c', ['a','b'])

        with self.assertRaises(DependencyDoesNotExistError) as err:
            graph.remove_node('d')
        
        self.assertEqual(err.exception.message, f"The dependency (d) does not exist.")

    def test_should_fail_when_removing_nodes_with_dependents(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        graph.add_node('b', 'b', [])
        graph.add_node('c', 'c', ['a','b'])

        with self.assertRaises(ExistingDependentsError) as err:
            graph.remove_node('a')
        
        self.assertEqual(err.exception.message, f"Existing dependents: ['c']. You must remove the existing dependents first.")

    def test_should_fail_on_update_when_cycles_are_detected(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        graph.add_node('b', 'b', ['a'])
        graph.add_node('c', 'c', ['b'])

        with self.assertRaises(DependencyCycleError) as err:
            graph.update_node('a', 'a', ['c'])

        self.assertEqual(err.exception.message, f"Dependency cycle detected: a -> c")

    def test_should_fail_on_update_when_loops_are_detected(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        graph.add_node('b', 'b', ['a'])
        graph.add_node('c', 'c', ['b'])

        with self.assertRaises(DependencyLoopError) as err:
            graph.update_node('a', 'a', ['a'])

        self.assertEqual(err.exception.message, f"Dependency loop detected. A node cannot list itself as a dependency.")

    def test_should_fail_on_update_when_node_does_not_exist(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])

        with self.assertRaises(DependencyDoesNotExistError) as err:
            graph.update_node('b', 'b', [])

        self.assertEqual(err.exception.message, f"The dependency (b) does not exist.")

    def test_should_handle_dependency_graph_updates(self):
        graph = DependencyGraph[str]()
        graph.add_node('a', 'a', [])
        graph.add_node('b', 'b', ['a'])
        graph.add_node('c', 'c', ['b'])
        graph.update_node('c', 'c', [])
        graph.update_node('b', 'b', ['c'])
        graph.update_node('a', 'a', ['b'])

        nodes = graph.generate_evaluation_order()

        actual = [asdict(x) for x in nodes]

        expected = [
            {
                'key': 'c',
                'data': 'c',
                'order': 1
            },
            {
                'key': 'b',
                'data': 'b',
                'order': 2
            },
            {
                'key': 'a',
                'data': 'a',
                'order': 3
            }
        ]

        self.assertCountEqual(actual, expected)

    @pytest.mark.timeout(5)
    def test_should_handle_deeply_nested_dependency_graph(self):
        # This is more of a performance test to try to ensure
        # we can calculate the dependency order for deeply nested
        # graphs with a high level of dependencies.
        # Change the levels and nodes_per_level to evaluate different
        # scenarios
        graph = DependencyGraph[str]()
        levels = 100
        nodes_per_level = 10
        roots = [str(x+1) for x in range(nodes_per_level)]
        expected = [{'key': x, 'data': x, 'order': 1} for x in roots]
        for key in roots:
            graph.add_node(key, key, [])

        dependencies = roots.copy()
        for level in range(levels):
            next_dependencies = []
            for key in roots:
                fkey = f'{key}_{level+1}'
                # every node added has a dependency on all the nodes
                # from every level before it
                graph.add_node(fkey, fkey, dependencies)
                next_dependencies.append(fkey)
                expected.append({'key': fkey, 'data': fkey, 'order': level+2})
            dependencies.extend(next_dependencies)

        nodes = graph.generate_evaluation_order()
        actual = [asdict(x) for x in nodes]
        self.assertCountEqual(actual, expected)
