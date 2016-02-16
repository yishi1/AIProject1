#File:        Search.py
#Author:      Brendan Waters
#Email:       b101@umbc.edu
#Description:
#             CMSC471 Artificial Intelligence Project 1
#   This program will read in a graph from a text file and then perform
#   a specified search, breadth first, depth first, or uniform cost on
#   the graph to find a path from the start node to the end node and
#   write the path to a text file.

import sys

def BreadthFirstSearch(graph, startNode, endNode):

    #sequences required in the loop
    openNodes = []
    closedNodes = []
    paths = {}

    #set up for loop
    openNodes.append(startNode)
    
    #start search
    #loops until end is found or no open nodes left
    while openNodes:
        
        #get node from start of list (queue) to process
        currentNode = openNodes.pop(0)
        #close this node, as it is being visited
        closedNodes.append(currentNode)

        #check if its the end node
        if currentNode == endNode:
            #was end, return the path to get there
            return TracePath(paths, startNode, endNode)
        
        #wasnt the end node, look at all nodes it is connected to, if any
        if currentNode in graph:
            for nextNode in graph[currentNode]:            
                #make sure next node isn't closed or already opened
                if nextNode[0] not in closedNodes and nextNode[0] not in openNodes:
                    #save this node as the path the next node came from and enqueue
                    paths[nextNode[0]] = currentNode
                    openNodes.append(nextNode[0])

    #end node not found, no valid path. return empty path
    return []

def DepthFirstSearch(graph, startNode, endNode):

    #sequences required in the loop
    openNodes = []
    closedNodes = []
    paths = {}

    #set up for loop
    openNodes.append(startNode)
    
    #start search
    #loops until end is found or no open nodes left
    while openNodes:
        
        #get node from end of list (stack) to process
        currentNode = openNodes.pop()
        #close this node, as it is being visited
        closedNodes.append(currentNode)

        #check if its the end node
        if currentNode == endNode:
            #was end, return the path to get there
            return TracePath(paths, startNode, endNode)
        
        #wasnt the end node, look at all nodes it is connected to, if any
        if currentNode in graph:
            for nextNode in graph[currentNode]:            
                #make sure next node isn't closed or already opened
                if nextNode[0] not in closedNodes and nextNode[0] not in openNodes:
                    #save this node as the path the next node came from and enqueue
                    paths[nextNode[0]] = currentNode
                    openNodes.append(nextNode[0])

    #end node not found, no valid path. return empty path
    return []

def UniformCostSearch(graph, startNode, endNode):
    
    #setup
    openNodes = []
    closedNodes = []
    weight = {}
    paths = {}
    
    weight[startNode] = 0

    openNodes.append(startNode)

    #do the search
    while openNodes:
        
        #find node with min weight
        currentNode = openNodes[0]
        for i in openNodes:
            if weight[i] < weight[currentNode]:
                currentNode = i
        
        #close the node, as it is being visited
        openNodes.remove(currentNode)
        closedNodes.append(currentNode)

        #check if we've reached the end
        if currentNode == endNode:
            return TracePath(paths, startNode, endNode)

        #so go to neighbors, if any
        if currentNode in graph:
            for nextNode in graph[currentNode]:

                #check if nextNode has already been visited
                if nextNode[0] not in closedNodes:
                    
                    #now check if it has already been seen
                    if nextNode[0] in openNodes:
                    
                        #compare new weight to current weight, only update if less than
                        if weight[currentNode] + nextNode[1] < weight[nextNode[0]]:
                            weight[nextNode[0]] = weight[currentNode] + nextNode[1]
                            paths[nextNode[0]] = currentNode

                    else:
                        #wasnt in, add it and calc weight
                        openNodes.append(nextNode[0])
                        weight[nextNode[0]] = weight[currentNode] + nextNode[1]
                        paths[nextNode[0]] = currentNode

    #end node not found, return empty path
    return []

#returns a path from the start node to the end node after search
def TracePath(paths, startNode, endNode):

    thePath = [endNode]

    #loop until the start is found
    while thePath[-1] != startNode:
        #add the path from the last node in paths to the end of thePath 
        thePath.append(paths[thePath[-1]])

    #thePath is from end to start right now, so reverse it
    thePath.reverse()
    return thePath        

def main():
    
    #check args
    if len(sys.argv) != 6:
        print("usage: python Search.py <input file> <output file> <start node> <end node> <search_type>")
        return 1

    #get all the args
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    startNode = sys.argv[3]
    endNode = sys.argv[4]
    searchType = sys.argv[5]

    #the graph to fill in
    graph = {}

    #begin parsing input to fill in graph
    inputFile = open(inputFileName, "r", 1)

    #loop thru each line and get info
    with inputFile as f:
        for line in f:
            line = line.rstrip('\n')
            node1, node2, weight = line.split(" ")
            if node1 not in graph:
                graph[node1] = []
            graph[node1].append((node2, int(weight)))

    inputFile.close()

    #use correct search type
    if searchType == "BFS":
        path = BreadthFirstSearch(graph, startNode, endNode)
    elif searchType == "DFS":
        path = DepthFirstSearch(graph, startNode, endNode)
    elif searchType == "UCS":
        path = UniformCostSearch(graph, startNode, endNode)

    #write the path to file
    outputFile = open(outputFileName, "w", 1)
    for node in path:
        outputFile.write(node + "\n")
    outputFile.close()

if __name__ == "__main__": main()
