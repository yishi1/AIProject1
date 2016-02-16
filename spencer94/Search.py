#Spencer Teolis
#umbc spe1
#471 Proj1

import sys

def make_graph(filename):   
    #dictionary of tuples 
    graph = {}
    f = open(filename, "r")
    for l in f:
        line = l.split()
        #line[0] is first node
        if line[0] in graph:
            #adds tuple as value for key line[0] where line[1] = the connected node and line[2] = the weight 
            graph[line[0]].add((line[1], line[2]))
        else:
            graph[line[0]] = {(line[1], line[2])}
    
    f.close()        
    return graph

def bfs_path(graph, start, goal):
    # queue holds tuples (x,y) where x is the current node and y is a list of the nodes in the path
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        if vertex in graph:
            #makes an ordered set of the nodes connected to current node (vertex)
            connectedNodes = set(sorted([x[0] for x in graph[vertex]]))
            #goes through all unvisted connected nodes
            for node in connectedNodes - set(path):
                if node == goal:
                    return path + [node]
                else:
                    queue.append((node, path + [node]))
                                
def dfs_path(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph:
            connectedNodes = set(sorted([x[0] for x in graph[vertex]]))
            for node in connectedNodes - set(path):
                if node == goal:
                    return path + [node]
                else:
                    stack.append((node, path + [node]))                   

def ucs_path(graph, start, goal):
    # queue holds tuples (x,y) where x is the current node and y is a list of the nodes in the path
    queue = [[start, [start], 0]]
    paths = []
    while queue:
        [vertex, path, cost] = queue.pop(0)
        if vertex in graph:
            #makes a set ordered by weight of the nodes connected to current node (vertex)
            sortedNodes = sorted(graph[vertex], key=lambda x: x[1])
            connectedNodes = set([x[0] for x in sortedNodes])
            weights = [x[1] for x in sortedNodes]
            i = -1
            #goes through all unvisted connected nodes
            for node in connectedNodes - set(path):
                i += 1
                if node == goal:
                    paths.append((path + [node], cost + int(weights[i])))
                else:
                    queue.append([node, path + [node], cost + int(weights[i])])
    if paths:
        return sorted(paths, key=lambda x: x[1])[0][0]
    
    
def write_path(filename, path):
    f = open(filename, "w")
    if path:
        for node in path:
            f.write("%s\n" % node)
    else:
        f.write("No path found \n")
        
    f.close()

def main():

    graph = make_graph(sys.argv[1])
    
    #decides search type
    searchType = sys.argv[5]
    if searchType == "BFS":
        path = bfs_path(graph, sys.argv[3], sys.argv[4])
    elif searchType == "DFS":
        path = dfs_path(graph, sys.argv[3], sys.argv[4])
    elif searchType == "UCS":
        path = ucs_path(graph, sys.argv[3], sys.argv[4])
           
    write_path(sys.argv[2], path)
    

main()   
