#############################################################                           
# File name: Search.py
# Author: Alex McCaslin
# Date Modified: 2/4/16
#
# Description: Class made for BFS, DFS, and UCS
#############################################################      


#my search class
from Search import search
import sys

def main():

    #get command line arguments
    numArguments = len(sys.argv)
    argList = sys.argv

    if numArguments != 6:
        print("Number of arguments != 6")
        print("Should look like python Search.py inputFile.txt outputFile.txt startNode endNode searchType")
        print()
        exit()

    #Command line argument placeholders
    inputFile = argList[1]
    outputFile = argList[2]
    startNode = argList[3]
    endNode = argList[4]
    searchType = argList[5]

    mySearches = search(inputFile, outputFile, startNode, endNode)

#    depthSearch = dfs(inputFile, outputFile, startNode, endNode)

#    uniformSearch = ucs(inputFile, outputFile, startNode, endNode)


    mySearches.ReadFile()

    #do a breadth first search
    if searchType == "BFS":
        mySearches.DoBFS()
        
    #do a depth first search
    elif searchType == "DFS":
        mySearches.DoDFS()
            
    #do a uniform cost search
    elif searchType == "UCS":
        mySearches.DoUCS()


main()
