
# coding: utf-8

# In[533]:

import sys

def main():
    print (BFS('A', 'G'))
    
#inputFileName = sys.argv[1]
#outputFileName = sys.argv[2]
#startNode = sys.argv[3]
#endNode = sys.argv[4]
#searchType = sys.argv[5]

main()


# In[528]:

# Load the input file
inputFile = open('graph.txt', 'r')

#inputContents = inputFile.read()
#print(inputContents)

lines = []

for line in inputFile:
    lines.append(line.rstrip('\n'))
    
inputFile.close()
    
graph = Graph()
    
# Start looping for each line    
    
for index in range(0, len(lines)):
    
    # Strips the start node from the line
    currentLine = lines[index]
    currentLine.split(" ")
    
    nodeStart = currentLine[0]
    nodeEnd = currentLine[2]
    weight = currentLine[4]
    
    graph.addLine(nodeStart, nodeEnd, weight)
    
    print(nodeStart + " start")
    print(nodeEnd + " end")
    print(weight + " cost\n")
    print(lines[index] + "\n")
    


# In[529]:

# Write to output file
outputFile = open('output.txt', 'w')

msg = "testing 1 2 testing 1 2"

outputFile.write(msg)
outputFile.close()


# In[530]:

from collections import deque

queue = deque()
#queue.append(dict['A'])
#queue.append('B')
#nextNode = queue.popleft()
#print(nextNode)


# In[531]:

class Graph:
    
    def __init__(self):
        self.nodesList = []
        self.graph = {}      
    
    def getGraph(self):
        return self.graph;
    
    def getNodes(self):
        return self.nodesList;
    
    def setNodes(self, givenList):
        self.nodes_list = givenList
        
    def addLine(self, start, end, cost):
        if (start in self.graph):
            self.graph[start][end] = cost
        else:
            self.graph[start] = { end : cost }
            
        if (start in self.nodesList):
            return
        else:
            self.nodesList.append(start)
                    
        if (end in self.nodesList):
            return
        else:
            self.nodesList.append(end)     
        


# In[532]:

def BFS(start, end):
    listOpen = graph.getNodes()
    listClosed = []
    currentNode = start
    
    print(graph.getNodes())
    
    if (start in listOpen):
        
        # loop until run out of nodes left or reach end
        while (currentNode != end and len(listOpen) != 0):
            
            # gets our neighboring nodes
            neighbors = graph.getGraph()[currentNode]
            print(neighbors)
            print(listOpen)
            print(listClosed)
            
            # checks if any nodes havent been visited yet and explores
            for node in neighbors:
                if (node not in listOpen):
                    print(node)
                    currentNode = node
                    break
                    
            print(currentNode)        
                    
            # marks as visited        
            if (currentNode in listOpen):
                print("yay")
                currentNode = listOpen.pop()
                listClosed.append(currentNode)
            else:
                # dead end, time to look elsewhere
                if (len(listClosed) != 0):  
                    currentNode = listClosed.pop()
        
        #print(currentNode)
        #if (neighbors == {}):
        #    print("yikes")
        #else:
        #    for i in neighbors:
        #        queue.append(i)
        #    
        #    currentNode = queue.popleft()
        #    listClosed.append(currentNode)
        #    listOpen.pop()
    elif (start == end):
        return listClosed
    else:
        print("EITHER NOT FOUND IN GRAPH OR NO END NODES")  
    return listClosed

