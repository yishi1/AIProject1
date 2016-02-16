# Python imports
import sys
# Basic File I/O section

# Read the File
def ReadFile( toRead ):
    # create a new instance of the graph
    readFile = open( toRead )
    # graph will be a dictionary of a dictionary of tuples,
    # for ease of lookup and reading through the values.
    graph = {}
    for lines in readFile:
        # split the three elements into a tuple, assuming
        # valid input file snytax as per project constraints.
        (parent, child, cost) = lines.split()
        # if the parent element isn't in the graph, add it.
        if parent not in graph:
            graph[parent] = [(child, cost)]
        # otherwise, append the tuple of the child and cost into
        # the graph node.
        else:
            graph[parent].append((child, cost))
    return graph

# Write the File
def WriteFile( toWrite, path ):
    writeFile = open ( toWrite, 'w' )
    # the path will be each string seperated by a newline,
    # as specified in the project description.
    if path is None:
        writeFile.write("")
    else:
        for nodes in path:
            writeFile.write(str(nodes) + '\n')

# BFS Search - needs the graph and the root object
def BFS( graph, root, goal ):
    # path will represent a queue of the nodes to visit.
    path = []
    # insert the root, or the starting point.
    path.append(root)
    # while there are still nodes to traverse,
    # check the currentNode and determine if you have reached the
    # goal. If not, then keep searching through and adding
    # elements to the queue.
    while path:
        # remove the front of the queue
        pos = path.pop(0)
        # the latest position
        currentNode = pos[-1]
        # condition to check to determine if the goal has been
        # reached yet.
        if currentNode is goal:
            # return a list of nodes necessary to travel to the goal.
            return pos
        # get all the children and add them to the queue.
        for childNodes in graph[currentNode]:
            # cast pos as a list for the append operation
            childPos = list(pos)
            # no need to append in the entire tuple in BFS, just
            # need the child's name not the cost.
            childPos.append(childNodes[0])
            # push the childPos into the path queue.
            path.append(childPos)

# DFS Search
def DFS( graph, root, goal ):
    # path will represent a stack of the nodes to visit
    path = []
    # insert the root, or the starting point.
    path.append(root)
    # while there are still nodes to traverse,
    # check the currentNode and determine if you have reached the
    # goal. If not, then keep searching through and adding
    # elements to the queue.
    while path:
        # remove the last element of the stack.
        pos = path.pop()
        # the latest position
        currentNode = pos[-1]
        # condition to check to determine if the goal has been
        # reached yet.
        if currentNode is goal:
            # return a list of nodes necessary to travel to the goal.
            return pos
        # get all the children and add them to the queue.
        for childNodes in graph[currentNode]:
            # cast pos as a list for the append opeeration
            childPos = list(pos)
            # no need to append in the entire tuple for DFS, just
            # need the child's name not the cost.
            childPos.append(childNodes[0])
            # push the childPos into the path stack.
            path.append(childPos)

# UCS Search
def UCS( graph, root, goal ):
    # path will represent a queue of the nodes to visit.
    path = []
    pos = []
    # insert the root, or the starting point.
    path.append((root, '0'))
    # while there are still nodes to traverse,
    # check the currentNode and determine if you have reached the
    # goal. If not, then keep searching through and adding
    # elements to the queue.
    while path:
        # remove the front of the queue
        pos.append(path.pop())
        # the latest position
        currentNode = pos[-1]
        if type(currentNode) is list:
            currentPos = currentNode[-1]
            # condition to check to determine if the goal has been
            # reached yet.
            if currentPos[0] is goal:
                # return a list of nodes necessary to travel to the goal.
                return pos[-1]
            # get all the children and add them to the queue.
            for childNodes in graph[currentPos[0]]:
                # cast pos as a list for the append operation
                childPos = list(pos)
                # no need to append in the entire tuple in BFS, just
                # need the child's name not the cost.
                childTup = (childNodes[0], str(int(childNodes[1]) + int(currentPos[1])))
                childPos.append(childTup)
                # push the childPos into the path queue.
                path.append(childPos)
        else :
            # condition to check to determine if the goal has been
            # reached yet.
            if currentNode[0] is goal:
                # return a list of nodes necessary to travel to the goal.
                return pos[-1]
            # get all the children and add them to the queue.
            for childNodes in graph[currentNode[0]]:
                # cast pos as a list for the append operation
                childPos = list(pos)
                # no need to append in the entire tuple in BFS, just
                # need the child's name not the cost.
                childTup = (childNodes[0], str(int(childNodes[1]) + int(currentNode[1])))
                childPos.append(childTup)
                # push the childPos into the path queue.
                path.append(childPos)

# Driver section
def main():
    # Read in the graph to ReadFile method.
    inFile = sys.argv[1]
    graph = ReadFile(inFile)
    # Prepare the file for answers
    outFile = sys.argv[2]
    # get the start node and the end node
    startNode = sys.argv[3]
    endNode = sys.argv[4]
    # get the search operation to perform
    searchType = sys.argv[5]
    # the user picked BFS.
    if ( searchType == 'BFS' ):
        BFSPath = BFS(graph, startNode, endNode)
        WriteFile(outFile, BFSPath)
    # the user picked DFS
    elif ( searchType == 'DFS' ):
        DFSPath = DFS(graph, startNode, endNode)
        WriteFile(outFile, DFSPath)
    # the user picked UCS
    elif ( searchType == 'UCS' ):
        UCSPath = UCS(graph, startNode, endNode)
        WriteFile (outFile, UCSPath)
    else :
        # user gave a bad argument, write nothing to the output file.
        path = []
        WriteFile( outFile, path)
main()