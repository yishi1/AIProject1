# Name:     Katie Dillon 
# Project:  Proj1, CMSC471 
# Date:     February 8, 2016
# E-mail:   kat42@umbc.edu 
# Description: 
#    This file contains code that reads in a file with nodes and 
# constructs a graph. Then it uses the specified search (BFS, DFS, 
# or UCS) and writes out the path it finds from the starting node 
# to the ending node (both specified along with the file and the 
# search type in the command line) into another file. 

import sys 

def main():

    # Check for the correct number of command line arguments 
    if (len(sys.argv) != 6):
        print ("Error: invalid number of arguments. Exiting program...")
        return 

    # Get the command line args and store them in variables 
    commandArgs = list(sys.argv)
    
    #Create a dictionary and call LoadFromFile to create the graph to be used in the search 
    graph = {}
    graph = LoadFromFile(commandArgs[1], graph)

    # Perform the specified search on the graph and starting/ending nodes and store the path 
    finalPath = []
    
    if commandArgs[5] == 'DFS':
        finalPath = DFS(graph, commandArgs[3], commandArgs[4])
    elif commandArgs[5] == 'BFS':
        finalPath = BFS(graph, commandArgs[3], commandArgs[4])
    else:
        finalPath = UCS(graph, commandArgs[3], commandArgs[4])
   
    # Write the path to the output file 
    WriteToFile(commandArgs[2], finalPath) 

    return 

# BFS: Breadth First Search 
# Function to perform a breadth first search on the given graph 
def BFS(graph, startNode, endNode):
    finalPath = []
    queue = []

    # Add the first node as a possible path to the queue 
    currentPath = [startNode]
    queue.append(currentPath)

    while queue:
        currentPath = queue.pop(0)
        
        # Check if the last node in the current path is the end, return 
        # if it is 
        if currentPath[-1] == endNode:
            finalPath = currentPath 
            return finalPath 
        
        # If it wasn't the correct path, add its children (alphabetically sorted) 
        # to the end of the current path and add those path's to the queue of possible path's 
        children = list((graph[currentPath[-1]]).keys())
        children.sort()
        for child in children:
            tempPath = []
            if (child not in currentPath):
                # Copy the currentPath, add the child and put that possible path in the queue
                for i in currentPath :
                    tempPath.append(i)
                tempPath.append(child) 
                queue.append(tempPath)
                
    return finalPath

# DFS: Depth First Search 
# Function to perform a depth first search on the given graph 
def DFS(graph, startNode, endNode):
    path = [startNode]
    opened = [startNode]
    currentNode = path[-1]
    closed = []

    while opened:
        closed.append(currentNode)

        # If we reach the end return 
        if currentNode == endNode:
            return path 

        # Otherwise, pick a child that hasn't been visited and go down that path 
        # if all children have been visited, pop off that node from the path and 
        # use the next to last node moving forward 
        else:
           children = list((graph[currentNode]).keys())
           children.sort()
           allVisited = True 
           
           for child in children:
               if child not in closed:
                   currentNode = child
                   path.append(child)
                   allVisited = False
                   break;
           
           if allVisited:
               path.pop()
               currentNode = path[-1]

    return path 
 
# UCS: Uniform Cost Search (Dijkstra's Algorithim)
# Function to perform a uniform cost search on the given graph 
def UCS(graph, startNode, endNode):

    path = []
    nodesAndCost = []
    opened = [[startNode, 0, 0]]
    closed = []
    currentNode = startNode 
    distance = 0

    # Loop to explore all the nodes and find their costs based on startNode 
    while opened:
        
        # pop off the node just added to the closed/visited queue
        for k in range(len(opened)):
            if (opened[k])[0] == currentNode:
                closed.append(opened.pop(k))
                break

        # get the children of the current node
        children = list((graph[currentNode]).keys())
        children.sort() 
        needToAdd = True  

        # iterate throught the children, updating costs in opened and or adding the 
        # child all together if necessary 
        for child in children:
            for i in range(len(opened)):
                if (opened[i])[0] == child:
                    needToAdd = False 
                    if distance + (graph[currentNode])[child] < (opened[i])[2]:
                        (opened[i])[2] = distance + (graph[currentNode])[child]
                        (opened[i])[1] = currentNode
            if needToAdd: 
                temp = [child, currentNode, distance + (graph[currentNode])[child]]
                opened.append(temp)

        # Find the next minimum cost and set that as the current node and update distance 
        if opened:
            minimum = (opened[0])
            for j in range(len(opened)):
                if (opened[j])[2] < minimum[2] and (opened[j])[0] not in closed:
                    minimum = (opened[j])

            currentNode = minimum[0]
            distance = minimum[2]

    # Get the path by following the parents to the start node and then reverse it 
    path.append(endNode)
    currentNode = endNode
    while currentNode != startNode:
         for f in range(len(closed)):
            if (closed[f])[0] == currentNode:
                path.append(closed[f][1])
                currentNode = ((closed[f])[1])
                break
        
    path.reverse()

    return path 


# LoadFromFile 
# Function to load the nodes from the given file and construct 
# a graph based on the file. It returns a dictionary that stores 
# the graph 
def LoadFromFile(filename, graph): 
    
    inFile = open(filename, "r")

    # Iterate over the lines in the file 
    for line in inFile:
        node1, node2, cost = line.split()
        
        # if the graph already has node1, add node2 and its cost as a dictionary entry 
        if node1 in graph:
            (graph[node1])[node2] = int(cost)
        else:
            graph[node1] = {node2 : int(cost)}

        if node2 not in graph:
            graph[node2] = {}

    inFile.close()

    return graph

# WriteToFile 
# Function that writes the path out to the specified file 
def WriteToFile(outfile, finalPath):

    outFile = open(outfile, "w")
    
    for i in range(0, len(finalPath)):
        outFile.write(finalPath[i])
        outFile.write("\n")

    outFile.close()

    return 

main() 
