# File:        Search.py
# Written by:  Zach Long
# Date:        02/07/16
# Email:       zlong1@umbc.edu 
# Description: Performs breadth first search, depth first search, and uniform cost search on a graph.
#              Graphs specified in an input file with format A B 10\n B C 1\n C B 1 etc.

import sys

#Graphs in the format of (node1, ((node1 neighbors), (cost of neighbors)), node2, ((node2 neighbors), (cost of neighbors))) etc

def breadthFirstSearch(graph, startNode, endNode):
	currentNode = startNode
	queue = []
	queueCostOrigin = []
	visited = []
	queue.append(currentNode)
	queueCostOrigin.append([0, None])
	path = []
	while True:
		if endNode == currentNode:
			break
		location = graph.index(currentNode)
		neighbors = graph[location + 1][0]
		currentNodeLocation = queue.index(currentNode)
		cost = queueCostOrigin[currentNodeLocation][0] + 1
		for node in neighbors:
			if node not in queue:
				queue.append(node)
				queueCostOrigin.append([cost, currentNode])
			else:
				nodeLocation = queue.index(node)
				oldCost = queueCostOrigin[nodeLocation][0]
				if cost < oldCost:
					queueCostOrigin[nodeLocation] = [cost, currentNode]
		visited.append(currentNode)
		done = True
		for node in queue:
			if node not in visited:
				currentNode = node
				done = False
				break
		if done:
			return None #All nodes were visited but endNode was not found.
	while True:
		path.insert(0,currentNode)
		if currentNode == startNode:
			break
		else:
			nodeLocation = queue.index(currentNode)
			currentNode = queueCostOrigin[nodeLocation][1]
	return path

def depthFirstSearch(graph, startNode, endNode):
	currentNode = startNode
	stack = []
	stackOrigin = []
	visited = []
	visitedOrigin = []
	path = []
	visited.append(currentNode)
	visitedOrigin.append(None)
	while True:
		if currentNode == endNode:
			break
		location = graph.index(currentNode)
		neighbors = graph[location + 1][0]
		for node in neighbors:
			if node not in stack and node not in visited:
				stack.append(node)
				stackOrigin.append(currentNode)
		if len(stack) == 0:
			return None
		else:
			currentNode = stack.pop()
			visited.append(currentNode)
			visitedOrigin.append(stackOrigin.pop())
	while True:
		path.insert(0,currentNode)
		if currentNode == startNode:
			break
		if currentNode in stack:
			nodeLocation = stack.index(currentNode)
			currentNode = stackOrigin[nodeLocation]
		else:
			nodeLocation = visited.index(currentNode)
			currentNode = visitedOrigin[nodeLocation]
	return path

def uniformCostSearch(graph, startNode, endNode):
	currentNode = startNode
	priorityQueue = []
	priorityQueueCost = []
	priorityQueueOrigin = []
	visited = []
	visitedCost = []
	visitedOrigin = []
	visited.append(currentNode)
	visitedCost.append(0)
	visitedOrigin.append(None)
	path = []
	while True:
		if endNode == currentNode:
			break
		location = graph.index(currentNode)
		neighbors = graph[location + 1][0]
		costs = graph[location + 1][1]
		currentNodeLocation = visited.index(currentNode)
		cost = visitedCost[currentNodeLocation]
		for i in range(len(neighbors)):
			if neighbors[i] not in priorityQueue and neighbors[i] not in visited:
				priorityQueue.append(neighbors[i])
				priorityQueueCost.append(cost + costs[i])
				priorityQueueOrigin.append(currentNode)
			elif neighbors[i] in priorityQueue:
				nodeLocation = priorityQueue.index(neighbors[i])
				currentCost = priorityQueueCost[nodeLocation]
				if (cost + costs[i]) < currentCost:
					priorityQueueCost[nodeLocation] = cost + costs[i]
					priorityQueueOrigin[nodeLocation] = currentNode
		if len(priorityQueue) == 0:
			return None
		minCostLocation = priorityQueueCost.index(min(priorityQueueCost))
		currentNode = priorityQueue.pop(minCostLocation)
		visited.append(currentNode)
		visitedCost.append(priorityQueueCost.pop(minCostLocation))
		visitedOrigin.append(priorityQueueOrigin.pop(minCostLocation))
	while True:
		path.insert(0,currentNode)
		if currentNode == startNode:
			break
		else:
			if currentNode in priorityQueue:
				nodeLocation = priorityQueue.index(currentNode)
				currentNode = priorityQueueOrigin[nodeLocation]
			else:
				nodeLocation = visited.index(currentNode)
				currentNode = visitedOrigin[nodeLocation]
	return path

def fileReader(filename):
	infile = open(filename, "r")
	graph = []
	for line in infile:
		rawData = line.split()
		firstNode = rawData[0]
		secondNode = rawData[1]
		cost = int(rawData[2])
		if firstNode not in graph:
			added = False
			for i in range(len(graph) / 2):
				if firstNode < graph[i]:
					graph.insert(i, firstNode)
					graph.insert(i + 1, [[secondNode], [cost]])
					added = True
					break
			if not added:
				graph.append(firstNode)
				graph.append([[secondNode], [cost]])
		else:
			paths = graph[graph.index(firstNode) + 1]
			if secondNode not in paths[1]:
				added = False
				for i in range(len(paths[0])):
					if secondNode < paths[0][i]:
						paths[0].insert(i, secondNode)
						paths[1].insert(i, cost)
						added = True
						break
				if not added:
					paths[0].append(secondNode)
					paths[1].append(cost)
			else:
				nodeLocation = paths[1].index(secondNode)
				if cost < paths[0][nodeLocation]:
					paths[0][nodeLocation] = cost #if a single node has multiple paths to some other node, only need shortest cost
		if secondNode not in graph:
			added = False
			for i in range(len(graph) / 2):
				if secondNode < graph[i]:
					graph.insert(i, secondNode)
					graph.insert(i + 1, [[], []])
					added = True
					break
			if not added:
				graph.append(secondNode)
				graph.append([[], []])
		print graph
	return graph

def fileWriter(filename, paths):
	outfile = open(filename, "w")
	if paths is None:
		outfile.write("")
	else:
		for path in paths:
			outfile.write("%s\n" % path)

def main():
	inputFile = sys.argv[1]
	outputFile = sys.argv[2]
	startNode = sys.argv[3]
	endNode = sys.argv[4]
	searchType = sys.argv[5]
	graph = fileReader(inputFile)
	if searchType == 'DFS':
		path = depthFirstSearch(graph, startNode, endNode)
	elif searchType == 'BFS':
		path = breadthFirstSearch(graph, startNode, endNode)
	elif searchType == 'UCS':
		path = uniformCostSearch(graph, startNode, endNode)
	else:
		path = None
	fileWriter(outputFile, path)

main()