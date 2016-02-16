from collections import deque
from typing import Tuple, List, Mapping

from fibonacci_heap_mod import Fibonacci_heap

from graph import Graph, V, E


class Searcher:
    def __init__(self, graph: Graph[V, E]):
        self.graph = graph

    def _assert_contains_vertices(self, source_vertex: V, target_vertex: V) -> None:
        if not self.graph.contains_vertex(source_vertex) or not self.graph.contains_vertex(target_vertex):
            raise ValueError("Cannot perform search on vertices which are not in graph")

    # make list of path, and count distance
    @staticmethod
    def _make_list_from_parents_map(parents: Mapping[V, V], source_vertex: V, target_vertex: V) -> Tuple[List[V], E]:
        distance = 1
        parent = parents[target_vertex]
        path = [target_vertex, parent]
        while parent != source_vertex:
            distance += 1
            parent = parents[parent]
            path.append(parent)

        return reversed(path), distance

    def breadth_first_search(self, source_vertex: V, target_vertex: V) -> Tuple[List[V], E]:
        self._assert_contains_vertices(source_vertex, target_vertex)

        # short-circuit for search for source
        if source_vertex == target_vertex:
            return [source_vertex], 0

        graph = self.graph
        parents = {}

        # enqueue source vertex
        queue = deque([source_vertex])
        parents[source_vertex] = source_vertex

        done = False

        # do search
        while len(queue) > 0 and not done:
            vertex = queue.popleft()

            for edge in graph.edges_from_vertex(vertex):
                adjacent_vertex = edge.get_target_vertex()
                if adjacent_vertex not in parents:
                    # enqueue new vertex
                    parents[adjacent_vertex] = vertex
                    queue.append(adjacent_vertex)
                    # check for target vertex
                    if adjacent_vertex == target_vertex:
                        done = True
                        break

        if target_vertex not in parents:
            raise NoGraphPathException("Source and target vertices are not linked in the graph")

        return self._make_list_from_parents_map(parents, source_vertex, target_vertex)

    def depth_first_search(self, source_vertex: V, target_vertex: V) -> Tuple[List[V], E]:
        self._assert_contains_vertices(source_vertex, target_vertex)

        # short-circuit for search for source
        if source_vertex == target_vertex:
            return [source_vertex], 0

        graph = self.graph
        parents = {}

        # push source vertex
        stack = [source_vertex]
        parents[source_vertex] = source_vertex

        done = False

        # do search
        while len(stack) > 0 and not done:
            vertex = stack.pop()

            for edge in graph.edges_from_vertex(vertex):
                adjacent_vertex = edge.get_target_vertex()
                if adjacent_vertex not in parents:
                    # push new vertex
                    parents[adjacent_vertex] = vertex
                    stack.append(adjacent_vertex)
                    # check for target vertex
                    if adjacent_vertex == target_vertex:
                        done = True
                        break

        if target_vertex not in parents:
            raise NoGraphPathException("Source and target vertices are not linked in the graph")

        return self._make_list_from_parents_map(parents, source_vertex, target_vertex)

    def dijkstra_search(self, source_vertex: V, target_vertex: V) -> Tuple[List[V], E]:
        self._assert_contains_vertices(source_vertex, target_vertex)

        # short-circuit for search for source
        if source_vertex == target_vertex:
            return [source_vertex], 0

        graph = self.graph
        parents = {}
        queue = Fibonacci_heap()

        # enqueue source vertex
        parents[source_vertex] = (source_vertex, 0, queue.enqueue(source_vertex, 0))

        # do search
        while len(queue) > 0:
            vertex = queue.dequeue_min().get_value()
            # check for target vertex
            if vertex == target_vertex:
                break

            for edge in graph.edges_from_vertex(vertex):
                adjacent_vertex = edge.get_target_vertex()
                priority = edge.get_weight() + parents[vertex][1]
                if adjacent_vertex not in parents:
                    # push new vertex
                    parents[adjacent_vertex] = (vertex, priority, queue.enqueue(adjacent_vertex, priority))
                elif priority < parents[adjacent_vertex][1]:
                    # adjust priority of adjacent_vertex
                    entry = parents[adjacent_vertex][2]
                    queue.decrease_key(entry, priority)
                    parents[adjacent_vertex] = (vertex, priority, entry)

        if target_vertex not in parents:
            raise NoGraphPathException("Source and target vertices are not linked in the graph")

        parent = parents[target_vertex][0]
        path = [target_vertex, parent]
        while parent != source_vertex:
            parent = parents[parent][0]
            path.append(parent)

        return reversed(path), parents[target_vertex][1]


class NoGraphPathException(Exception):
    pass
