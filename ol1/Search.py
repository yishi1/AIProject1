import sys

from graph import Graph
from searcher import Searcher, NoGraphPathException

NUM_ARGS = 5

# Check arg num
if len(sys.argv) != NUM_ARGS + 1:
    print("Invalid number of arguments - expected exactly " + str(NUM_ARGS))
    exit(1)

# Parse command line args
input_file = sys.argv[1]
output_file = sys.argv[2]
start_node = sys.argv[3]
end_node = sys.argv[4]
search_type = sys.argv[5]

# Validate args
if search_type not in ["BFS", "DFS", "UCS"]:
    print("Invalid search type: ", search_type)
    exit(1)

graph = Graph()

# Read from file
file = open(input_file, "r")
for line in file:
    edge = line.split()
    graph.add_vertex(edge[0])
    graph.add_vertex(edge[1])
    graph.add_edge(edge[0], edge[1], int(edge[2]))
file.close()

# Perform search
searcher = Searcher(graph)
try:
    result = []
    if search_type == "BFS":
        result = searcher.breadth_first_search(start_node, end_node)
    elif search_type == "DFS":
        result = searcher.depth_first_search(start_node, end_node)
    elif search_type == "UCS":
        result = searcher.dijkstra_search(start_node, end_node)

    # Write result to file
    file = open(output_file, "w")
    for node in result[0]:
        file.write(node + "\n")
    file.close()
except NoGraphPathException:
    file = open(output_file, "w")
    file.write("")
    file.close()
