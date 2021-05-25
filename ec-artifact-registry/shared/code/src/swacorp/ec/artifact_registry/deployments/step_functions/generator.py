from swacorp.ec.artifact_registry.dependency_graph.graph import DependencyGraph


class StepFunctionGenerator:
    def __init__(self, dependency_graph: DependencyGraph):
        self._dependency_graph = dependency_graph

    def generate(self):
        pass
