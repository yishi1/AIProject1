# Search.py
# written by Colter Radden-LeSage
# Student ID: HX85135
# UMBC - CMSC471 - Spring 2016 - Project 1

# parse command line args
import sys

NUM_OF_ARGS = 6
if len(sys.argv) != NUM_OF_ARGS:
    sys.exit("usage: Search.py <input file> <output file> <start node> <end node> <search type>")

infile = sys.argv[1]
outfile = sys.argv[2]
startNode = sys.argv[3]
endNode = sys.argv[4]
searchType = sys.argv[5]


# read the file and generate the graph
# open in read mode
try:
    graphFile = open(infile, "r")
except FileNotFoundError:
    sys.exit(infile + " could not be found")

edges = 0
graph = {}

print("Reading", infile, "...")
for line in graphFile:
    edges += 1
    tokens = line.split()
    if tokens[0] in graph:
        graph[tokens[0]][tokens[1]] = int(tokens[2])
    else:
        graph[tokens[0]] = {tokens[1] : int(tokens[2])}
    if tokens[1] not in graph:
        # ensures a dict entry for nodes with no outflow
	# needed for seamless searching
        graph[tokens[1]] = {}

print("Total Edges:", edges)
# neatly prints graph edges
#for node in graph.keys():
#    print(node, ":", graph[node])

print("Closing", infile)
graphFile.close()




# search block

if searchType == "DFS":
    print("Searching graph from", startNode, "to", endNode, "using Depth First Search...")
    
elif searchType == "BFS":
    print("Searching graph from", startNode, "to", endNode, "using Breadth First Search...")
    
elif searchType == "UCS":
    print("Searching graph from", startNode, "to", endNode, "using Uniform Cost Search...")  

# used by all searches and file output to track parents
visited = {}
pathFound = False

# DFS and BFS use the same code.  The only difference
# is whether a list of nodes is treated as a stack
# or as a queue
if searchType == "DFS" or searchType == "BFS":
    # index of removal point
    # 0 if queue (BFS)
    # len(nodes)- 1 if stack (DFS)
    exitPoint = 0

    # format is (thisNode, parentNode)
    nodes = [(startNode, startNode)]
    while(len(nodes) > 0):
        if searchType == "DFS":
            exitPoint = len(nodes) - 1
        
	# remove node from the list
        current = nodes.pop(exitPoint)

        # check if we've found the goal
        if(current[0] == endNode):
            pathFound = True
            #keep track of goal's "parent"
            visited[endNode] = current[1]
            break
        
        # add nodes unvisited "children" to the stack/queue
        for child in graph[current[0]].keys():
            if child not in visited.keys():
                nodes.append((child, current[0]))

        # mark node as visited and track "parent"
        visited[current[0]] = current[1]


# UCS uses the cost, so it needs a separate block
elif searchType == "UCS":
    
    # tuple format is (cost from startNode, thisNode, parentNode)
    frontier = [(0, startNode, startNode)]
    finalPathCost = -1
    
    while(len(frontier) > 0):
        # pretty sure this turns a list into a priority queue
        # as long as the cost is the first item in the tuple
        current = min(frontier)
        frontier.remove(current)

        # check for the goal node
        if current[1] == endNode:
            pathFound = True
            visited[endNode] = current[2]
            finalPathCost = current[0]
            break
            
        # add node's unvisited children to the frontier
        # update cost and parent if a cheaper path is found
        for child in graph[current[1]].keys():
            if child not in visited.keys():
                # generates list of tuples from frontier
                # that match the child.  May be empty if child
                # node isn't on the frontier yet
                inFrontier = [node for node in frontier if node[1] == child]
		# cost for child nodes is their parent's cost
		# plus the edge between child and parent
                childCost = current[0] + graph[current[1]][child]
		# simply add child if it isn't on the frontier
                if len(inFrontier) == 0:
                    frontier.append((childCost, child, current[1]))
                else:
                    # update cost and parent if cheaper path has been found
                    if inFrontier[0][0] > childCost:
                        frontier[frontier.index(inFrontier[0])] = (childCost, child, current[1])
        # track parents                
        visited[current[1]] = current[2]
        
    if pathFound:
        print("Lowest path cost from", startNode, "to", endNode, ":", finalPathCost)


# handle input error, leaves block open-ended for more searches to be added    
else:
    print("Search Type", searchType, "not recognized")

if not pathFound:
    print("No path found.")

# generate output (reverse order) and write to file
print("Overwriting", outfile, "...")
pathFile = open(outfile, "w")
if pathFound:
    output = "\n"
    current = endNode
    while current != startNode:
        output = "\n" + current + output
        current = visited[current]
    output = startNode + output
    pathFile.write(output)
print("Closing", outfile)
pathFile.close()

