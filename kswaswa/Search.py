# Katie Swanson
# CMSC 471 Max
# Project 1 - Search Graphs using BFS, DFS, and UCS

import sys


myGraph = {}

def readFile(inputFile):
    myFile = open(inputFile, "r")
    for line in myFile:
        myLine = line.split()
        if myLine[0] in list(myGraph.keys()):
            (myGraph[myLine[0]])[myLine[1]] = int(myLine[2])
            if (myLine[1] not in list(myGraph.keys())):
                myGraph[myLine[1]] = {}
        else:
            myGraph[myLine[0]] = {myLine[1]: int(myLine[2])}
    
    myFile.close()

def BFS(startNode, endNode, outputFile):
    currentNode = startNode
    opened = []
    close = []
    path = []
    opened.append((startNode,0))

    while(opened):
        if(currentNode == endNode):
            break
        for i in myGraph.get(currentNode, []):
            isValid = True
            for j in opened:
                if j[0] == i:
                    isValid = False
            for k in close:
                if k[0] == i:
                    isValid = False
            if (isValid):
               opened.append((i, currentNode))
        temp = opened.pop(0)
        close.append(temp)
        currentNode = (opened[0])[0]
        
    path.append(currentNode)
    path.append((opened[0])[1])
    pathNode = (opened[0])[1]
    while (pathNode != startNode):
        for i in close:
            if i[0] == pathNode:
                print ("Appending: ", i[1])
                path.append(i[1])
                pathNode = i[1]
                    
    backwardsPath = list(reversed(path))
    return backwardsPath

def DFS(startNode, endNode, outputFile):
    visited = []
    path = []
    currentNode = startNode
    path.append(startNode)
    visited.append(startNode)
    while(currentNode != endNode):
        children = False
        if (currentNode in list(myGraph.keys())):
            children = list(myGraph[currentNode].keys())
        if (children):
            children.sort()
            i = 0
            while i < len(children):
                if (children[i] in visited):
                    children.pop(i)
                i += 1
            if (children):
                path.append(children[0])
                visited.append(children[0])
                currentNode = children[0]
            else:
                path.pop()
                currentNode = path[-1]
        else:
            path.pop()
            currentNode = path[-1]

    return path  

def UCS(startNode, endNode, outputFile):
    nodes = []
    parents = []
    cost = []
    visited = []
    visitedCost = []
    currentNode = startNode
    numNodes = len(list(myGraph.keys()))

    nodes.append(startNode)
    parents.append(0)
    cost.append(0)

    while (nodes):
        children = list(myGraph[currentNode].keys())
        if(children):
            i = 0
            while i < (len(children)):
                if (children[i] not in visited):
                    if (children[i] in nodes or children[i] in visited):
                        newCost = cost[nodes.index(currentNode)]
                        newCost += (myGraph[currentNode])[children[i]]
                        if (children[i] in nodes):
                            if (newCost < cost[nodes.index(children[i])]):
                                cost[nodes.index(children[i])] = newCost
                                parents[nodes.index(children[i])] = currentNode
                            elif (children[i] in visited):
                                if (newCost < visitedCost[visited.index(children[i])]):
                                    cost[nodes.index(children[i])] = newCost
                                    parents[nodes.index(children[i])] = currentNode
                        else:
                            nodes.append(children[i])
                            cost.append(cost[nodes.index(currentNode)] + (myGraph[currentNode])[children[i]])
                            parents.append(currentNode)
                i += 1
                visitedCost.append(cost[nodes.index(currentNode)])
                cost.remove(cost[nodes.index(currentNode)])
                parents.remove(parents[nodes.index(currentNode)])
                nodes.remove(currentNode)
                visited.append(currentNode)
                if (cost):
                    minimum= min(cost)
                    index = cost.index(minimum)
                    currentNode = nodes[index]
        
    path = []
    visited = []
    currentNode = endNode
    path.append(currentNode)
    visited.append(currentNode)
    while (currentNode != startNode):
        nodes = list(myGraph.keys())
        found = False
        i = 0
        while (not found) and (i < len(nodes)):
            children = myGraph[nodes[i]]
            if (currentNode in children):
                if (nodes[i] not in visited):
                    currentNode = nodes[i]
                    path.append(currentNode)
                    visited.append(currentNode)
                    found = True
            i += 1
    
    backwardsPath = list(reversed(path))
    return backwardsPath

def main():
    if(len(sys.argv) != 6):
        print("You need 6 args")
        exit(1)
    else:
        args = list(sys.argv)
        inputFile = args[1]
        outputFile = args[2]
        startNode = args[3]
        endNode = args[4]
        searchType = args[5]

        readFile(inputFile)

        if searchType == "BFS":
            path = BFS(startNode, endNode, outputFile)
        elif searchType == "DFS":
            path = DFS(startNode, endNode, outputFile)
        elif searchType == "UCS":
            path = UCS(startNode, endNode, outputFile)
        else:
            print("Your search type didn't match any in the system")
            exit(1)

        output = open(outputFile, "w")
        for i in path:
            output.write(i + "\n")
        output.close()

main()
