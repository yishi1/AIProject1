# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from sys import argv

def main():
    
    #inline arguments
    readFile = argv[1]
    writeFile = argv[2]
    stNode = argv[3]
    enNode = argv[4]
    searchType = argv[5]
    
    #graph as a dictionary
    graph = {}
    
    #dictionary used for Uniform Cost Search
    costUCS = {}
    
    inFile = open(readFile, "r")
    
    #sets up the dictionaries
    for line in inFile:
        
        node1, node2, weight = line.split()
        
        if node1 not in graph:
            graph[node1] = {}
        
        if node1 not in costUCS:
            costUCS[node1] = ["",-1]
        if node2 not in costUCS:
            costUCS[node2] = ["",-1]
            
        graph[node1][node2] = int(weight)
        
    inFile.close()
    
    costUCS[stNode][1] = 0
    
    visited = [stNode]
    
    #chooses search based on inline arguments
    if (searchType == "BFS"):
        result, visited, endFound = breadthFirstSearch(graph, stNode, enNode, visited)
    elif (searchType == "DFS"):
        result, visited, endFound = depthFirstSearch(graph, stNode, enNode, visited)
    elif (searchType == "UCS"):
        result, visited, endFound = uniformCostSearch(graph, stNode, enNode, visited, costUCS)
    else:
        result, endFound = "Invalid Search Type", False
        
      
    #writes results to file
    outFile = open(writeFile, "w")
    if endFound:
        for node in result:
            outFile.write(node + "\n")
    else:
        outFile.write(result)
        outFile.write("End Node Not Found")
    outFile.close()
    

#recursive
def breadthFirstSearch(graph, stNode, enNode, visited):    
    
    pathQueue = Queue()
    
    if stNode not in graph:
        return [], visited, False
    
    for node in graph[stNode]:
        if node not in visited:
            visited.append(node)
            pathQueue.enqueue(node)
            
            if (node == enNode):
                return [stNode, node], visited, True
    
    endFound = False    
    
    while (pathQueue.isEmpty() == False) and (endFound == False):
        newStNode = pathQueue.dequeue()
        result, visited, endFound = breadthFirstSearch(graph, newStNode, enNode, visited)

    if (endFound == True):
        
        result.insert(0, stNode)
        
        return result, visited, endFound
    
    return [], visited, endFound
    
    
#recursive  
def depthFirstSearch(graph, stNode, enNode, visited):
    
    if stNode not in graph:
        return [], visited, False
    
    for node in graph[stNode]:
        
        if node not in visited:
            visited.append(node)
            
            if (node == enNode):
                return [stNode, node], visited, True
                
            result, visited, endFound = depthFirstSearch(graph, node, enNode, visited)
            
            if (endFound):
                result.insert(0, stNode)
                return result, visited, endFound
    
    return [], visited, False
    
    
#NOT recursive
def uniformCostSearch(graph, stNode, enNode, visited, costUCS):
    
    currNode = stNode
    
    endFound = False
    while(endFound == False):
    
        if (currNode == enNode):
            
            result = []
            
            pathComplete = False
            while(pathComplete == False):
                
                result.insert(0, currNode)
                
                currNode = costUCS[currNode][0]
                
                if(currNode == ""):
                    return result, visited, True
            
    
        if currNode in graph:
            for node in graph[currNode]:
        
                costFromPrevNode = costUCS[currNode][1] + graph[currNode][node]
        
                if ((costFromPrevNode < costUCS[node][1]) or (costUCS[node][1] == -1)):
                    costUCS[node] = (currNode, costFromPrevNode)
            
        visited.append(currNode)
    
        currNode = "done"
        currNodeValue = -1
    
        for node in costUCS:
            if((costUCS[node][1] != -1) and (node not in visited)):
                if((currNodeValue == -1) or (costUCS[node][1] < currNodeValue)):
                
                    currNode = node
                    currNodeValue = costUCS[node][1]
    
        if (currNode == "done"):
            return "", visited, False
    

#queue class
class Queue:
    
    def __init__(self):
        self.items = []
        
    def isEmpty(self):
        return self.items == []
        
    def enqueue(self, item):
        self.items.insert(0,item)
        
    def dequeue(self):
        return self.items.pop()
    
    def size(self):
        return len(self.items)
        
main()