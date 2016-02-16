#Dylan Chu
#2/15/16
#CMSC 471 AI
#Project 1
#Breadth-First, Depth-First, and Uniform Cost Search in python
import sys

#reads file into graph
def readFile(infile):
    testlist = []
    f=open(infile,"r")
    for line in f:
        source, dest, value = line.split()
        testlist.append([source, dest,int(value)])
    f.close()
    return testlist

#writes path into file
def writeFile(outfile, data):
    f = open(outfile,"w")
    for node in data:
        f.write(node + "\n")
        
    f.close()
    return 0

#takes the command line args
def processCommandLineArgs():
    infile = sys.argv[1]
    outfile = sys.argv[2]
    start = sys.argv[3]
    end = sys.argv[4]
    search = sys.argv[5]
    return infile, outfile, start, end, search

#Each search takes 3 args:
#graph: the graph to search
#start, end: the start and ending nodes
#Each method returns the path if found, or an empty string if no path was found


#depth first search
def DFS(graph, start, end):
    #set up the data structures
    visited, stack = [], []
    last = ""
    #expand start node
    for node in graph:
        if node[0] == start:
            stack.append([node[0], node[1]])
            
    while stack:
        
        node = stack.pop()
        #mark current position as visited
        if node[0] not in visited:
            visited.append(node[0])

        #if we expand into the end, then end
        if node[1] == end:
            #set up variables to find path
            visited.append(node[1])
            last = node[1]
            antiloop = node[1]
            path = [last]
            flag = 1
            #loop through the graph backwards to construct the path
            #antiloop is there to stop the graph from going back and forth between nodes
            while flag == 1:
                for pathnode in graph:
                    if pathnode[1] == last and pathnode[0] != antiloop:
                        path.insert(0,pathnode[0])
                        last = pathnode[0]
                        antiloop = pathnode[1]
                        if pathnode[0] == start:
                            flag = 0
                            break
                
            
            return path
        #place next node in stack
        vertex = node[1]
        if vertex not in visited:
            for node2 in graph:
                if node2[0] == vertex:
                    stack.append([node2[0], node2[1]])
    #return empty string if no answer is found
    if end not in visited:
        return ""
    else:
        return visited

#breadth first search
def BFS(graph, start, end):
    #set up data structures
    visited, stack = [], []
    last = ""
    #expand start node
    for node in graph:
        if node[0] == start:
            stack.append([node[0], node[1]])
            
    while stack:
        node = stack.pop(0)
        #mark current position as visited
        if node[0] not in visited:
            visited.append(node[0])
            
        #if we expand into the end, then end
        if node[1] == end:
            #set up variables to find path
            visited.append(node[1])
            last = node[1]
            antiloop = node[1]
            path = [last]
            flag = 1
            #loop through the graph backwards to construct the path
            #antiloop is there to stop the graph from going back and forth between nodes
            while flag == 1:
                for pathnode in graph:
                    if pathnode[1] == last and pathnode[0] != antiloop:
                        path.insert(0,pathnode[0])
                        last = pathnode[0]
                        antiloop = pathnode[1]
                        if pathnode[0] == start:
                            flag = 0
                            break
                
            
            return path
        #place next node in stack
        vertex = node[1]
        if vertex not in visited:
            for node2 in graph:
                if node2[0] == vertex:
                    stack.append([node2[0], node2[1]])
    #return empty string if no answer is found    
    if end not in visited:
        return ""
    else:
        return visited

#uniform cost search
def UCS(graph, start, end):
    #set up data structures
    visited, pqueue = {},[]

    #expand start node
    for node in graph:
        if node[0] == start:
            pqueue.append(node)
            if node[0] not in visited:
                visited[node[0]] = 0

    while pqueue:
        #sort the priority queue to find the smallest distance
        sorted(pqueue, key = lambda n:n[2])
        node = pqueue.pop(0)

        #check for the end
        if node[1] == end:
            visited[node[1]] = node[2] + visited[node[0]]
            last = node[1]
            antiloop = node[1]
            path = [last]
            flag = 1
            #find path
            while flag == 1:
                for pathnode in graph:
                    if pathnode[1] == last and pathnode[0] != antiloop:
                        path.insert(0,pathnode[0])
                        last = pathnode[0]
                        antiloop = pathnode[1]
                        if pathnode[0] == start:
                            flag = 0
                            break
                
            
            return path

        #check the next node and expand
        goal = node[1]
        if goal not in visited or visited[goal] < visited[node[0]]+node[2]:
            visited[goal] = node[2] + visited[node[0]]
            for i in graph:
                if i[0] == goal:
                    pqueue.append([i[0],i[1], node[2] + visited[node[0]]])
            

                
            
  
        


    return ""


def main():
    infile, outfile, start, end, search = processCommandLineArgs()
    graph = readFile(infile)
    answer = ""
    flag = 1
    if search == "BFS":
        print("Breadth-First Search")
        answer = BFS(graph, start, end)
    elif search == "DFS":
        print("Depth-First Search")
        answer = DFS(graph, start, end)
    elif search == "UCS":
        print("Uniform-Cost Search")
        answer = UCS(graph, start, end)
    else:
        print("illegal search")
        flag = 0
        
    if flag ==1:
        writeFile(outfile, answer)


main()
