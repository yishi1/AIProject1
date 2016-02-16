# Name: Jerson Guansing
# Assignment: Project 1
# Class: CMSC 471
# Instructor: Prof. Maksym Morawski
import sys
try:
    import Queue as Q
except ImportError:
    import queue as Q
from collections import deque

# read the data file
def readFile(fileName):
	graph = dict()
	with open(fileName, "r") as f:
		for line in f:
			# upper case each line for consistency
			line = line.upper()
			fields = line.split(" ")
			#print(fields[0],fields[1],int(fields[2]))
			if fields[0] in graph:
				# the dictionary key exists, so update it
				dest = graph[fields[0]]
				dest.update( {str(fields[1]) : int(fields[2]) } )
				graph[fields[0]] = dest
			else:
				# the dictionary key doesn't exist, so create it
				graph[ str(fields[0]) ] = { str(fields[1]) : int(fields[2]) }
	return graph

# write the data to a file
def writeFile(fileName, visited):
	out = open(fileName, "w")
	for key in visited:
		print(key)
		out.write(key + "\n")
	out.close()

# Uniform-cost search
def ucs(graph, end, priorityQueue):
	while not priorityQueue.empty():
		currentNode = {}
		cost, start, visited = priorityQueue.get()
		#print(cost, start, visited)
		# remove the visited node from the graph
		if start in graph:
			currentNode = graph[start]
			del graph[start]
		#check if the current node matches the goal
		if(start == end):
			# goal found, return the visited list
			return visited
		else:
			# all the child nodes of current node sorted by value
			#for key in sorted(currentNode, key=currentNode.__getitem__):
			for key in currentNode:
				#print(key)
				# keep track of the node path by passing the visited list
				#print(key, currentNode[key])
				# add it to the queue (cost, key, path)
				priorityQueue.put((cost + currentNode[key], str(key), visited + [key] ))
	# goal node not found
	return list()

# Breath-first search
def bfs(graph, end, queue):
	while queue:
		currentNode = {}
		start, visited = queue.popleft()
		#print(start, visited)
		# remove the visited node from the graph
		if start in graph:
			currentNode = graph[start]
			#print(start, currentNode)
			del graph[start]
			#print(start, currentNode)
		#check if the current node matches the goal
		if(start == end):
			# goal found, return the visited list
			return visited
		else:
			# add all the nodes on the level below to the queue
			for key, value in sorted(currentNode.items()):
				# keep track of the node path by passing the visited list
				#print(key, value)
				# add it to the queue (key, path)
				queue.append((str(key), visited + [key] ))
	# goal node not found
	return list()

# Depth-first search
def dfs(graph, end, stack):
	while stack:
		currentNode = {}
		start, visited = stack.pop()
		#print(start, visited)
		# remove the visited node from the graph
		if start in graph:
			currentNode = graph[start]
			#print(start, currentNode)
			del graph[start]
			#print(start, currentNode)
		#check if the current node matches the goal
		if(start == end):
			# goal found, return the visited list
			return visited
		else:
			# add all the nodes on the level below to the queue
			for key, value in sorted(currentNode.items(), reverse=True):
				# keep track of the node path by passing the visited list
				#print(key, value)
				# add it to the stack (key, path)
				stack.append((str(key), visited + [key] ))
	# goal node not found
	return list()

def main():
	if len(sys.argv) < 6:
		print("Need five(5) command line arguments.")
		print("Search.py <input file> <output file> <start> <end> <search type>")
	else:
		inputFile, outputFile = sys.argv[1], sys.argv[2]
		start, end = (sys.argv[3]).upper(), (sys.argv[4]).upper()
		searchType, visited = (sys.argv[5]).upper(), list()
		
		# read the input file and create the graph
		graph = readFile(inputFile)

		# do the search based on command line argument
		if searchType == "DFS":
			stack = [ (start, list(start)) ]
			visited = dfs(graph, end, stack)
		elif searchType == "UCS":
			priorityQueue = Q.PriorityQueue()
			priorityQueue.put((0, start, list(start)))
			visited = ucs(graph, end, priorityQueue)
		elif searchType == "BFS":
			queue = deque()
			queue.append((start, list(start)))
			visited = bfs(graph, end, queue)
		else:
			dfs(graph, start, end, visited)
		
		writeFile(outputFile, visited)

# call the main function
main()