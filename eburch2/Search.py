
# coding: utf-8

import sys

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]
startNode = sys.argv[3]
endNode = sys.argv[4]
searchType = sys.argv[5]

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

# Load the input file
inputFile = open(inputFileName, 'r')

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

def write(msg):
	# Write to output file
	outputFile = open(outputFileName, 'w')
	for line in msg:
		outputFile.write(line)
		outputFile.write("\n")
	outputFile.close()


from collections import deque

queue = deque()
#queue.append(dict['A'])
#queue.append('B')
#nextNode = queue.popleft()
#print(nextNode)
     
def BFS(start, end):
	listOpen = deque(graph.getNodes())
	listClosed = []
	currentNode = start
    
    
	if (start in listOpen):   
		# loop until run out of nodes left or reach end
		      
		# should always be true, would use assert if i knew how to handle it
		if (start in listOpen):
			listOpen.popleft()
			listClosed.append(start)
		
		while (currentNode != end and len(listOpen) != 0):
		
            # gets our neighboring nodes
			try:
				neighbors = graph.getGraph()[currentNode]
			except:
				return	
            
            # checks if any nodes havent been visited yet and explores
			for node in neighbors:
				if (node in listClosed):
					return
				else:
					currentNode = node
					break
                     
                    
			# marks as visited        
			if (currentNode in listOpen):
				listOpen.popleft()
				listClosed.append(currentNode)
			else:
				# dead end, time to look elsewhere
				if (len(listClosed) != 0):  
					currentNode = listClosed.pop()
					
	elif (start == end):
		return listClosed
	else:
		print("EITHER NOT FOUND IN GRAPH OR NO END NODES")  
	return listClosed
	    
def main():
	if (searchType == "BFS"):
		write(BFS(startNode, endNode))
	#elif (searchType == "DFS"):
	#	print (DFS(startNode, endNode))
	#elif (searchType == "UCS"):
	#	print (UCS(startNode, endNode))
	#else
	#	print ("Wrong search type! Choose BFS, DFS, or UCS")
	
main()

