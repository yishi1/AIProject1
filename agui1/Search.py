# Jeremy Aguillon
# CMSC 471
# Project 1
# Due 2/15/2016

# imports queues for BFS and UCS
from Queue import Queue
from Queue import PriorityQueue
# imports sys for command line arguments (argv)
import sys


## Constants ## 
# Command line arguments
INPUT_FILE = 1
OUTPUT_FILE = 2
START_NODE = 3
END_NODE = 4
SEARCH_TYPE = 5

# Input file arguments
NODE_1 = 0
NEIGHBOR_1 = 1
WEIGHT = 2

# Error flags
FILE_IO = -1
MISSING_NODE = -2
MISSING_START = -3
MISSING_END = -4

    

# getNodes() takes in a filename and parses the file to create nodes for each of the inputs in the file
#            This also validates that the file exists and can be opened, and the start and end nodes are
#            in the given graph.
# Input: Filename - string of the filename of the input
#        start - the node to begin searching at
#        end - the node to stop searching at
# Output: The nodes that are created and stored in a dictionary or an error flag
def getNodes(Filename, start, end):
    # flags to validate that nodes exist in the given graph
    foundStart = 0
    foundEnd = 0

    # validation for opening the file
    try:
        inFile = open(Filename, 'r')

    except IOError as e:
        print ("I/O error({0}): {1} \"{2}\"".format(e.errno, e.strerror, Filename),)
        # error flag of -1 for main
        return FILE_IO

    # initialized dictionary
    nodeDict = {}

    # loops through each line of the file
    for line in inFile:
        line = line.split()

        # checks for start and end nodes and sets flag when found
        if line[NODE_1] == start or line[NEIGHBOR_1] == start:
            foundStart = 1

        if line[NODE_1] == end or line[NEIGHBOR_1] == end:
            foundEnd = 1

        # adds an entry for each unadded node as the key with a tuple of neighbors and weight as the value
        if line[NODE_1] in nodeDict.keys():
            nodeDict[ line[NODE_1] ].append( ( line[NEIGHBOR_1], int(line[WEIGHT]) ) )
        # if the node already exists, adds another node to the neighbors
        else:
            nodeDict[ line[NODE_1] ] = [(line[NEIGHBOR_1], int(line[WEIGHT]) )]
            
    inFile.close()

    # returns the dictionary if the nodes exist
    if foundStart and foundEnd:
        return nodeDict
    # returns an error message otherwise
    elif foundStart:
        return MISSING_END
    elif foundEnd:
        return MISSING_START
    else: 
        return MISSING_NODE



# writePath() writes the final path it takes to search from start to end to a new file 
# Input: outFile - the filename of the file to be written to
#        finalPath - a list of the nodes of the path from start to end nodes
# Output: None
def writePath(outFile, finalPath):
    outFile = open(outFile, 'w')

    for node in finalPath:
        outFile.write("{0}\n".format(node))

    outFile.close()



'''
Based on pseudocode from Wikipedia
https://en.wikipedia.org/wiki/Depth-first_search
1  procedure DFS-iterative(G,v):
2      let S be a stack
3      S.push(v)
4      while S is not empty
5            v = S.pop()
6            if v is not labeled as discovered:
7                label v as discovered
8                for all edges from v to w in G.adjacentEdges(v) do
9                    S.push(w)
'''
# DFS() uses a graph to search depth first to find a path to a given end node 
#       from a start node and returns the path as a list
# Input: nodeDict - a dictionary of nodes representing a graph
#        start - a start node that is in the graph
#        end - the goal node that is in the graph
# Output: a list of the path from start to end 
def DFS(nodeDict, start, end):
    # creates lists for nodes to visit and visited nodes
    open = []
    closed = []

    # begins with the start node
    open.append(start)

    # loops through the unvisited nodes until there are no more
    while open:
        # examines the node at the top of the stack
        curNode = open.pop()
        # checks if the node is found
        if curNode == end:
            # adds the final node and returns the path
            closed.append(curNode)
            return closed
        # checks if you have visited the node before
        elif curNode not in closed:
            # adds the current node to visited nodes
            closed.append(curNode)
            # adds all neighbors of the current node to unvisited
            for pair in sorted(nodeDict[curNode]):
                open.append(pair[0])

    # return blank string if none found
    return " "


'''
Based on pseudocode from Wikipedia
https://en.wikipedia.org/wiki/Breadth-first_search
1 Breadth-First-Search(Graph, root):
 2 
 3     for each node n in Graph:            
 4         n.distance = INFINITY        
 5         n.parent = NIL
 6 
 7     create empty queue Q      
 8 
 9     root.distance = 0
10     Q.enqueue(root)                      
11 
12     while Q is not empty:        
13     
14         current = Q.dequeue()
15     
16         for each node n that is adjacent to current:
17             if n.distance == INFINITY:
18                 n.distance = current.distance + 1
19                 n.parent = current
20                 Q.enqueue(n)
'''
# BFS() uses a graph to search breadth first to find a path to a given end node 
#       from a start node and returns the path as a list
# Input: nodeDict - a dictionary of nodes representing a graph
#        start - a start node that is in the graph
#        end - the goal node that is in the graph
# Output: a list of the path from start to end 
def BFS(nodeDict, start, end):
    # creates the unvisited nodes as a queue
    open = Queue()
    # closed 1 is the path taken and closed 2 is the node that led to the next node
    closed1 = []
    closed2 = []

    # begins searching at the start node which is the node and what led to it
    open.put((start,start))

    # loops until there are no more unvisited nodes
    while open:
        # dequeues the first node
        curNode = open.get()

        # checks if the node is at the end and stops if it is
        if curNode[0] == end:
            # adds the final node and what sent it to the lists
            closed1.append(curNode[0])
            closed2.append(curNode[1])

            # begins tracing list one back for the path at the goal node
            cur = closed1[len(closed1)-1]
            final = [cur]
            
            # searches each pair until it goes back to the start node
            while cur != start:
                # finds the location of the current node
                loc = closed1.index(cur)
                # finds the node that sent the current node
                cur = closed2[loc]
                # adds the node that sent it to the list
                final.append(cur)

            # returns the final path reversed for consistency with DFS
            return reversed(final)

        # Adds each of the neighbors of the node if it is not the goal
        for pair in sorted(nodeDict[curNode[0]]):
            # each node is classified by the node it is at and the node that led to it
            open.put((pair[0], curNode[0]))
        
        # updates the visited lists and how they got there
        closed1.append(curNode[0])
        closed2.append(curNode[1])
        
    # return blank string if none found
    return " "



