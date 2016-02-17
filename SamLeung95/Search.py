
# coding: utf-8

# In[131]:

class Graph:
    
    graph={}
    
    def addnode(self, nodeName, connectedNode, weight):
        
        if(nodeName in self.graph):
            
            self.graph[nodeName][connectedNode]=weight

        else:
            
            self.graph[nodeName]={connectedNode:weight}
        
    def getnode(self, nodeName):
        
        if(nodeName not in self.graph):
            
            self.graph[nodeName]={}
            
        return self.graph[nodeName]

        


# In[187]:

def GetPath(graph,start,end,visited):
    
    path=[end]
    count=0
    
    for x in range(len(visited)-2, -1, -1):
        
        node=graph.getnode(visited[x])
        
        if(path[count] in node):
            path.append(visited[x])
            count+=1
                    
    return list(reversed(path))


# In[234]:

def BFS(graph, start, end):
    
    queue=[start]
    visited=[]

    while(queue):
        
        nodeName=queue.pop(0)
        node=graph.getnode(nodeName)
        visited.append(nodeName)
        
        if(node):
            
            for adjacent in node:

                #if there are more linked nodes, then queue those nodes
                if(adjacent not in visited):
                    
                    queue.append(adjacent)
        
        else:
            
            #if end node matches given end node get path
            if(nodeName==end):
               
                return GetPath(graph,start,end,visited)

    return ""
                


# In[232]:

def DFS(graph, start, end):
    
    stack=[start]
    visited=[]

    while(stack):
        
        nodeName=stack.pop(0)
        node=graph.getnode(nodeName)
        visited.append(nodeName)
        
        if(node):
            
            for adjacent in node:

                #if there are more linked nodes, then queue those nodes
                if(adjacent not in visited):
                    
                    stack.insert(0,adjacent)

        else:
            
            #if end node matches given end node get path
            if(nodeName==end):
                
                return GetPath(graph,start,end,visited)
            
    return ""


# In[197]:


    


# In[236]:

def main():
    
    inputFile=sys.argv[1]
    outputFile=sys.argv[2]
    startNode=sys.argv[3]
    endNode=sys.argv[4]
    searchType=sys.argv[5]

    graph=Graph()
    file=open(inputFile, "r")
    
    
    for line in file:
        
        splitLine=line.split(" ")
        graph.addnode(splitLine[0], splitLine[1], splitLine[2].strip())
        
    file.close()
    
    if(searchType=="DFS"):
        
         solution=DFS(graph,startNode,endNode)
        
    elif(searchType=="BFS"):
        
        solution=BFS(graph,startNode,endNode)
        
    elif(searchType=="UCS"):
        
        solution=BFS(graph,startNode,endNode)
        
    else:
        
        print ("Not a valid search type.")
    
    
    file=open(outputFile, "w")
    
    for line in solution:
        
        file.write(line)
        file.write("\n")
        
    file.close()


# In[238]:

import sys

main()


# In[ ]:



