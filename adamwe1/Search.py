#Search.py
#Adam Wendler
#2/5/16
#CMSC471


import sys



#Holds a series of nodes and the weights of movement between them
class Graph: 
    #constructor
    def __init__(self):
        self.Nodes = {} #Nodes are held in a Dictionary
        
    #Adds a node
    def AddNode(self, name):
        #nodes are dictionaries containing neighbors
        self.Nodes[name] = {}
    
    #adds a neighbor to a node
    def UpdateNode(self, node, newNeighbor, weight):
        #adds neighbor to node
        self.Nodes[node][newNeighbor] = weight
        
        #if neighbor does not exists, adds neighbor
        if newNeighbor not in self.Nodes:
            self.Nodes[newNeighbor] = {}
        
        #if neighbor -> node wieghts
        if node not in self.Nodes[newNeighbor]:
            self.Nodes[newNeighbor][node] = weight
        
    #returns the weight of the move
    def GetMove(self, node, goal):
        return self.Nodes[node][goal]
        
    #returns True if node exists in graph
    def HasNode(self, node):
        if node in self.Nodes:
            return True
        
        else:
            return False



#Functions as a priority queue
class PriorityQ:
    #constructor
    def __init__(self):
        self.Cells = []
        self.Priorities = {}#dictionary of priorities by cell
        
    #adds a new node
    def addNode(self, name, priority):
        #truncates new node onto front of Cells
        self.Cells = [name] + self.Cells
        self.Priorities[name] = priority
        
            
    #tries to update the node, return True when update occurs
    def tryUpdateNode(self, node, newPriority):
        hold = self.Priorities[node]
        
        #compares priorities, updates if new weight is preferable
        if hold > newPriority:
            self.Priorities[node] = newPriority
            return True
        
        return False
        
    #pops node of lowers priority
    def getNode(self):
        ticket = 9999
        
        #cycles though Cells
        for n in self.Cells:
            #updates to lowest prority, or node of same priority closer to top
            if self.Priorities[n] <= ticket:
                
                ticket = self.Priorities[n]
                toPop = n
        hold = self.Cells.pop(self.Cells.index(toPop))
        return (hold, ticket)
    



#Reads file contents into arrays
def GetFile(myFile):
    n=0
    rawGraph = []

    #open file in read mode
    inputFile=open(myFile, "r")
    
    #for each line,  split the line and place it into hold
    for line in inputFile:
        rawGraph.append([])
        
        hold = line.split()
        

        #Each edge goes into the graph (node, neighbor, weight)
        for m in hold:
            
            rawGraph[n].append(m)
          
        n = n + 1
        
    #close input stream 
    inputFile.close()
    return rawGraph

    
        
#Write path to file
def WriteFile(myFile, text):
    #opens output
    with open(myFile, "w") as outFile:
    
        #writes each line
        for n in text:
            
            outFile.write(n + "\n")
        outFile.close()
        

#refines the raw path dictionary into a simple array
def RefinePath(rawPath, Root, Goal): 
    path = [Goal]
    n = Goal
    
    #appends untill reaching the root
    while n is not Root:
        #appends each node to the path in reverse
        path.append(rawPath[n][0])
        n = rawPath[n][0]
        
    #path is reversed to the correct order
    path.reverse()
    return path


    
#takes a rawGraph array element and converts it into
#a dictionary-based Graph Object
def MakeGraph(rawGraph):
    newGraph = Graph()
    
    for n in rawGraph:
        node = n[0] 
        
        #if the node does not exist in the Graph, it is added
        if not newGraph.HasNode(node):
            newGraph.AddNode(node)
        
        #Updates node to include new edge
        newGraph.UpdateNode(node, n[1], int(n[2]))
        
    return newGraph

        
    
#Preformes a Bredth First Search from Root to Goal in myGraph
def BreadthFirst(myGraph, Root, Goal):
    n = 0
    memory = []
    fail = [""]
    queue = []
    pathD = {}
    
    #appends root to array and path
    queue.append(Root)  
    pathD[Root] = []
    
    #while queue is not empty
    while queue:
        
        #pop from queue
        current = queue.pop(0)
        #remembers current node
        memory.append(current)
        
        #ends when Goal is reached
        if current == Goal:
            return pathD
        
        #checks all neighbors of current node
        for neighbor in myGraph.Nodes[current]:   
            #if neighbor has not been seen before 
             if neighbor not in memory:
                if neighbor not in queue:
                    #pushes path to queue
                    queue.append(neighbor)
                    #adds neighbor to pathD with path to current
                    pathD[neighbor] = [current]
                
    return fail
    

    
#Preformes a Bredth First Search from Root to Goal in myGraph
def DepthFirst(myGraph, Root, Goal):
    n = 0
    memory = []
    fail = [""]
    stack = [Root]
    pathD = {}
    
    #appends root to path
    pathD[Root] = []
    
    #while stack is note empty
    while stack:
        #pop stack
        current = stack.pop()
        #remember memory
        memory.append(current)
        
        #ends when Goal is reached
        if current == Goal:
            return pathD
        
        #checks all neighbors of current node
        for neighbor in myGraph.Nodes[current]:
            #if neighbor has not been seen before
            if neighbor not in memory:
                if neighbor not in stack:
                    #pushes path to queue
                    stack.append(neighbor)
                    #adds neighbor to pathD with path to current
                    pathD[neighbor] = [current]
    
    return fail


#Preformes a Uniform Cost Search from Root to Goal in myGraph
def UniformCost(myGraph, Root, Goal):
    node = Root
    pathD= {}
    memory = []
    fail = [""]
    weight = 0
    PQ = PriorityQ()
    PQ.addNode(Root, 0)
    
    pathD[Root] = []
    
    #while Priority Queue is not empty
    while PQ.Cells:
        #pop node of highest priority
        current, weight = PQ.getNode()
        #remembers node
        memory.append(current)
        
        #ends when Goal is reached
        if current == Goal:
            return pathD
        
        
        #checks all neighbors of current node
        for n in myGraph.Nodes[current]:
            #if neighbor has not been seen before
            if n not in memory:
                if n not in PQ.Cells:
                    #adds node and weight to PQ
                    #new weight is existent weight + move weight
                    PQ.addNode(n, weight + myGraph.Nodes[current][n])
                    pathD[n] = [current]
                    #print(n)
            

                else:         
                    #Compares weights, replaces if a lower weight is found 
                    flag = PQ.tryUpdateNode(n, weight + myGraph.Nodes[current][n])
                    if flag:
                        pathD[n] = [current] #changes neighbors's path
                      
    return fail 


    
#driver                         
def main():
    #gets rawGraph from file
    rawGraph = GetFile(sys.argv[1])
    #refines raw graph into Graph object
    myGraph = MakeGraph(rawGraph)
    #closes input
    
    
    #decides search type
    searchType = sys.argv[5]
    if searchType == "BFS":
        rawpath = BreadthFirst(myGraph, sys.argv[3], sys.argv[4])

    elif searchType == "DFS":
        rawpath = DepthFirst(myGraph, sys.argv[3], sys.argv[4])

    elif searchType == "UCS":
        rawpath = UniformCost(myGraph, sys.argv[3], sys.argv[4])
           
    #refines path found by search and writes to file
    path = RefinePath(rawpath, sys.argv[3], sys.argv[4])
    WriteFile(sys.argv[2], path)
    

main()   