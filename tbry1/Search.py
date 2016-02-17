import sys
import queue

class Search:
    def readFile(self, inFile):
        graph = {}
        with open (inFile) as file:
            for lines in file:
                s, f, w = lines.split()
                graph.setdefault(s, []).append((f))
        #print (graph)
        return graph
        
    def readFileWeight(self, inFile):
        graph = {}
        with open (inFile) as file:
            for lines in file:
                s, f, w = lines.split()
                graph.setdefault(s, []).append((f, w))
        #print (graph)
        return graph
        
    def writeFile(self, outFile, path):
        file = open(outFile, "w")
        file.write("\n".join(path))
        file.close()
        
    def bfs (self, myGraph, start, end):
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            try: 
                for next in myGraph[vertex]:
                    if next[0] == end:
                        return path + [next]
                    else:
                        queue.append((next, path +[next]))
            except KeyError:
                continue
                
        
    def dfs (self, myGraph, start, end):
        stack = [(start, [start])]
        while stack:
            (vertex, path) = stack.pop(0)
            try:
                for next in myGraph[vertex]:
                    if next[0] == end:
                        return path + [next]
                    else:
                        stack.append((next, path + [next]))
            except KeyError:
                continue
        
    def ucs (self, myGraph, start, end):
        pqueue = queue.PriorityQueue()
        pqueue.put((0,start))
        node = start
        path = [start]
        vertex = start
        print (pqueue.get())
        while node != end:
            print ("_____________________________________")
            prio, vertex = pqueue.get()
            try:
                for next in myGraph[vertex]:
                    node, weight = next
                    if node == end:
                        return path + [node]
                    else:
                        vertex = node
                        pqueue.put(weight, node)
            except KeyError:
                continue


c = Search()

if sys.argv[5] == "BFS":
    myGraph = c.readFile(sys.argv[1])
    answer = list(c.bfs(myGraph, sys.argv[3], sys.argv[4]))
    c.writeFile(sys.argv[2], answer)
elif sys.argv[5] == "DFS":
    myGraph = c.readFile(sys.argv[1])
    answer = list(c.dfs(myGraph, sys.argv[3], sys.argv[4]))
    c.writeFile(sys.argv[2], answer)
else:
    myGraph = c.readFileWeight(sys.argv[1])
    c.ucs(myGraph, sys.argv[3], sys.argv[4])
    #c.writeFile(sys.argv[2], answer)
    



