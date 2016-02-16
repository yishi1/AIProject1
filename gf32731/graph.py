import queue
from priorityQueue import PriorityQueue

class Graph:

    graph = {};
    start = ""
    end = ""
    
    def __init__(self, inputFile, start, end):
        myFile = open(inputFile)
        lines = myFile.readlines()
        self.start = start
        self.end = end
        for line in lines:
            self.addLine(line)
            
    def addLine(self,line):
        data = line.split(" ")
        data[2] = data[2].rstrip()
        if data[0] in self.graph:
            self.graph[data[0]].append([data[1],data[2]])
        else:
            self.graph[data[0]] = [[data[1],data[2]]]

    #Breadth First Search
    def solveBFS(self):
        q = queue.Queue()
        if self.start == self.end:
            print("Graph already solved! start and end nodes are the same!")
        else:
            #Build Queue
            for edge in self.graph[self.start]:
                q.put([edge[0],self.start])
            #Recursively solve
            path = []
            self.rsolveBFS(q,path)
            path.append(self.start)
            return path
            
    #Recursive call for BFS
    def rsolveBFS(self,myQueue,path):
        data = myQueue.get()
        currentNode = data[0]
        parent = data[1]
        #Current node is not the final node, add all connected nodes to the queue
        if currentNode != self.end:
            for edge in self.graph[currentNode]:
                myQueue.put([edge[0],currentNode])
            #Recurse and further solve, take solution's parent
            ans = self.rsolveBFS(myQueue,path)
        #Current node is the goal, return parent node
        else:
            path.append(currentNode)
            return parent
        #Is the current node on the path back? If so, return that node's parent,
        if ans == currentNode:
            path.append(currentNode)
            return parent
        #Otherwise return the current parent needed for the path.
        else:
            return ans


    #Depth First Search
    #Exact same as the Breadth First Search, but uses a stack instead
    #causing the search to probe forward until it either finds the goal
    #or cannot go in that direciton any further, then falls back.
    def solveDFS(self):
        s = []
        if self.start == self.end:
            print("Graph already solved! start and end nodes are the same!")
        else:
            for edge in self.graph[self.start]:
                s.append([edge[0],self.start])

            path = []
            self.rsolveDFS(s,path)
            path.append(self.start)
            return path
            

    #Recursive call for Depth First Search
    def rsolveDFS(self,myStack,path):
        data = myStack.pop()
        currentNode = data[0]
        parent = data[1]
        if currentNode != self.end:
            for edge in self.graph[currentNode]:
                myStack.append([edge[0],currentNode])
            ans = self.rsolveDFS(myStack,path)
        else:
            path.append(currentNode)
            return parent
        if ans == currentNode:
            path.append(currentNode)
            return parent
        else:
            return ans

    #Uniform Cost Search. Similar to Breadth First Search, but utilizes a few
    #differing functionalities
    def solveUCS(self):
        #Initialize priority queue and fill it with the first connecting nodes
        pq = PriorityQueue()
        for edge in self.graph[self.start]:
            pq.push(edge,self.start,edge[1])
        #Recurse
        path = []
        self.rsolveUCS(pq,path)
        path.append(self.start)
        return path
        
    #Recursive call for UCS
    def rsolveUCS(self, pQueue, path):
        #Name everything, makes it much easier to remember what does what
        data = pQueue.pop()
        currentNode = data[0][0]
        cost = data[0][1]
        parent = data[1]
        weight = data[2]
        if currentNode != self.end:
            for edge in self.graph[currentNode]:
                #Add the node if it isn't already in the priority queue
                if not pQueue.contains(edge):
                    pQueue.push(edge,currentNode,weight+edge[1])
                else:
                    #If the node is in the priority queue already,
                    #update the weight and parent if the if the new weight is shorter 
                    edgeWeight = pQueue.getElement(edge)[2]
                    if weight < edgeWeight:
                        pQueue.updateElement(edge,currentNode,weight)
        #Same methodology as BFS & DFS
            ans = self.rsolveUCS(pQueue,path)
        else:
            path.append(currentNode)
            return parent

        #Is the current node on the path back? If so, return that node's parent,
        if ans == currentNode:
            path.append(currentNode)
            return parent
        #Otherwise return the current parent needed for the path.
        else:
            return ans
