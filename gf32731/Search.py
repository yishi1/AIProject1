from graph import Graph
from sys import argv

def main():
    g = Graph(argv[1],argv[3],argv[4])
    a = argv[5]
    output = argv[2]
    path = []
    if a == 'BFS':
        path = g.solveBFS()
    elif a == 'DFS':
        path = g.solveDFS()
    elif a == 'UCS':
        path = g.solveUCS()

    outputFile = open(output,'w')
    for i in range(len(path)-1,-1,-1):
        outputFile.write((path[i]+" "))
main()
    
