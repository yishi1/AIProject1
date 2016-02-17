########################################################################
## File:    Search.py                                                 ##
## Author:  Anna Aladiev                                              ## 
## Date:    02/15/2016                                                ##
## Course:  CMSC 471 - Artificial Intelligence (Spring 2016)          ##
## Section: 02                                                        ##
## E-mail:  aladiev1@umbc.edu                                         ## 
##                                                                    ##
##   This file contains the python code for PROJECT 1 - GRAPH SEARCH. ##
## This program conducts a Breadth-First Search, Depth-First Search,  ##
## or Uniform Cost Search based on user-chosen graph data and search  ##
## properties.                                                        ##  
##                                                                    ## 
########################################################################

# for command line argument parsing
import sys

# for queue used in BFS
from collections import deque

# for sorting edges by weights
from operator import itemgetter

# for UCS traversal
import heapq

### BREADTH-FIRST SEARCH ###
def BFS(parents, start, end):
    
    visited, queue, path = [], [], []

    queue.append([start])

    while (len(queue) > 0):

        # path constructed from last popped nodes
        path = queue.pop(0)

        node = path[-1]

        # end search if path is found
        if node == end:
            return path

        elif node not in visited:
            for parent in parents:
                if parent[0] == node:
                    # add parent's children to queue
                    for x in range(1, len(parent)):
                        # update current path by adding on children's path
                        path2 = list(path)
                        path2.append(parent[x])
                        queue.append(path2)

            visited.append(node)

    return (path)

### DEPTH-FIRST SEARCH ###
def DFS(parents, start, end, path = None):

    visited, stack, path = [], [], []
    stack.append(start)

    if(start == end):
        path.append(start)
        return path

    else:
        while (len(stack) > 0):
        
            node = stack.pop()
            visited.append(node)
            path.append(node)
        
            if node == end:
              return path

            else:
                for parent in parents:
                    if parent[0] == node:
                        for x in range(1, len(parent)):
                             if parent[x] not in visited:
                                stack.append(parent[x])
 
    return (path)
             

### UNIFORM COST SEARCH ###
def UCS(edges, parents, start, end):

    visited, queue, path = [], [], []

    # [(COST, NODE, PATH)]
    # q = [('0', start, [])]      
    # cost, node, path = heapq.heappop(queue)
    # update the path
    # path = path + [node]


    queue.append([start])

    while (len(queue) > 0):

        # path constructed from last popped nodes
        path = queue.pop(0)

        node = path[-1]

        # end search if path is found
        if node == end:
            return path

        elif node not in visited:
            for parent in parents:
                if parent[0] == node:
                    # add parent's children to queue
                    for x in range(1, len(parent)):
                        # update current path by adding on children's path
                        path2 = list(path)
                        path2.append(parent[x])
                        queue.append(path2)

            visited.append(node)

    return (path)


# READS COMMAND LINE ARGUMENTS AND VALIDATES INPUT
def ReadCommandLine():

    NUM_ARGS = 5

    # checking for correct number of input arguments
    if ( len(sys.argv) != NUM_ARGS):
            print ("ERROR: INVALID INPUT FORMAT.")
            print ("Please use the following format:")
            print ("python Search.py <input file> <output file> <start node> <end node> <search type>")
            print ("EXITING PROGRAM...")
            exit()

    else:
        inputFile  = (sys.argv[1])
        outputFile = (sys.argv[2])
        startNode  = (sys.argv[3])
        endNode    = (sys.argv[4])
        searchType = (sys.argv[5])

    if ( searchType != ("BFS" or "DFS" or "UCS") ):
        print ("ERROR: INVALID SEARCH TYPE")
        print ("EXITING PROGRAM...")
        exit()

    return (inputFile, outputFile, startNode, endNode, searchType)


# READS IN AN EDGE LIST FROM A TEXT FILE AND CREATES A GRAPH
def readFromFile(fileName):	

    edgeList = []
    neighborsList = []

    try:
        print ("CONSTRUCTING GRAPH FROM '" + fileName + "'...")

        # open file in read mode
        inFile = open(fileName, 'r')

    except IOError:
        print ("ERROR: CANNOT OPEN '" + fileName + "'")
        print ("EXITING PROGRAM...")
        exit()

    else:
        tempList = []
        # each line represents the edge between node1 and node2 with weight 'w'
        for line in inFile:
            node1, node2, w = line.split()
            tempList.append((node1, node2, int(w)))

        # edges sorted by accending weight
        edgeList = sorted(tempList, key = itemgetter(2))

        nodesList = []
        for edge in edgeList:
            if edge[0] not in nodesList:
                # list of parent node names
                nodesList.append(edge[0])

        temp = []
        for node in nodesList:
            temp.append(node)
            for edge in edgeList:
                if edge[0] == node:
                    temp.append(edge[1])
            # list of nodes and their neighbors
            neighborsList.append(temp)
            temp = []
            
        inFile.close()
        print ("GRAPH CONSTRUCTED. \n")

    return (edgeList, neighborsList)


# WRITES THE SOLUTION PATH OF THE SEARCH TO A TEXT FILE
def writeToFile(fileName, path):

    try:
        print ("WRITING PATH SOLUTION TO '" + fileName + "'...")

        # open file in writing mode
        outFile = open(fileName, 'w')

    except IOError:
        print ("ERROR: CANNOT OPEN '" + fileName + "'")
        print ("EXITING PROGRAM...")
        exit()

    else:
        if path:
            for node in path:
                outFile.write(node + "\n")

        # clears contents of file if there is no path
        else:
            outFile.truncate()

        outFile.close()
        print ("PATH SOLUTION WRITTEN. \n")

    return (None)


def main():
    print('')
    
    # command line arguments placeholders
    inputFile  = "graph.txt"
    outputFile = "path.txt"
    startNode  = "A"
    endNode    = "G"
    searchType = "BFS"

    inputFile, outputFile, startNode, endNode, searchType = ReadCommandLine()

    edges, neighbors = readFromFile(inputFile)

    print ("START NODE: " + startNode)
    print ("END NODE:   " + endNode)

    path = []

    if (searchType == "BFS"):
        print ("CONDUCTING BREADTH-FIRST SEARCH...")
        path = BFS(neighbors, startNode, endNode)

    if (searchType == "DFS"):
        print ("CONDUCTING DEPTH-FIRST SEARCH...")
        path = DFS(neighbors, startNode, endNode, path = None)

    if (searchType == "UCS"):
        print ("CONDUCTING UNIFORM COST SEARCH...")
        path = UCS(edges, neighbors, startNode, endNode)


    print ("SEARCH CONDUCTED. \n")
    
    writeToFile(outputFile, path)
    print ("GOODBYE!")

main()