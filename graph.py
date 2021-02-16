### graph.py
### an implementation of a graph using an adjacency list.

## helper class representing a node in a graph. For the moment, nodes
## only have names. Later, we will add state variables.

class Node():
    def __init__(self, n):
        self.name = n

    def __hash__(self):
        return hash(self.name)

### an edge is a link between two nodes. Right now, the only other
### information an edge carries is the weight of the link. Later we
### will add other annotations.


class Edge():
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

### The graph class itself.
### The nodeTable is a dictionary that maps names to Node objects.
### (this keeps us from having to repeatedly search edgeMap.keys())

### The edgeMap is a dictionary that maps nodes to lists of Edges emanating from that node.

class Graph() :

    def __init__(self):
        self.nodeTable = {}
        self.edgeMap = {}

    ### implements the 'in' keyword. Returns true if the node is in the graph.
    def __contains__(self, item):
        return item in self.nodeTable

    def getNode(self, src):
        return self.nodeTable[src] # Adjusted method since professor made mistake and wrote nodeList here

    def addNode(self, src):
        if src not in self.nodeTable :
            self.nodeTable[src] = Node(src)

    def getEdge(self, src):
        return self.edgeMap[src]

    def addEdge(self, src, dest, weight):
        e = Edge(src,dest,weight)
        self.addNode(src)
        self.addNode(dest)
        if src in self.edgeMap :
            self.edgeMap[src].append(e)
        else :
            self.edgeMap[src] = [e]

    def addInvertEdge (self, src, dest, weight):
        e = Edge(dest,src,weight)
        self.addNode(src)
        self.addNode(dest)
        if dest in self.edgeMap :
            self.edgeMap[dest].append(e)
        else :
            self.edgeMap[dest] = [e]

    # Return list of neighbor nodes. Input: String
    def getNeighborNodes(self, src):
        nodeList = []
        edgeList = self.getEdge(src)
        for edge in edgeList:
            nodeList.append(self.getNode(edge.dest).name)
        return nodeList

    # Return distance between an edge
    def getDistance(self, src, dest):
        for edge in self.getEdge(src):
            if edge.dest == dest:
                return float(edge.weight)
        return float("inf")



    ## Assume file is in the mtx format: % is a comment
    ## Otherwise it's source destination weight
    ### The file in the github repo will work as a sample for you.
    ### It's in the format: source, vertex, weight. You should assume that the graph is symmetric -
    ### if there's an edge from a to b, there's an edge from b to a.
    ### You can find lots of others here: http://networkrepository.com/index.php
    def readFromFile(self, fname):
        with open(fname) as f :
            for l in f.readlines() :
                if not l.startswith("%") :
                    (s,d,w) = l.split()
                    self.addEdge(s,d,w)
                    self.addInvertEdge(s,d,w) # Adjust readFromFile to make it create undirected graph

    ### inputs are the name of a startNode and endNode. Given this,
    ### return a list of Nodes that indicates the path from start to finish, using breadth-first search.

    def breadthFirstSearch(self, startNode, endNode):

        if startNode == endNode: return # No need to find

        # 1. Create tree using breadthFirstSearch
        searchQueue = [startNode]
        searchedList = [startNode]
        parentList = []

        while searchQueue: # There should always be something in queue if all nodes are not yet to be reached
            targetNode = searchQueue.pop(0) # Deque one node
            #print "Current target is " + targetNode
            neighbors = self.getNeighborNodes(targetNode) # Get neighbors
            for neighbor in neighbors:
                #print "Testing neighbor " + neighbor
                if neighbor not in searchedList: # avoid repeating
                    searchQueue.append(neighbor)
                    searchedList.append(neighbor)
                    parentList.append([neighbor, targetNode]) # parentList is used to track backwards of the tree

        # 2. Trace backward from endNode
        solutionQueue = [endNode]
        while solutionQueue[-1]!=startNode:
            for parent in parentList:
                if parent[0] == solutionQueue[-1]:
                    solutionQueue.append(parent[1])
        return solutionQueue

    ### inputs are the name of a startNode and endNode. Given this,
    ### return a list of Nodes that indicates the path from start to finish, using depth-first search.

    def depthFirstSearch(self, startNode, endNode):

        if startNode == endNode: return # No need to find

        # 1. Create tree using depthFirstSearch
        searchStack = [startNode]
        searchedList = [startNode]
        parentList = []

        while searchStack:
            targetNode = searchStack.pop()
            #print "Current target is "+targetNode
            neighbors = self.getNeighborNodes(targetNode)  # Get neighbors
            for neighbor in neighbors:
                #print "Testing neighbor "+neighbor
                if neighbor not in searchedList: # avoid repeating
                    searchStack.append(neighbor)
                    searchedList.append(neighbor)
                    parentList.append([neighbor, targetNode]) # parentList is used to track backwards of the tree

        # 2. Trace backward from endNode
        solutionQueue = [endNode]
        while solutionQueue[-1] != startNode:
            for parent in parentList:
                if parent[0] == solutionQueue[-1]:
                    solutionQueue.append(parent[1])
        return solutionQueue


    ### implement Djikstra's all-pairs shortest-path algorithm.
    ### https://yourbasic.org/algorithms/graph/#dijkstra-s-algorithm
    ### return the array of distances and the array previous nodes.

    def djikstra(self, startNode):

        # Create tree using Dijkstra's search
        searchStack = [startNode]
        searchedList = [startNode]
        distList = []
        parentList = []
        for node in self.nodeTable:
            distList.append([node, float('inf')])
            parentList.append([node, ""]) # I tried to make it null (none), but it won't print very well on console

        # Make dist to source 0
        targetDist = next(dist for dist in distList if dist[0] == startNode)
        targetDist[1] = 0

        while searchStack:
            # Initialize targetNode
            targetNode = searchStack[0]
            targetDist = next(dist for dist in distList if dist[0] == targetNode)

            #Adjust targetNode to the one within the stack and with shortest dist
            for node in searchStack:
                newTargetDist = next(dist for dist in distList if dist[0] == node)
                if newTargetDist[1] < targetDist[1]:
                    targetNode = newTargetDist[0]
                    targetDist = newTargetDist

            #Pop that node away from searchStack, and add it to the searchedLIst
            searchStack.pop(searchStack.index(targetNode))
            searchedList.append(targetNode)

            neighbors = self.getNeighborNodes(targetNode)  # Get neighbors
            for neighbor in neighbors:
                if neighbor not in searchedList: # Avoid repeat

                    # Put neighbor into stack
                    if neighbor not in searchStack:
                        searchStack.append(neighbor)

                    # Update neighbor's distance toward targetNode, if shorter than current one
                    neighborDist = next(dist for dist in distList if dist[0] == neighbor)
                    numberOfDistFromNeighborToTarget = self.getDistance(neighbor, targetNode)
                    numberOfDistFromNeighborToStart = numberOfDistFromNeighborToTarget + targetDist[1]

                    if numberOfDistFromNeighborToStart < neighborDist[1]:
                        neighborParent = next(parent for parent in parentList if parent[0] == neighbor)
                        neighborParent[1] = targetNode
                        neighborDist[1] = numberOfDistFromNeighborToTarget + targetDist[1]
        return parentList

    ### takes as input a starting node, and computes the minimum spanning tree, using Prim's algorithm.
    ### https:// en.wikipedia.org/wiki/Prim % 27s_algorithm
    ### you should return a new graph representing the spanning tree generated by Prim's.
    def prim(self, startNode):


        nodeAdded = [startNode] # It should contain all node in final tree
        nodeNotAdded = [] # This should contains everything else
        parentList = []

        for node in self.nodeTable:
            nodeNotAdded.append(node)
            parentList.append([node, ""]) # I tried to make it null (none), but it won't print very well on console
        nodeNotAdded.pop(nodeNotAdded.index(startNode))

        while (nodeNotAdded):
            searchEdgeList = []  # Create an edge list since we are comparing lot of edges.
            for node in nodeAdded:
                tempEdgeList = self.getEdge(node)
                for edge in tempEdgeList:
                    if edge.dest in nodeNotAdded:
                        searchEdgeList.append(edge)
                        # print(edge.src + "->" + edge.dest + " is added to searchEdgeList.")
            targetEdge = searchEdgeList[0]
            if  searchEdgeList:
                for edge in searchEdgeList:
                    # print("COMPARE "+edge.weight+"and target weight which is: "+targetEdge.weight)
                    if float(edge.weight) < float(targetEdge.weight):
                        targetEdge = edge
            # print(targetEdge.src+"->"+targetEdge.dest+" is final edge to add to tree.")
            neighborParent = next(parent for parent in parentList if parent[0] == targetEdge.dest)
            neighborParent[1] = targetEdge.src

            nodeAdded.append(targetEdge.dest)
            nodeNotAdded.pop(nodeNotAdded.index(targetEdge.dest))

        return parentList


    ### 686 students only ###
    ### takes as input a startingNode and returns a list of all nodes in the maximum clique containing this node.
    ### https://en.wikipedia.org/wiki/Clique_problem#Finding_a_single_maximal_clique

    def clique(self, startNode):
        cliqueList = []
        searchQueue = [startNode]

        while searchQueue:
            nextNode = searchQueue.pop(0)
            nextNodeNeighbors = self.getNeighborNodes(nextNode)
            isInClique = True

            # Only add node when it is neighbor of everything in clique
            for node in cliqueList:
                if node not in nextNodeNeighbors:
                    isInClique = False
            if isInClique:
                cliqueList.append(nextNode)
                # All neighbors of new member becomes member on queue
                for neighbor in nextNodeNeighbors:
                    searchQueue.append(neighbor)

        return cliqueList



if __name__ == '__main__':
    graph1 = Graph()
    graph1.readFromFile("testMap.edges")
    graph2 = Graph()
    graph2.readFromFile("testMap2.edges")

    # Since graph 2 is better than graph 1 all tests below will use graph 2.
    # Answer# is number of problem related to the test (4-1, 4-2, etc.)

    answer1 = graph2.breadthFirstSearch("A", "H")
    print("breadthFirstSearch result: "+"->".join(answer1))
    answer2 = graph2.depthFirstSearch("A","H")
    print("depthFirstSearch result: " + "->".join(answer2))
    answer3 = graph2.djikstra("A")
    print("djikstra result (showing arrow TOWARDS startNode):")
    for thing in answer3:
        print("->".join(thing))
    answer4 = graph2.prim("A")
    print("prim result (showing arrow TOWARDS startNode):")
    for thing in answer4:
        print("->".join(thing))
    answer5 = graph2.clique("C")
    print("clique result: " + ",".join(answer5))
    answer52 = graph2.clique("F")
    print("clique result #2: " + ",".join(answer52))