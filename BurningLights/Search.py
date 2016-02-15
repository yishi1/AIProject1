import sys

# Runs a breadth-first search on the given graph
def breadthFirstSearch(start, end, edges):
    # Create a queue of nodes, startig with the start
    nodeQueue = [start]
    # List of nodes visited so far
    visitedNodes = []
    # Dictionary of parent nodes
    parents = {}
    # Current node being checked
    currNode = ''
    
    # Continue as long as the queue isn't empty
    while len(nodeQueue) > 0 and currNode != end:
        # Pop first node in list
        currNode = nodeQueue.pop(0)

        # Find adjacent nodes
        if currNode in edges:
            # Sort adjacent nodes by weight, low to high
            adjNodes = edges[currNode].keys()
        else:
            # No adjacent nodes
            adjNodes = []

        # Add nodes to queue and set parent node, if not already visited
        for node in adjNodes:
            # Check if visited or coming up
            if node not in visitedNodes and node not in nodeQueue:
                # Not visited yet
                parents[node] = currNode
                nodeQueue.append(node)
        

        # Mark node as visited
        visitedNodes.append(currNode)

    # List indicating path to goal node
    path = []

    # Trace back from end node to start node, if end node is present
    if end in parents:
        path.append(end)
        currNode = end
        while currNode != start:
            # Add next node to path
            currNode = parents[currNode]
            path.append(currNode)

    # Return reverse of path list, so it goes from start to finish
    path.reverse()
    return path

# Runs a depth-first search on the given graph
def depthFirstSearch(start, end, edges):
    # Create a stack of nodes, startig with the start
    nodeStack = [start]
    # List of nodes visited so far
    visitedNodes = []
    # Dictionary of parent nodes
    parents = {}
    # Current node being checked
    currNode = ''
    
    # Continue as long as the queue isn't empty
    while len(nodeStack) > 0 and currNode != end:
        # Look at top node in stack
        currNode = nodeStack[-1]
        # Find adjacent nodes
        if currNode in edges:
            # Sort adjacent nodes by weight, low to high
            adjNodes = edges[currNode].keys()
        else:
            # No adjacent nodes
            adjNodes = []

        # Whether an unvisited adjacent node has been found
        nodeFound = False
        
        # Add first unvisited node to stack, or backtrack if none
        for node in adjNodes:
            # Check if visited
            if node not in visitedNodes:
                # Not visited yet
                parents[node] = currNode
                nodeStack.append(node)
                nodeFound = True

        if not nodeFound:
            # Backtrack
            nodeStack.pop()

        # Mark node as visited
        visitedNodes.append(currNode)

    # List indicating path to goal node
    path = []
    # Trace back from end node to start node, if end node is present
    if end in parents:
        path.append(end)
        currNode = end
        while currNode != start:
            # Add next node to path
            currNode = parents[currNode]
            path.append(currNode)

    # Return reverse of path list, so it goes from start to finish
    path.reverse()
    return path

# Function to perform uniform cost search
def uniformCostSearch(start, end, edges):
    # Create a heap of nodes, starting with the start
    nodeHeap = [start]
    # List of nodes visited so far
    visitedNodes = []
    # Dictionary of parent nodes
    parents = {}
    # Dictionary of costs to nodes
    costs = {start: 0}
    # Current node being checked
    currNode = ''
    
    # Continue as long as the queue isn't empty
    while len(nodeHeap) > 0 and currNode != end:
        # Pop lowest cost node off of queue
        sortedHeap = sorted(nodeHeap, key=lambda t: costs[t[0]])
        # Get name of first node in sorted heap and remove
        currNode = sortedHeap[0][0]
        nodeHeap.remove(currNode)

        # Find adjacent nodes
        if currNode in edges:
            # Get adjacent nodes
            adjNodes = edges[currNode].items()
        else:
            # No adjacent nodes
            adjNodes = []

        # Add nodes to queue and set parent node, if not already visited
        for node in adjNodes:
            # node[0] is node name, node[1] is cost to node

            # Check if visited
            if node[0] not in visitedNodes:
                # Not visited yet
                # Determine cost to node from start node
                costToNode = costs[currNode] + node[1]
                if node[0] not in costs or costToNode < costs[node[0]]:
                    # New, cheaper path found, or no previous path,
                    # so update cost to node and parent
                    costs[node[0]] = costToNode
                    parents[node[0]] = currNode
                if currNode not in nodeHeap:
                    # Add node to heap, if not already there
                    nodeHeap.append(node[0])
        

        # Mark node as visited
        visitedNodes.append(currNode)

    # List indicating path to goal node
    path = []

    # Trace back from end node to start node, if end node is present
    if end in parents:
        path.append(end)
        currNode = end
        while currNode != start:
            # Add next node to path
            currNode = parents[currNode]
            path.append(currNode)

    # Return reverse of path list, so it goes from start to finish
    path.reverse()
    return path

# Function to write the found path to a file
def writePath(fileName, path):
    outFile = open(fileName, 'w')
    if len(path) == 0:
        # No path found, so print empty string
        outFile.write('')
    else:
        # Write the path one line at a time
        for node in path:
            print(node, file=outFile)
            
    outFile.close()

# Function to read the graph from an input file
def readGraph(fileName):
    # Dictionary for graph edges
    edgeDict = {}

    # Read in edges and weights from file
    inStream = open(fileName, 'r')
    for line in inStream:
        # Remove linebreak
        line = line.replace('\n', '')
        # split line into components
        components = line.split(' ')
        # First component is starting node for edge
        # check for existance in dictionary
        if (not components[0] in edgeDict):
            # Not in edge dictionary, so create new entry
            edgeDict[components[0]] = {}

        # Second component is ending node for edge
        # add weight entry (third component) in dictionary
        edgeDict[components[0]][components[1]] = int(components[2])

    inStream.close()

    return edgeDict

def main():
    # Get input file name, output file name, start node, end node,
    # and search type from command line
    inFileName = sys.argv[1]
    outFileName = sys.argv[2]
    startNode = sys.argv[3]
    endNode = sys.argv[4]
    searchType = sys.argv[5]
    # Dictionary for graph edges
    edgeDict = readGraph(inFileName)

    # Run the appropriate algorithim
    path = []
    if searchType == 'DFS':
        path = depthFirstSearch(startNode, endNode, edgeDict)
    elif searchType == 'BFS':
        path = breadthFirstSearch(startNode, endNode, edgeDict)
    elif searchType == 'UCS':
        path = uniformCostSearch(startNode, endNode, edgeDict)

    #Print resulting path to output file
    writePath(outFileName, path)
main()
