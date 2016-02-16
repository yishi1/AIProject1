# File:			Search.py
# Author: 		Ying Zhang
# Date: 		2/11/2016
# Course:		CMSC 471
# E-mail:		yzhang3@umbc.edu
# Description:  Implement breath first, depth first and uniform cost search
# Reference: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
#            https://en.wikipedia.org/wiki/Breadth-first_search
#            https://en.wikipedia.org/wiki/Depth-first_search
#--------------------------------------------------------------------------

from collections import deque
from heapq import heappush, heappop
import sys
import math

# check if the the source and destinations nodes are in the graph
def inGraph(source, destination, nodes):

	if ((source in nodes) and (destination in nodes)):
		return True

	return False

# changes the priority of an item in the heapq
def changePriority(heap, target, newWeight):

	flag = True
	tmpH = []

	while (flag and heap):
		tmpVertex = heappop(heap)
		
		if (tmpVertex == target):
			heappush(heap, ([newWeight], tmpVertex))
			flag = False
		else:
			tmpH.append(tmpVertex)

	for i in range(len(tmpH)):
		heappush(heap, tmpH[i])

	return heap

# reads the nodes' name and its distance from a file into graph{}
def readFile(fileName):

	temp = []
	keeper = []
	graph = {}

	# open the file
	fin = open(fileName, 'r')

	# parse the file
	# append the nodes to the graph{}
	# parents are the keys and their children objects are the values
	lines = fin.readlines()
	for line in lines:
		temp = line.split()
		node1 = temp[0]
		node2 = temp[1]
		cost = int(temp[2])
		node = [node2, cost]
		if (node1 in graph):
			graph[node1].append(node)
		else:
			graph[node1]=[node]

	fin.close()

	for key in graph.keys():
		if (key not in keeper):
			keeper.append(key)
		value = graph.get(key)
		for j in range(len(value)):
			temp = value[j]
			if (temp[0] not in keeper):
				keeper.append(temp[0])

	return graph, keeper

# outputs the path from source node to destination node to a file
def outputFile(fileName, result):

	fout = open(fileName, 'w')

	for i in range(len(result)):
		fout.write(result[i]+'\n')

	fout.close()

# breadth first search
def breadthFirst(source, destination, graph):

	queue = deque()
	visited = []
	BFParent = {}
	path = []

	queue.append(source)

	try: 
		while (queue):
			current = queue.popleft()

			# if destination reached return path
			if (current == destination):
				temp = destination
				while (temp != source):
					path.insert(0, temp)
					temp = BFParent[temp]
				path.insert(0, source)
				return path

			# if a dead end is reached, do nothing, pop it from the queue
			if (current not in graph.keys() and current != destination):
				current = queue.popleft()
		
			elif (current not in visited):
				visited.append(current)
				for i in graph[current]:
					if (i[0] not in queue):
						queue.append(i[0])
						BFParent[i[0]] = current
	except IndexError:
		return path

# depth first search
def depthFirst(source, destination, graph):

	stack = []
	visited = []
	path = []

	stack.append(source)

	# if the stack is not empty, pop the last element in the stack
	# it will become the current node
	while (stack):	
		current = stack.pop()
		path.append(current)

		# if the destination node is reached, return path
		if (current == destination):
			return path
			
		# if we have reached a dead end, and it is not our destination node
		# pop if from the path
		if (current not in graph.keys() and current != destination):
			current = stack.pop()
			path.pop()

		if (current not in visited):
			visited.append(current)
			for i in graph[current]:
				stack.append(i[0])
		
# uniform cost search
def uniformCost(source, destination, graph):

	weight = {}
	weight[source] = 0
	UCParent = {}
	heap = []
	path = []
	tmpHeap = []
	heapNodes = []

	# initialize the weights of all nodes to infinity
	# initialize the parent of all nodes to an empty string
	for key in graph.keys():
		if (key != source and key not in heapNodes):
			weight[key] = math.inf
			UCParent[key] = ''
		heappush(heap, ([weight[key]], key))
		heapNodes.append(key)
		value = graph.get(key)
		for i in range(len(value)):
			temp = value[i][0]
			if (temp not in graph.keys() and temp not in heapNodes):
				if (temp != source):
					weight[temp] = math.inf
					UCParent[temp] = ''
				heappush(heap, ([weight[temp]], temp))
				heapNodes.append(temp)

	# loop through neighbors of the current node
	while (heap):
		current = heappop(heap)[1]
		if (current in graph.keys()):
			for i in graph[current]:
				# calcualte their weights
				tmpCost = weight[current]+i[1]
				# it will become the new weight(priority) if it is 
				# smaller than the weight already recorded
				if (tmpCost < weight[i[0]]):
					weight[i[0]] = tmpCost
					UCParent[i[0]] = current
					heap = changePriority(heap, i[0], tmpCost)

	# finds the path from source to destination node then return it
	tmpNode = destination
	while (tmpNode != source and UCParent[tmpNode] != ''):
		print("tmpNode: ", tmpNode)
		path.insert(0, tmpNode)
		tmpNode = UCParent[tmpNode]
	path.insert(0, source)

	print("path: ", path)
	return path

# main
def main():

	total = len(sys.argv)
	graph = []
	result = []
	nodes = []

	#if user passed in correct number of arguments, perform the search
	if (total == 6):
		fileName = str(sys.argv[1])
		output = str(sys.argv[2])
		source = str(sys.argv[3])
		destination = str(sys.argv[4])
		search = str(sys.argv[5])

		graph, nodes = readFile(fileName)

		# if the source or destination node does not exist in the graph
		# output an empty string
		if (not inGraph(source, destination, nodes)):
			outputFile(output, result)

		else:
			if (search == "DFS"):
				result = depthFirst(source, destination, graph)
			elif (search == "BFS"):
				result = breadthFirst(source, destination, graph)
			elif (search == "UCS"):
				result = uniformCost(source, destination, graph)
			else:
				print("Search not found")
			outputFile(output, result);

	else:
		print("wrong number of arguments")

main()
