import sys
def openfile():
    flag=True
    #loop until flag is false
    while flag:
        try:
            filename=sys.argv[1]
            inputfile=open(filename,"r")
            flag=False
            inputfile.close()
            return filename
        except:
            print("Do not have this input file")
            flag=False
            exit()

def getgraph(filename):
    #get graph from input file
    inputfile=open(filename,"r")
    Graph={}
    Graph1={}
    #set two graphs one with distance and one without distance
    for line in inputfile:
        node1, node2, d=line.split()
        if node1 in Graph:
           Graph[node1].append((node2))
           Graph1[node1].append((node2,d))
        else:
            Graph[node1]=[(node2)]
            Graph1[node1]=[(node2,d)]
    return Graph,Graph1

def searchtype(stype,mygraph,mygraph1,start,end):
    #determine search type
    if stype == "BFS":
        path=bfspath(mygraph,start,end)
    elif stype == "DFS":
        path=dfspath(mygraph,start,end)
    elif stype == "UCS":
        path=ucspath(mygraph,mygraph1,start,end)
    else:
        print("Wrong search type")
        exit()
    return path

def bfspath(mygraph,start,end):
    #default queue
    queue = []
    queue.append([start])
    while queue:
        #search for the path
        path=queue.pop(0)
        node=path[-1]
        if node == end:
            return path
        for i in mygraph.get(node,[]):
            new_path=list(path)
            new_path.append(i)
            queue.append(new_path)
    return queue

def dfspath(mygraph,start,end):
    #default stack
    stack = []
    stack.append([start])
    while stack:
        #searth for the path
        path=stack.pop()
        node=path[-1]
        if node == end:
            return path
        for i in mygraph.get(node,[]):
            new_path=list(path)
            new_path.append(i)
            stack.append(new_path)
    return stack

def ucspath(mygraph,mygraph1,start,end):
    visited=[]
    nextnode=[]
    distance={}
    parents={}
    for i in mygraph:
        #set default weight
        if i == start:
            distance[i]=0
        else:
            distance[i]=99999
        for j in mygraph[i]:
            if j == start:
                distance[j]=0
            else:
                distance[j]=99999
    current = start
    while len(mygraph1)>len(visited):
        #compare the weight
        visited.append(current)
        for i in mygraph1.get(current,[]):
            child=i[0]
            nextnode.append(child)
            dis = int(i[1])
            newdis = dis + distance[current]
            if newdis < distance[child]:
                distance[child]=newdis
                parents[child]=current
        for j in nextnode:
            if j in visited:
                nextnode.remove(j)
            else:
                current = j
                nextnode.remove(j)
    path=[]
    path.append(end)
    parentnode=parents[end]
    while parentnode != start:
        #find path
        path.append(parentnode)
        parentnode=parents[parentnode]
    path.append(start)
    path.reverse()
    return path

def output(mypath,outputname):
    #write ouput file
    outputfile=open(outputname,"w")
    for item in mypath:
        outputfile.write(item)
        outputfile.write("\n")

def main ():
        outputname=sys.argv[2]
        start=sys.argv[3]
        end=sys.argv[4]
        stype=sys.argv[5]
        filename=openfile()
        mygraph,mygraph1=getgraph(filename)
        mypath=searchtype(stype,mygraph,mygraph1,start,end)
        output(mypath,outputname)
main()


