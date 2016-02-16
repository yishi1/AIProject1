# File name: Search.py
# Author: Christine Vu
# Date: Feb 10, 2016
# Email: chrisv3@umbc.edu
# Description: DFS|BFS|UCS search methods



    
#!/usr/bin/python3

#keys passed in are already sorted
def BFS2(dic, strt, end, keys):
    result = []
    queue = []
    current = strt
    currentKeyIndex = keys.index(current)
    result.append(current)
    visited = 0


    while (result[-1] != end): 
        currentLEN = len(dic[current])
        for i in range(currentLEN):
            node = dic[current][i][0]

            while node not in result:
                result.append(node)
                queue.append(node)
                currentQ = queue.index(node)
                if result[-1] == end:
                    return result
                

            if i == (currentLEN-1):
                current = queue[visited]
                visited = visited + 1
                if current not in dic:
                    current = queue[visited]
            
    #result.append(end)
                
                
    return result
#------------------------------------------


def DFS(dic, strt, end, keys):
    result = []
    stack = [] 
    current = strt
    visited = 0


    while ((result == []) or (result[-1] != end)):
        #currentLEN = len(dic[current])


        while current not in result:
            result.append(current)
            stack.append(current)
            if result[-1] == end:
                return result
            currentLEN = len(dic[current])
            for i in range(currentLEN):
                #current = dic[current][i][0]
                node = dic[current][i][0]

                if node not in result:
                    current = dic[current][i][0]
                    break

        stack = stackPOP(stack)
        current = stack[-1]
        currentLEN = len(dic[current])
        current2 = current
        for i in range(currentLEN):
            node2 = dic[current2][i][0]
            #if current not in result:
            if node2 not in result:
                current = dic[current2][i][0]
                break
            else:
                current = dic[current][i][0]
                if i == (currentLEN-1):
                    current = dic[current][i][0]
    return result



def UCS(dic, strt, end, keys):

    result = []
    explored = []
    queue = []

    current = strt

    #-------checking strt-------
    #if start node doesn't have children
    if current not in dic:
        return strt, " has no children to explore!"

    #False if end is not a child
    isPointedto = True
    for key in dic:
        for i in range(len(dic[key])):
            if end not in dic[key][i]:
                False

    if isPointedto == False:
        return end, " is not a child!"
    #-----------------------------------

    currentLEN = len(dic[current])

    #adding the starting node and its kids to the queue
    for i in range(currentLEN):
        temp = []
        temp.append(current)
        temp.append(dic[current][i][0])
        temp.append(dic[current][i][1])
        queue.append(temp)

    explored.append(queue[0][0])
    queue.sort(key=lambda x: x[-1])

    flag = True
    #will hold the frontier node of the...
    #sequence that has the lowest cost
    lowest = 'X'
    while flag:
        temp = queue[0]
        #OG = copy.copy(queue[0])
        OG = queue[0][:]
        lowest = queue[0][-2]
        explored.append(lowest)

        #sees if lowest has children
        while lowest not in dic:
            queue.pop(0)
            lowest = queue[0][-2]

    
        currentLEN = len(dic[lowest])
        num = queue[0][-1]
        
        for i in range(currentLEN):

            if dic[lowest][i][0] in explored:
                continue
            else:
                temp[-1] = temp[-1] + dic[lowest][i][1]
                temp.insert(-1, dic[lowest][i][0])
                queue.append(temp)
                queue.sort(key=lambda x: x[-1])
                if queue[0][-2] == end:
                    return queue[0]
                temp = OG
                


        queue.sort(key=lambda x: x[-1])
        

        if queue[0][-2] == end:
            flag = False

    return queue[0]



def queuePOP(queue):
    queue.pop(queue[0])

    return queue

def stackPOP(stack):
    stack.pop(-1)

    return stack





# main()
# where all functions come together with loops and interact with the user
# no input
def main():

    import sys
    import collections

    numArg = len(sys.argv)

    

    inputFile = str(sys.argv[1])
    output = str(sys.argv[2])
    startNode = str(sys.argv[3])
    endNode = str(sys.argv[4])
    searchType = str(sys.argv[5])

    

    #prints greeting
 #   printGreeting()

    # sets condition for while loop
    happy = True
    #while loop:
    while happy:
        #starts a try body.
        try:
            #asks users for the text to open. This will be asked over and...
            #...over again until the user enters a file that exists
        
            #once the file is recognized, the file will open in read mode
            textfile = open(str(sys.argv[1]), "r")
            #while loop will close
            happy = False
        #if user enters a file tthat does not exist, then it will loop again.
        except OSError:
            happy = True

    #will hold list of lists
    listOfLists = []


    #parsing
    for line in textfile:
        parsed = line.split(" ")
        parsed[2] = parsed[2].rstrip()
        listOfLists.append(parsed)


    listOfLists.sort()
    listLen = len(listOfLists)

    d = dict();


    for i in range(listLen):
        temp = []
        temp.append(listOfLists[i][1])
        temp.append(listOfLists[i][2])
        if listOfLists[i][0] in d:
            d[listOfLists[i][0]].append(temp)
        else:
            d[listOfLists[i][0]] = []
            d[listOfLists[i][0]].append(temp)


    

    dLEN = len(d)

    keys = list(d.keys())
    keys.sort()
   



    for j in range(dLEN):
        for i in range(len(d[keys[j]])):
            d[keys[j]][i][1] = int(d[keys[j]][i][1])
            
        


    writeTo = open(output, 'w')

    if searchType == "BFS":
        result = BFS2(d, startNode, endNode, keys)
        print "BFS = ", result

        for i in range(len(result)):
            writeTo.write(result[i])
            writeTo.write("\n")

    if searchType == "DFS":
        result = DFS(d, startNode, endNode, keys)
        print "DFS = ", result

        for i in range(len(result)):
            writeTo.write(result[i])
            writeTo.write("\n")

    if searchType == "UCS":
        result = UCS(d, startNode, endNode, keys)
       

        for i in range(len(result)-1):
            writeTo.write(result[i])
            writeTo.write("\n")

    writeTo.close()


    
    

   


main()


