#Search.py -- Komal Soni

def ucs(graph, start, end, a):

    f = open(a,'w')
    queue = [start]
    traveled = set()

    hold_path = []
    hold_weight = 0

    while queue:
        path = queue.pop(0)
        vertex = path[-1]

        if vertex == end:
            k = 0
            weight = 0
            while (len(path) > k ):
                try:
                     for link_node1 in graph[path[k]]:
                         if(path[k+1] == link_node1[0]):
                             weight = weight + int(link_node1[1])
                except:
                    break
               
                k = k + 1

            if ((hold_weight == 0) or (weight < hold_weight)):
                hold_weight = weight
                hold_path = path

        else:
            if vertex not in traveled:
                try:
                    for link_node in graph[vertex]:
                        add_path = list(path)
                        add_path.append(link_node[0])
                        queue.append(add_path)

                    traveled.add(vertex)
                except:
                    break

    n = 0
    while (len(hold_path) > n ):
        f.write(hold_path[n])
        f.write("\n")
        n = n + 1

    f.close()            

def bfs(graph, start, end, a):

    f = open(a,'w')
    queue = [start]
    traveled = set()
  
    while queue:
        path = queue.pop(0)
        vertex = path[-1]

        if vertex == end:
            k = 0
            while (len(path) > k ):
                f.write(path[k])
                f.write("\n")
                k = k + 1
            break
        
        else:
            if vertex not in traveled:
                try:
                    for link_node in graph[vertex]:
                        add_path = list(path)
                        add_path.append(link_node)
                        queue.append(add_path)               
                        
                    traveled.add(vertex)
                except:
                    f.write(" ")
    f.close()


def dfs(graph, start, end, a, path = [], visited = []):
    
    f = open(a,'w')
    visited.append(start)
    path.append(start)
    edge_fnd = 0

    while (start != end):
        if (edge_fnd == 1):
            if(len(path) == 1):
                f.write(path[0])
                f.write("\n")
            if(len(path) > 0):
                start = path.pop()
            else:
                f.write(" ")
                break
    
        try:
            for edge in graph[start]:
                if edge not in visited:
                    visited.append(edge)
                    if edge not in path:
                        path.append(edge)

                    start = edge
                    break

        except:
            edge_fnd = 1

    k = 0
    while (len(path) > k ):
        f.write(path[k])
        f.write("\n")
        k = k + 1
    f.close()

def main():

    import sys

    if (len(sys.argv) != 6):
        print("Invalid number of arguments!!")
        return

    graph = {}
    with open(sys.argv[1]) as f:
        content = f.readlines()

        for i in range(1,len(content)):
            n1, n2, d = content[i].split()
            if(sys.argv[5] == "UCS"):
                graph.setdefault(n1, []).append((n2, d))
            else:
                graph.setdefault(n1, []).append(n2)
        
    f.close()

    if (sys.argv[5] == "DFS"):
        dfs(graph, sys.argv[3], sys.argv[4], sys.argv[2]) 
    elif (sys.argv[5] == "BFS"):
        bfs(graph, sys.argv[3], sys.argv[4], sys.argv[2])
    elif (sys.argv[5] == "UCS"):
        ucs(graph, sys.argv[3], sys.argv[4], sys.argv[2])
    else:
        print("Invalid Search Type!!")

main()
