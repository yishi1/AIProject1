import sys
import queue
from queue import PriorityQueue


class PQ(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter=0
        
    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1
        
    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item


def result(path, output):
    for item in path:
        output.write("%s\n" %item)



def dfs(startNode, endNode):
    visited = []
    stack = []
    stack.append(startNode)
    

    #insert shorter distance to stack
    while not len(stack) == 0:
        flag = False 
        node = stack[0]

        if node == endNode:
            break
 
        visited.append(node)
        # sort whole dictionary
        if  node in graph:
            graph[node].sort(key = lambda node:node[1])
       
       # break
        else:
            stack.pop(0)
            continue
        #loop all children
        for data in graph[node]:

            shortestNode = data[0]

            if not shortestNode in visited: 
                
                stack.insert(0,shortestNode)
                flag = True
                break
        if flag == False:
            stack.pop(0)
    stack.reverse()
    return (stack)

def bfs(startNode, endNode):
   
    visited= []
 
    q = queue.Queue()
    q.put(startNode)
    
    distanceMap = {}
    # each key store in new dictionary
    for eachKey in graph:
        distanceMap[eachKey] = 999999
        # startNode distance = 99999 ????
        for data1 in graph[eachKey]:
            distanceMap[data1[0]] = 99999
    discoverMap = {}
   # print(eachKey)
    distanceMap[startNode] = 0

    while not q.empty():
        parentNode = q.get()
        visited.append(parentNode)
        if parentNode == endNode:
            break
    #    print ("1111")

        if not  parentNode in graph:
            continue
        # loop lingju
        for data in graph[parentNode]:

            childNode = data[0]
            ToParentDistance = int(data[1])
            # updata distance map
            newDistance = ToParentDistance+distanceMap[parentNode]

            if distanceMap[childNode] > newDistance :
                distanceMap[childNode]= newDistance
                # {b} = a
                discoverMap[childNode]= parentNode

#jia you xian du
            if not childNode in visited:

                q.put(childNode)
            
                       # print(childNode)
        # pop shortest distance

    path= []
    path.append(endNode)
    previousNode = discoverMap[endNode]
    while not previousNode == startNode:
      #  print("666")
      #  print(previousNode)
        path.append(previousNode)
        previousNode = discoverMap[previousNode]
    path.append(startNode)
    path.reverse()
   # print(startNode)
   # print(path)
   # print(distanceMap[endNode])

    return(path)


 #   if distanceMap[childNode] < distanceMap[parentNode]:

def ucs(startNode, endNode):
    
    visited= []
 #   print(startNode + endNode)
 #   print (graph[startNode])
#    initial priority queue
    q = PQ()
    q.put(startNode,0)
    distanceMap = {}   
    # each key store in new dictionary
    for eachKey in graph:
        distanceMap[eachKey] = 999999
        # startNode distance = 99999 ????
        for data1 in graph[eachKey]:
            distanceMap[data1[0]] = 99999
    discoverMap = {}    
   # print(eachKey)
    distanceMap[startNode] = 0

    while not q.empty():
        parentNode = q.get()
        visited.append(parentNode)
      #  if parentNode == endNode:
       #     break
        if not  parentNode in graph:
            continue
        # loop lingju
        for data in graph[parentNode]:
    
            childNode = data[0]
            ToParentDistance = int(data[1])
            # updata distance map
            newDistance = ToParentDistance+distanceMap[parentNode]
            
            if distanceMap[childNode] > newDistance :
                distanceMap[childNode]= newDistance
                # {b} = a
                discoverMap[childNode]= parentNode

#jia you xian du 
            if not childNode in visited:
                q.put(childNode,distanceMap[childNode])
        # pop shortest distance
                
    path= []
    path.append(endNode)
    previousNode = discoverMap[endNode]
   # print("555")
   # print(endNode)
    while not previousNode == startNode:
      #  print("666")
      #  print(previousNode)
        path.append(previousNode)
        previousNode = discoverMap[previousNode]
    path.append(startNode)
    path.reverse()
   # print(startNode)
   # print(path)
   # print(distanceMap[endNode])

    return(path)
    


            
            
        

inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])
startNode = str(sys.argv[3])
endNode = str(sys.argv[4])
searchType = str(sys.argv[5])

readFile = open(inputFile, "r")
output = open(outputFile, "w")
wholeFile = readFile.readlines()

graph = {}
#read input line
for line in wholeFile:
    words = line.split()
    if not words[0] in graph:
        graph[words[0]] = [(words[1],words[2])]
    else:     
        graph[words[0]].append((words[1],words[2]))
   
#print (graph['A'])

#print(searchType)
if searchType == "DFS" :
    path =dfs(startNode, endNode)

if searchType == "BFS":
    path =bfs(startNode, endNode)
    


if searchType == "UCS":
    path =ucs(startNode, endNode)

#print (inputFile+outputFile+startNode+endNode+searchType)

#path = bfs(startNode, endNode)

result(path,output)



