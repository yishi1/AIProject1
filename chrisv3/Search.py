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
        print "current = ", current 
        currentLEN = len(dic[current])
        print "currentLEN = ", currentLEN
        print"----------------------"
        for i in range(currentLEN):
            print "!!!!!!!!!!!!!!!!!!!!!!!"
            node = dic[current][i][0]
            print "NODE: ", node

            while node not in result:
                print "IN WHILE NOT IN"
                result.append(node)
                queue.append(node)
                currentQ = queue.index(node)
                if result[-1] == end:
                    print "BREAK"
                    return result
                
            print result
            print "CURRENT = ", current
            print "i=",i
            if i == (currentLEN-1):
                print "VISITED: ", visited
                current = queue[visited]
                print "current in visited = ", current
                visited = visited + 1
                if current not in dic:
                    print "current NOT in dic"
                    current = queue[visited]
            
    #result.append(end)
                
                
    print "QUEUE", queue
    return result
#------------------------------------------


def DFS(dic, strt, end, keys):
    result = []
    stack = [] 
    current = strt
    visited = 0

    print "DFS dic: ", dic

    while ((result == []) or (result[-1] != end)):
        #currentLEN = len(dic[current])


        while current not in result:
            print "result: ", result
            print "current = ", current
            result.append(current)
            stack.append(current)
            if result[-1] == end:
                return result
            currentLEN = len(dic[current])
            print "currentLEN = ", currentLEN
            for i in range(currentLEN):
                #current = dic[current][i][0]
                node = dic[current][i][0]
                print "NODE = ", node
                print "i = ", i
                print "in forLoop, current = ", current
                if node not in result:
                    print "BREAK"
                    print "in BREAK, current = ", current
                    current = dic[current][i][0]
                    break

        print "STACK: ", stack
        stack = stackPOP(stack)
        current = stack[-1]
        print "stack[-1] = ", current
        currentLEN = len(dic[current])
        print "LEN = ",currentLEN
        print "CURRENT = ", current
        current2 = current
        for i in range(currentLEN):
            print "-------------------------------_"
            node2 = dic[current2][i][0]
            print "i = ", i
            print "LEN2 = ", currentLEN
            #current = dic[current][i][0]
            #print current
            print "node2 = ", node2
            #if current not in result:
            if node2 not in result:
                print "CURRENT not in result"
                current = dic[current2][i][0]
                break
            else:
                print "current in result"
                current = dic[current][i][0]
                if i == (currentLEN-1):
                    current = dic[current][i][0]
    return result



def UCS(dic, strt, end, keys):
    print"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
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
    print "currentLEN1 = ", currentLEN

    #adding the starting node and its kids to the queue
    for i in range(currentLEN):
        temp = []
        temp.append(current)
        temp.append(dic[current][i][0])
        temp.append(dic[current][i][1])
        queue.append(temp)
        print "TEMP1 = ", temp

    explored.append(queue[0][0])
    queue.sort(key=lambda x: x[-1])

    flag = True
    #will hold the frontier node of the...
    #sequence that has the lowest cost
    lowest = 'X'
    while flag:
        temp = queue[0]
        temp2 = queue[0]
        print "temp2 = ", temp2
        print "in while flag"
        lowest = queue[0][-2]
        explored.append(lowest)

        #sees if lowest has children
        while lowest not in dic:
            print "lowest not in dic"
            queue.pop(0)
            lowest = queue[0][-2]

        print "LOWEST = ", lowest
        #temp2 = queue[0]
        #temp2 = temp
        currentLEN = len(dic[lowest])
        print "currentLEN = ", currentLEN
        for i in range(currentLEN):

            print "-----------------"
            print "TEMP = ", temp
            print "queue = ", queue
            print "i = ", i
            if dic[lowest][i][0] in explored:
                print "LOWEST in EXPLORED"
                continue
            else:
                #queue.pop(0)
                print "else TEMP = ", temp
                temp[-1] = temp[-1] + dic[lowest][i][1]
                print "queue1 = ", queue
                temp.insert(-1, dic[lowest][i][0])
                print "queue2 = ", queue
                print "inserting...", dic[lowest][i][0]
                print "TEMP = ", temp
                queue.append(temp)
                queue.sort(key=lambda x: x[-1])
                print "QUEUE = ", queue
                #temp = []
                #print "LOWEST = ", lowest


        queue.sort(key=lambda x: x[-1])
        print "AFTER SORT = ", queue
        

        if queue[0][-2] == end:
            print "queue[0][-2] == end"
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

    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    numArg = len(sys.argv)
    print "numARG = ", numArg
    

    for i in range(numArg):
        print str(sys.argv[i])

    inputFile = str(sys.argv[1])
    output = str(sys.argv[2])
    startNode = str(sys.argv[3])
    endNode = str(sys.argv[4])
    searchType = str(sys.argv[5])

    print "inputFile = ", inputFile
    print "output = ", output
    print "startNode = ", startNode
    print "endNode = ", endNode
    print "searchType = ", searchType  

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
        print parsed
        listOfLists.append(parsed)


    print listOfLists
    listOfLists.sort()
    print "sorted: ", listOfLists
    listLen = len(listOfLists)

    d = dict();

    print listOfLists[1][1]
    print "LEN: ", listLen

    for i in range(listLen):
        temp = []
        temp.append(listOfLists[i][1])
        temp.append(listOfLists[i][2])
        if listOfLists[i][0] in d:
            d[listOfLists[i][0]].append(temp)
        else:
            d[listOfLists[i][0]] = []
            d[listOfLists[i][0]].append(temp)


    print d

    dLEN = len(d)

    keys = list(d.keys())
    keys.sort()
    print "KEYS", keys
   



    for j in range(dLEN):
        print "KEY", keys[j]
        for i in range(len(d[keys[j]])):
            d[keys[j]][i][1] = int(d[keys[j]][i][1])
            print "VALUES", d[keys[j]][i][1]
            

    print d


    print "***************STARTING BFS*****************"

    writeTo = open(output, 'w')

    if searchType == "BFS":
        result = BFS2(d, 'A', 'D', keys)
        print "BFS = ", result

        for i in range(len(result)):
            writeTo.write(result[i])
            writeTo.write("\n")

    if searchType == "DFS":
        result = DFS(d, 'A', 'D', keys)
        print "DFS = ", result

        for i in range(len(result)):
            writeTo.write(result[i])
            writeTo.write("\n")

    if searchType == "UCS":
        result = UCS(d, 'A', 'F', keys)
        print "UCS = ", result

        for i in range(len(result)-1):
            print result[i]
            writeTo.write(result[i])
            writeTo.write("\n")

    writeTo.close()


    
    #baseTenList will be a list taken from the toBase10() function. 
    #this list will hold the base 10 ASCII values or ".." of the file
    #ASCII values should be integers
  #  baseTenList = toBase10(textfile)

   


main()


