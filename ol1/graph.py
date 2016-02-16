from typing import TypeVar, Generic, Set

V = TypeVar('V')
E = TypeVar('E', int, float)


class Edge(Generic[V, E]):
    def __init__(self, source_vertex: V, target_vertex: V, weight: E):
        self.source = source_vertex
        self.target = target_vertex
        self.weight = weight

    def get_source_vertex(self) -> V:
        return self.source

    def get_target_vertex(self) -> V:
        return self.target

    def get_weight(self) -> E:
        return self.weight


# Yes, I am blatantly basing my design on that of JGraphT
class Graph(Generic[V, E]):
    def __init__(self):
        self.vertices = {}

    def _assert_contains_vertices(self, source_vertex: V, target_vertex: V) -> None:
        if not (source_vertex in self.vertices and target_vertex in self.vertices):
            raise ValueError("Source and/or target vertices not found in graph")

    def _assert_contains_vertex(self, vertex: V) -> None:
        if not (vertex in self.vertices):
            raise ValueError("Vertex not found in graph")

    def _do_remove_edge(self, source_vertex: V, target_vertex: V) -> None:
        del self.vertices[source_vertex][target_vertex]

    def add_vertex(self, vertex: V) -> bool:
        if vertex in self.vertices:
            return False
        self.vertices[vertex] = {}
        return True

    def add_edge(self, source_vertex: V, target_vertex: V, weight: E) -> bool:
        self._assert_contains_vertices(source_vertex, target_vertex)
        if target_vertex in self.vertices[source_vertex]:
            return False
        self.vertices[source_vertex][target_vertex] = weight
        return True

    def contains_edge(self, source_vertex: V, target_vertex: V) -> bool:
        return source_vertex in self.vertices and target_vertex in self.vertices[source_vertex]

    def contains_vertex(self, vertex: V) -> bool:
        return vertex in self.vertices

    # Not a view - does not stay up-to-date
    def edge_set(self) -> Set[Edge[V, E]]:
        edges = set()
        for source_vertex in self.vertices:
            for target_vertex in self.vertices[source_vertex]:
                edges.add(Edge(source_vertex, target_vertex, self.vertices[source_vertex][target_vertex]))
        return edges

    # Not a view - does not stay up-to-date
    def edges_of(self, vertex: V) -> Set[Edge[V, E]]:
        self._assert_contains_vertex(vertex)
        edges = self.edge_set()
        edges_of_vertex = set()
        for edge in edges:
            if edge.get_source_vertex() == vertex or edge.get_target_vertex() == vertex:
                edges_of_vertex.add(edge)
        return edges_of_vertex

    # Not a view - does not stay up-to-date
    def edges_from_vertex(self, source_vertex: V) -> Set[Edge[V, E]]:
        self._assert_contains_vertex(source_vertex)
        edges = set()
        for target_vertex in self.vertices[source_vertex]:
            edges.add(Edge(source_vertex, target_vertex, self.vertices[source_vertex][target_vertex]))
        return edges

    def get_edge_weight(self, source_vertex: V, target_vertex: V) -> E:
        self._assert_contains_vertices(source_vertex, target_vertex)
        return self.vertices[source_vertex][target_vertex]

    def remove_edge(self, source_vertex: V, target_vertex: V) -> bool:
        if self.contains_edge(source_vertex, target_vertex):
            self._do_remove_edge(source_vertex, target_vertex)
            return True
        return False

    # Also removes connected edges
    def remove_vertex(self, vertex: V) -> None:
        edges = self.edges_of(vertex)
        for edge in edges:
            self._do_remove_edge(edge[0], edge[1])
        del self.vertices[vertex]

    def vertex_set(self) -> Set[V]:
        return self.vertices.keys()
