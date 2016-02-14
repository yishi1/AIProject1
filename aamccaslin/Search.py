#############################################################
# File name: Search.py
# Author: Alex McCaslin
# Date Modified: 2/4/16
#
# Description: Class made for BFS, DFS, and UCS
#              
#############################################################

import queue

class search:
    def __init__(self, theInputFile, theOutputFile, theStartNode, theEndNode):
        self.inputFile = theInputFile
        self.outputFile = theOutputFile
        self.startNode = theStartNode
        self.endNode = theEndNode


        self.alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        self.alphabetDict = {"A":"0", "B":"1", "C":"2", "D":"3", "E":"4", "F":"5", "G":"6", "H":"7", "I":"8", "J":"9", "K":"10", "L":"11", "M":"12", "N":"13", "O":"14", "P":"15", "Q":"16", "R":"17", "S":"18", "T":"19", "U":"20", "V":"21", "W":"22", "X":"23", "Y":"24", "Z":"25"}

        self.alreadyVisited = []
        self.parent = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        self.exist = []
        self.nodesMatrix = []

        #26 by 26 reference array
        for letter in self.alphabet:
            tempAlphabet = []
            for letter2 in self.alphabet:
                tempAlphabet.append(letter2)
            self.nodesMatrix.append(tempAlphabet)

    def ReadFile(self):
        infile = open(self.inputFile, 'r')
        
        for line in infile:
            line = line.split()

            #If line[0] = C and line[1] = E and line[2] = "5"
            #nodesMatrix will access at [2][4] and set = to "5"
            firstNode = self.alphabetDict[str(line[0])]

            secondNode = self.alphabetDict[str(line[1])]
            
            self.nodesMatrix[int(firstNode)][int(secondNode)] = line[2]
            
            if firstNode not in self.exist:
                self.exist.append(self.alphabet[int(firstNode)])
            if secondNode not in self.exist:
                self.exist.append(self.alphabet[int(secondNode)])

        infile.close()

    def WriteFile(self, nodeOrder):
        outFile = open(self.outputFile, 'w')
        for node in nodeOrder:
            outFile.write(node)
            outFile.write("\n")


    def GetNeighboors(self, currentNode):
        count = 0
        neighboors = []

        #Goes through current node and checks if it has any neighboors in nodesMatrix
        while(count < len(self.alphabet)):

            #lookup node value in dictionary                                                       
            currentNodeInt = int(self.alphabetDict[currentNode])
            currentNodeMatrix = self.nodesMatrix[currentNodeInt][count]

            #the value is a number, meaning there is a link between the nodes                      
            if ord(currentNodeMatrix[0]) >= 48 and ord(currentNodeMatrix[0]) <= 57:

                if self.alphabet[count] not in self.alreadyVisited:

                    #append to the neighboors list which will be returned at the end of function
                    neighboors.append(self.alphabet[count])

                    #makes traversing list backwards ez pz                                         
                    self.parent[count] = currentNode

            count += 1

        return neighboors

    def DoBFS(self):

        nodeOrder = []
        nodeOrder.append(self.startNode)
        
        theQueue = queue.Queue()

        #if the start node is the node we are looking for end the program right there
        if(self.startNode == self.endNode):
            WriteFile(nodeOrder)
        
        else:
            currentNode = self.startNode
            
            while(currentNode != self.endNode):
                self.alreadyVisited.append(currentNode)

                #return a list of neighboors and make sure that it is populated
                neighboors = self.GetNeighboors(currentNode)

                if(len(neighboors) > 0):
                    neighboors = neighboors[::-1]

                    for i in neighboors:
                        theQueue.put(i)
                        
                currentNode = theQueue.get()


        #traverse list backwards after finding the final node
        self.traverseList()

    def DoDFS(self):

        stack = []
        stack.append(self.startNode)

        while len(stack) != 0:
            current = stack.pop()
            if(current not in self.alreadyVisited):
                self.alreadyVisited.append(current)
                
                neighboors = self.GetNeighboors(current)

                for neighboor in neighboors:
                    if neighboor not in self.alreadyVisited:
                        stack.append(neighboor)

        self.traverseList()
        
    def DoUCS(self):
        
        dist = []

        allNodesChecked = False
        nodeInVisited = True

        for letter in self.alphabet:
            dist.append(99999999)
        

        dist[int(self.alphabetDict[self.startNode])] = 0
            
        lowestNode = 0
        lowestValue = 1
        count = 0
        while allNodesChecked == False:
            #get node with smallest dist[]
            for i in range(len(dist)):
                if ((dist[i] < lowestValue) and (self.alphabet[i] not in self.alreadyVisited) and (self.alphabet[i] in self.exist)):
                    lowestValue = dist[i]
                    lowestNode = i

            #add node to alreadyVisited

            self.alreadyVisited.append(self.alphabet[lowestNode])

            neighboors = self.GetNeighboors(self.alphabet[lowestNode])

            #goes through neighboors
            for neighboor in neighboors:
                newNeighboorDist = dist[lowestNode] + int(self.nodesMatrix[lowestNode][int(self.alphabetDict[neighboor])])

                #updates distance and parent of neighboors if the value is lower than the previous
                if newNeighboorDist < dist[int(self.alphabetDict[neighboor])]:
                    dist[int(self.alphabetDict[neighboor])] = newNeighboorDist

                    self.parent[int(self.alphabetDict[neighboor])] = self.alphabet[lowestNode]

                                                   
            

            #goes through list of nodes
            for i in self.exist:
                #if a node hasn't been visited
                if i not in self.alreadyVisited:
                    nodeInVisited = False
                    
            #if all nodes have been visited
            if nodeInVisited == True:
                allNodesChecked = True

                
            count+=1
            lowestValue = 99999999
            nodeInVisited = True
           
    def traverseList(self):
        backwardsList = []

        currentNode = self.endNode
        while currentNode != self.startNode:
            backwardsList.append(currentNode)

            #current node equals parent of the translated currentnode in alphabetDict
            #so if currentNode = A and Parent of A = B, currentNode now = B
            
            currentNode = self.parent[int(self.alphabetDict[currentNode])]

        backwardsList.append(self.startNode)

        self.WriteFile(backwardsList[::-1])
        