'''
Based on pseudocode from Wikipedia
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
 1  function Dijkstra(Graph, source):
 2
 3      create vertex set Q
 4
 5      for each vertex v in Graph:             // Initialization
 6          dist[v] = INFINITY                  // Unknown distance from source to v
 7          prev[v] = UNDEFINED                 // Previous node in optimal path from source
 8          add v to Q                          // All nodes initially in Q (unvisited nodes)
 9
10      dist[source] = 0                        // Distance from source to source
11      
12      while Q is not empty:
13          u = vertex in Q with min dist[u]    // Source node will be selected first
14          remove u from Q 
15          
16          for each neighbor v of u:           // where v is still in Q.
17              alt = dist[u] + length(u, v)
18              if alt < dist[v]:               // A shorter path to v has been found
19                  dist[v] = alt 
20                  prev[v] = u 
21
22      return dist[], prev[]
'''
# UCS() uses a graph to search using Dijkstra's algorithm to find 
#       a path to a given end node from a start node and returns 
#       the path as a list
# Input: nodeDict - a dictionary of nodes representing a graph
#        start - a start node that is in the graph
#        end - the goal node that is in the graph
# Output: a list of the path from start to end 
def UCS(nodeDict, start, end):
    # crates the priority queue with a max value of 10,000
    open = PriorityQueue(10000)
    # creates dictionaries to keep track of distance and previous node of each element
    distance = {}
    previous = {}

    # Initializes each node to have infinity length and no previous
    for node in nodeDict.keys():
        # gives the initial node 0 distance to be chosen first
        if node == start:
            distance[node] = 0
        else:
            distance[node] = float('inf')

        previous[node] = None

        # adds each node to the queue
        open.put((distance[node], node))

    # iterates through each node of the graph
    while open:
        # gets the least valued piece from the queue
        cur = open.get()
        
        # checks if reached the end
        if cur[1] == end:
            temp = end
            finalPath = [temp]
            # loops backwards through the found path until reaches start
            while temp != start:
                temp = previous[temp]
                finalPath.append(temp)
            # returns start reverse for consistency
            return reversed(finalPath)

        # Adds each of the neighbors of the node and compares their length
        for pair in sorted(nodeDict[cur[1]]):
            # distance of current path is saved and compared with distance
            alternate = distance[cur[1]] + pair[1]

            # if the distance is shorter it replaces in the algorithm
            if alternate < distance[pair[0]]:
                distance[pair[0]] = alternate
                previous[pair[0]] = cur[1]

    # returns blank string if no output found
    return ""


# main
def main(argv):
    # validates amount of arguments given
    if len(argv) != 6:
        print("Invalid Input\nUsage: python Search.py <input file> <output file> <start node> <end node> <search_type>")
    # validates correct search types entered
    elif "DFS" != argv[SEARCH_TYPE] and "BFS" != argv[SEARCH_TYPE] and "UCS" != argv[SEARCH_TYPE]:
        print("Invalid Search Type\nUsage: python Search.py <input file> <output file> <start node> <end node> <search_type>\n<search_type> = DFS or BFS or UCS")
    else:
        # Gets the dictionary of nodes and weights
        nodeDict = getNodes(argv[INPUT_FILE], argv[START_NODE], argv[END_NODE])

        # validates start and end nodes exist in graph
        if nodeDict <= MISSING_NODE:
            if nodeDict == MISSING_START:
                print("Start node ({0}) is not in the given graph.".format(argv[START_NODE]))        
            elif nodeDict == MISSING_END:
                print("End node ({0}) is not in the given graph.".format(argv[END_NODE]))        
            else:
                print("Start node ({0}) and/or End node ({1}) are not in the given graph.".format(argv[START_NODE], argv[END_NODE]))        
        # checks if file was sucessfully opened
        elif nodeDict != FILE_IO:    
            # performs the search on the graph that the user requests
            if "DFS" == argv[SEARCH_TYPE]: 
                finalPath = (DFS(nodeDict, argv[START_NODE], argv[END_NODE]))
            elif "BFS" == argv[SEARCH_TYPE]:
                finalPath = BFS(nodeDict, argv[START_NODE], argv[END_NODE])    
            elif "UCS" == argv[SEARCH_TYPE]:
                finalPath = UCS(nodeDict, argv[START_NODE], argv[END_NODE])

            # writes the final result to the provided file
            writePath(argv[OUTPUT_FILE], finalPath)


# call to main
main(sys.argv)
