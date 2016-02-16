#!/usr/bin/env python3
import os, sys
import queue

class Graph(object):
    def __init__(self, directed_links):
        """Build a representation for a graph given a list of 3-tuples
        representing edges made of (A, B, cost) where A -> B is a directed
        link."""
        self._links = {}
        self.nodes = set()
        # Construct graph as {A: {B: cost}}
        for a, b, cost in directed_links:
            if a not in self._links:
                self._links[a] = {}

            self._links[a][b] = int(cost)
            self.nodes.add(a)
            self.nodes.add(b)

    def links(self, node):
        """Return the edges coming from the given node in a dictionary of
        {B: cost}. If the node is not known, it will return a KeyError. If the
        node has no links from it, it will return an empty dictionary."""
        if node not in self.nodes:
            raise KeyError("Node not known: '{}'".format(node))
        try:
            return self._links[node]
        except KeyError:
            return {}

def dfs(start, end, graph):
    """Find a path from the start to the end on the graph using Depth First
    Search. If the start node is not present in the graph, a KeyError will be
    raised.
    
    Returns a list representing the path to the goal, or None if none is
    found."""
    # A LIFO queue is a stack.
    visit_stack = queue.LifoQueue()
    visit_stack.put((start, []))
    # Keep an unordered set of nodes we have already visited.
    visited = set()

    # Loop as long as there are more nodes to visit, or until the goal is
    # reached.
    while not visit_stack.empty():
        # Grab the last element off the stack.
        node, orig_path = visit_stack.get()
        # If the node has already been visited, skip it.
        if node in visited: continue

        # Mark the node visited and extend the path.
        visited.add(node)
        path = orig_path + [node]

        # Check if it's the goal; if so, return the path.
        if node == end:
            return path

        # Otherwise, push the other nodes to the stack in decreasing order of
        # cost (so that the least expensive edge is on top).
        for next_node, cost in sorted(graph.links(node).items(),
                key = lambda t: t[1],
                reverse = True):
            visit_stack.put((next_node, path))

    return None

def bfs(start, end, graph):
    """Find the shortest path from the start to the end on the graph using
    Uniform Cost Search. If the start node is not present in the graph, a
    KeyError will be raised.

    Returns a list representing the path to the goal, or None if none is
    found."""
    # Use a standard queue.
    visit_queue = queue.Queue()
    visit_queue.put((start, []))
    # Keep an unordered set of nodes we have already visited.
    visited = set()

    # Loop as long as there are more nodes to visit, or until the goal is
    # reached.
    while not visit_queue.empty():
        # Get the best element from the priority queue.
        node, orig_path = visit_queue.get()
        # If the node has already been visited, skip it.
        if node in visited: continue

        # Mark the node visited and extend the path.
        visited.add(node)
        path = orig_path + [node]

        # Check if it's the goal; if so, return the path.
        if node == end:
            return path

        # Otherwise, push the other nodes to the queue in tuples also containing
        # their total path cost. This forms the priority in the priority queue.
        for next_node, next_cost in sorted(graph.links(node).items(),
                key = lambda t: t[1],
                reverse = True):
            visit_queue.put((next_node, path))

    return None

def ucs(start, end, graph):
    """Find the shortest path from the start to the end on the graph using
    Uniform Cost Search. If the start node is not present in the graph, a
    KeyError will be raised.

    Returns a list representing the path to the goal, or None if none is
    found."""
    # Use a priority queue.
    visit_queue = queue.PriorityQueue()
    visit_queue.put((0, start, []))
    # Keep an unordered set of nodes we have already visited.
    visited = set()

    # Loop as long as there are more nodes to visit, or until the goal is
    # reached.
    while not visit_queue.empty():
        # Get the best element from the priority queue.
        path_cost, node, orig_path = visit_queue.get()
        # If the node has already been visited, skip it.
        if node in visited: continue

        # Mark the node visited and extend the path.
        visited.add(node)
        path = orig_path + [node]

        # Check if it's the goal; if so, return the path.
        if node == end:
            return path

        # Otherwise, push the other nodes to the queue in tuples also containing
        # their total path cost. This forms the priority in the priority queue.
        for next_node, next_cost in sorted(graph.links(node).items(),
                key = lambda t: t[1],
                reverse = True):
            visit_queue.put((path_cost + next_cost, next_node, path))

    return None

def main(args):
    if len(args) < 6:
        print("Usage:")
        print("    {} <in_path> <out_path> <start> <end> <search_type>".format(args[0]))
        print()
        print("Search type one of: DFS, BFS, UCS")
        return 1

    in_file_path = args[1]
    out_file_path = args[2]
    start = args[3]
    end = args[4]
    search_type = args[5]

    search_func = {
            "DFS": dfs,
            "BFS": bfs,
            "UCS": ucs
            }[search_type.upper()]

    with open(in_file_path, 'r') as f_in:
        graph = Graph([tuple(line.split()) for line in f_in])

    goal_path = search_func(start, end, graph)
    if not goal_path:
        print("No path exists!")
        goal_path = []

    with open(out_file_path, 'w') as f_out:
        f_out.write('\n'.join(goal_path))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
