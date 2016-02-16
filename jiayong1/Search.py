import sys
import copy
from collections import deque

class node(object):
    name = ""
    nextnode = []
    weight = []
    

    def __init__(self, name):
        self.name = name
        self.nextnode = []
        self.weight = []


def DFS(allnodes, allnames, startnode, endnode, outputfilename):
    target = open(outputfilename, 'w')    
    thestart = allnodes[allnames.index(startnode)]
    theend = allnodes[allnames.index(endnode)]    
    queue = []
    queue.append([thestart])
    while queue:
        path = queue.pop(len(queue)-1)
        thenode = path[-1]
        #if thenode in checked:
            #continue
        #checked.add(thenode)
        if thenode.name == theend.name:
            for i in path:
                target.write(i.name)
                target.write("\n")  
            break       
        for i in thenode.nextnode:
           
            path2 = list(path)
            path2.append(i)
            queue.append(path2)
    target.close()


def BFS(allnodes, allnames, startnode, endnode, outputfilename):
    target = open(outputfilename, 'w')    
    thestart = allnodes[allnames.index(startnode)]
    theend = allnodes[allnames.index(endnode)]
    queue = []
    queue.append([thestart])
    while queue:
        path = queue.pop(0)
        thenode = path[-1]
        #if thenode in checked:
            #continue
        #checked.add(thenode)
        if thenode.name == theend.name:
            for i in path:
                target.write(i.name)
                target.write("\n")   
            break      
        for i in thenode.nextnode:
            path2 = list(path)
            path2.append(i)
            queue.append(path2)
    target.close()
    

def UCS(allnodes, allnames, startnode, endnode, outputfilename):
    target = open(outputfilename, 'w')    
    thestart = allnodes[allnames.index(startnode)]
    theend = allnodes[allnames.index(endnode)]
    checked = []
    ready = []

    nodeweight = {}
    nodepath = {}
     
    for i in allnames:
        if i == startnode:
            nodeweight[i] = 0
            nodepath[i] = [i]
        else:
            nodeweight[i] = 100000
            nodepath[i] = []

    thenode = thestart
    while len(checked) < len(allnames):
        checked.append(thenode.name)
        for i in thenode.nextnode:
            ready.append(i.name)
            edge = thenode.weight[thenode.nextnode.index(i)]
            newweight = edge + nodeweight[thenode.name]
            if newweight < nodeweight[i.name]:
                nodeweight[i.name] = newweight
                
                a = copy.deepcopy(nodepath[thenode.name])
                a.append(i.name)
                
                nodepath[i.name] =a 
               
        for j in ready:
            if j in checked:
                ready.remove(j)
            else:
                thenode = allnodes[allnames.index(j)]
                ready.remove(j)
              
                break
    if len(nodepath[endnode]) > 0:
    
        for i in nodepath[endnode]:
            target.write(i) 
            target.write("\n")          
        target.write(str(nodeweight[endnode])) 
        target.write("\n")   
        target.close()
    else:
        target.write("No path found")


        




def main():
    try:
        inputfilename = sys.argv[1]
        outputfilename = sys.argv[2]
        startnode = sys.argv[3]
        endnode = sys.argv[4]
        searchtype = sys.argv[5]
        flag = True
    
        inputFile= open(inputfilename,"r")
    
        allnodes = []
        allnames= []
    
        for line in inputFile:
            mylist =line.strip().split(' ')   

            if mylist[0] in allnames:
                node1 = allnodes[allnames.index(mylist[0])]
            else:
                node1 = node(mylist[0])
                allnames.append(mylist[0])
                allnodes.append(node1)

            if mylist[1] in allnames:
                node2 = allnodes[allnames.index(mylist[1])]
            else:
                node2 = node(mylist[1])
                allnames.append(mylist[1])
                allnodes.append(node2)

            node1.nextnode.append(node2)
            node1.weight.append(int(mylist[2]))
        target = open(outputfilename, 'w')    
        if searchtype == "DFS":
    	    DFS(allnodes, allnames, startnode, endnode, outputfilename)
        
        elif searchtype == "BFS":
         
            BFS(allnodes, allnames, startnode, endnode, outputfilename)
            

        elif searchtype == "UCS":
            UCS(allnodes, allnames, startnode, endnode, outputfilename)

        else:
            target.write("the type is not found")

        target.close()
        

    except:  
        print("Inputfile error or unexpected node")

main()




