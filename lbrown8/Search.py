from queue import *
import sys

def BFS(startNode, endNode, linkDict):
    
    visited = [startNode]
    q = Queue()
    q.put(startNode)
    path = []
    parentDict = {}

    while not q.empty():
        
        current = q.get()

        if current == endNode:

            parent = current
            
            while parent != startNode:
                path = [parent] + path
                parent = parentDict[parent]
            path = [startNode] + path

            return path

        if current in linkDict.keys():
            children = list(linkDict[current].keys())
            children.sort()

            for i in children:
                if i not in visited:
                    q.put(i)
                    visited.append(i)
                    parentDict[i] = current

    
    return []

def DFS(startNode, endNode, linkDict):
    
    visited = [startNode]
    stack = [startNode]
    path = []

    parentDict = {}

    while len(stack) > 0:


        current = stack.pop()
        path.append(current)
        

        if current == endNode:
            return path
        
        if current in linkDict.keys():
            children = list(linkDict[current].keys())
            children.sort()

            for i in children:
                if i not in visited:
                    stack.append(i)
                    visited.append(i)
                    parentDict[i] = current
        else:
            while len(path) > 1 and path[len(path)-1] != parentDict[stack[len(stack)-1]]:
                path.pop()

    return []

def UCS(startNode, endNode, linkDict):

    visited = [startNode]
    pq = [startNode]
    path = []
    parentDict = {startNode: 0}
    costDict = {startNode: 0}

    while len(pq) > 0:

        current = pq[0]

        # find the next smallest priority
        for i in pq:
            if costDict[current] < costDict[i]:
                current = i

        pq.remove(current)

        if current in linkDict.keys():
            children= list(linkDict[current].keys())
            children.sort()

            for i in children:
                if i not in visited:
                    icost = linkDict[current][i] + costDict[current]
                    pq.append(i)
                    visited.append(i)
                    costDict[i] = icost
                    parentDict[i] = current

                else:
                    if (linkDict[current][i] + costDict[current]) < costDict[i]:
                        costDict[i] = linkDict[current][i] + costDict[current]
                        parentDict[i] = current

    if endNode in visited:

            parent = endNode
            
            while parent != startNode:
                path = [parent] + path
                parent = parentDict[parent]
            path = [startNode] + path

            return path

    else:
        return []


def readFile(fileName):
    
    inFile = open(fileName, 'r')
    
    linkDict = {}

    for line in inFile:
        startNode, endNode, weight = line.split()
        
        weight = int(weight)

        if startNode not in linkDict:
            linkDict[startNode] = {}

        linkDict[startNode][endNode] = weight

    inFile.close()

    return linkDict

def writeToFile(fileName, path):

    outFile = open(fileName, "w")

    for i in path:
        outFile.write(i + "\n")

    outFile.close()

def main(argv):

    inputFile = argv[1]
    outputFile = argv[2]
    startNode = argv[3]
    endNode = argv[4]
    searchType = argv[5]

    linkDict = readFile(inputFile)

    results = []

    if searchType == "BFS":
        
        results = BFS(startNode, endNode, linkDict)

    elif searchType == "DFS":

        results = DFS(startNode, endNode, linkDict)

    elif searchType == "UCS":
        
        results = UCS(startNode, endNode, linkDict)

    else:
        
        print("Invalid search type!")

    writeToFile(outputFile, results)
        

main(sys.argv)
