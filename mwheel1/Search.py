
#File:    Search.py
#Author:  Matthew Wheeler
#Date:    02/07/2016
#Section: 02
#E-mail:  mwheel1@umbc.edu
#Description: A python searching program that calculates DFS BFS
# and UCS on a input file with graph information. It wrotes the
# results of the search to a user designated output file.

INPUT_ARGS = 6

import sys
import math

#
# Class Graph
# Holds the values of a graph and holds data for the various searches 
class Graph:
    def __init__(self):
        self.Nodes = {}
        self.Path = {}
        self.Visited = []
        self.Unvisited = {}

#
# Depth First Search
# Finds any path from a start node to an end node. Unweighted
def depthFirstSearch(graph, startNode, endNode):
    print("Processing depth first search on graph...")
    if startNode in graph.Nodes:
        stack = []
        stack.append(startNode)
        while (len(stack) != 0):
            N = stack.pop()
            if N in graph.Visited: continue
            if N == endNode:
                print("Depth first search executed sucessfully.")
                return graph
            graph.Visited.append(N)
            if N in graph.Nodes:
                for edge in graph.Nodes[N]:
                    stack.append(edge[0])
                    graph.Path[edge[0]] = N
    print("Depth first search executed sucessfully, but found no path.")
    graph.Path = None
    return graph

#
# Breadth First Search
# Finds the shortest path from a start node to an end node. Unweighted
def breadthFirstSearch(graph, startNode, endNode):
    print("Executing breadth first search on graph...")
    if startNode in graph.Nodes:
        queue = []
        queue.append(startNode)
        while (len(queue) != 0):
            N = queue.pop(0)
            if N in graph.Visited: continue
            if N == endNode:
                print("Breadth first search executed sucessfully.")
                return graph
            graph.Visited.append(N)
            if N in graph.Nodes:
                for edge in graph.Nodes[N]:
                    if edge[0] not in graph.Path:
                        queue.append(edge[0])
                        graph.Path[edge[0]] = N
    print("Breadth first search executed sucessfully, but found no path.")
    graph.Path = None
    return graph

#
# Uniform Cost Search
# Finds the shortest path from a start node to an end node. Weighted
def uniformCostSearch(graph, startNode, endNode):
    print("Executing uniform cost search on graph...")
    for node in graph.Nodes:
        if node not in graph.Visited:
            graph.Unvisited[node] = math.inf
            graph.Visited.append(node)
        for edge in graph.Nodes[node]:
            if edge[0] not in graph.Visited:
                graph.Unvisited[edge[0]] = math.inf
                graph.Visited.append(edge[0])
    graph.Visited = []
    current = startNode
    graph.Unvisited[startNode] = int(0)
    while (len(graph.Unvisited) != 0):
        current = min(graph.Unvisited, key=graph.Unvisited.get)
        if current == endNode:
            print("Uniform cost search executed sucessfully.")
            return graph
        if current in graph.Visited or graph.Unvisited[current] == math.inf:
            break
        if current in graph.Nodes:
            for edge in graph.Nodes[current]:
                if edge[0] in graph.Unvisited:
                    temp = int(graph.Unvisited[current]) + int(edge[1])
                    if (temp < graph.Unvisited[edge[0]]):
                        graph.Unvisited[edge[0]] = temp
                        graph.Path[edge[0]] = current
        graph.Visited.append(current)
        del graph.Unvisited[current]
    print("Uniform cost search executed sucessfully, but found no path.")
    graph.Path = None
    return graph

#
# Read File
# Reads in the user specified file and parses it into a graph object
def readFile(inputFile):
    s = 'Opening stream to file ' + inputFile + '...'
    print(s)
    try:
        inFile = open(inputFile, 'r')
        print("File stream opened sucessfully.")
    except IOError:
        s = 'Could not find the specified file: ' + inputFile
        print(s)
        print("Make sure the file exists and is readable then try again.")
        print("Exiting...")
        exit()
    try:
        print("Building graph from data...")
        graph = Graph()
        for line in inFile:
            args = line.split()
            if args[0] in graph.Nodes:
                graph.Nodes[args[0]].append((args[1],args[2]))
            else:
                graph.Nodes[args[0]] = [(args[1],args[2])]
        print("Graph built sucessfully.")
        inFile.close()
        return graph
    except:
        print("Error building graph from data.")
        print("File syntax should look like: A B 1")
        print("Where A: node, B: node, 1: weight from A to B")
        print("Exiting...")
        exit()

#
# Write File
# Writes the output of the previous search to a user designated output file
def writeFile(graph, outputFile, startNode, endNode):
    s = 'Writing output to ' + outputFile + '...'
    print(s)
    outFile = open(outputFile, 'w')
    if (graph.Path == None):
        s = 'No path was found from node '+startNode+' to node '+endNode+'.\n'
        outFile.write(s)
        outFile.close()
        return
    graph.Visited = []
    pathStack = []
    P = endNode
    while (P in graph.Path and P not in graph.Visited and P != startNode):
        print(P)
        pathStack.append(P)
        graph.Visited.append(P)
        P = graph.Path[P]
    if P == startNode:
        pathStack.append(P)
    while (len(pathStack) != 0):
        temp = pathStack.pop()
        outFile.write(temp+'\n')
    outFile.close()
    return

#
# Main
# The main driver of the program
def main():
    if (len(sys.argv) != INPUT_ARGS):
        print("Invalid number of Arguments. Check Syntax.")
        print("Syntax: Search.py <input file> <output file> <start node> <end node> <search type>")
        print("where <search type> = DFS, BFS, UCS")
        print("Exiting...")
        exit()
    else:
        print("Executing Program...")
        try:
            inputFile = str(sys.argv[1])
            outputFile = str(sys.argv[2])
            startNode = str(sys.argv[3])
            endNode = str(sys.argv[4])
            searchType = str(sys.argv[5]).upper()
        except TypeError:
            print("Invalid value types for input.")
            print("Syntax: Search.py <input file> <output file> <start node> <end node> <search type>")
            print("where <search type> = DFS, BFS, UCS")
            print("Example: Search.py input.txt output.txt A Z BFS")
            print("Exiting...")
            exit()
        graph = readFile(inputFile)
        if (searchType == "DFS"):
            graph = depthFirstSearch(graph, startNode, endNode)
        elif (searchType == "BFS"):
            graph = breadthFirstSearch(graph, startNode, endNode)
        elif (searchType == "UCS"):
            graph = uniformCostSearch(graph, startNode, endNode)
        else:
            s = 'Unrecognized input ' + searchType + '. Try: DFS, BFS, UCS'
            print(s)
            print("Syntax: Search.py <input file> <output file> <start node> <end node> <search type>")
            print("Example: Search.py input.txt output.txt A Z BFS")
            print("Exiting...")
            exit()
        writeFile(graph, outputFile, startNode, endNode)
        print("Done.")
        exit()
main()
