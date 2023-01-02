from pathlib import Path
from Node import Node


class IndTree:

    # purpose: opens a file, creates the game's root, and calls gameBuild
    # parameters: the name of the game file to be opened
    def __init__(self, game):
        p = Path(__file__).with_name(game)

        with p.open('r') as tfile:
            self.numPlayers = -1
            self.edges = []
            self.numNodes = 0
            self.nodes = []

            #creates the game's root
            rawLine = tfile.readline()
            self.root = self.nodeBuild(rawLine)

            #creates the game's nodes
            self.gameBuild(tfile, self.root)

        #finds a subgame perfect equilibrium and stores the strategies in self.edges
        self.findSPE(self.root)

        #sorts the SPE actions to reduce worst case query asymptotic time complexity
        self.edges = sorted(self.edges, key=lambda tup: tup[0])

    # Name: gameBuild
    # purpose: to initialize all nodes in the gametree
    # parameters: tfile (file from which the nodes and their relationships will be read), 
    # root (the root of the current subgame)
    # returns: none
    def gameBuild(self, tfile, root):
        rawLine = tfile.readline().rstrip()
        
        # adds a descendant to the subgame rooted at 'root' provided the input isn't
        # '.' or ""
        while rawLine != "." and rawLine != "":
            newNode = self.nodeBuild(rawLine)
            root.actions.append(newNode)
            self.gameBuild(tfile, newNode)
            rawLine = tfile.readline().rstrip()

    # Name: nodeBuild
    # purpose: to parse a string read from the file into a node
    # parameters: the string to be parsed
    # returns: a new node based on the inputted string
    # Note!!! does not handle the '.' input. That must be done natively   
    def nodeBuild(self, rawLine):
        self.numNodes = self.numNodes + 1

        # splits the player and payoffs
        splitLine = rawLine.split()

        if splitLine[0] == 'x':
            Player = splitLine[0]
        else:
            Player = int(splitLine[0])

        # stores the payoffs for the node as a list or indicates an internal node
        Payoffs = splitLine[1]
        if Payoffs == 'x':
            Payoffs = 'x'
        else:
            Payoffs = Payoffs.split(",")
            for i in range(0, len(Payoffs)):
                Payoffs[i] = int(Payoffs[i])

            if self.numPlayers == -1:
                self.numPlayers = len(Payoffs)

        newNode = Node(Player, Payoffs, self.numNodes)
        self.nodes.append(newNode)
        return newNode
    
# Name: findSPE
# purpose: to find a subgame perfect equilibrium for the game (both payoffs and actions)
# parameters: the current subgame's root
# returns: none
    def findSPE(self, root):
        maxPayoffs = [float('-inf')] * self.numPlayers
        SPE_action = -1

        for action in root.actions:
            # if the action's SPE payoffs have not been determined yet, do so recursively
            if len(action.payoffs) == 0:
                self.findSPE(action)

            actionPayoff = action.payoffs[root.player - 1]

            # finds the action that gives the player a SPE payoff 
            if actionPayoff > maxPayoffs[root.player - 1]:
                maxPayoffs = action.payoffs
                SPE_action = action.ID
        # sets the node's SPE payoffs
        root.payoffs = maxPayoffs

        # notes the edge taken to get to SPE payoff and stores in self.edges
        SPE_edge = (root.ID, SPE_action)
        self.edges.append(SPE_edge)


# Name: equilibrate
# purpose: to report a path from the given node to a terminal node that is part of a SPE
# parameters: the ID number of the start node (from 1 to n)
# returns: none
    def equilibrate(self, ID):
        try:
            #faults exception
            self.nodes[ID - 1]

            print("Your path is: ", end=" ")

            #prints path to internal node
            curr = ID 
            for x in self.edges:
                if x[0] == curr:
                    print(x, end=" "),
                    curr = x[1]
            
            # if the original node is terminal, print its path
            if curr == ID:
                print("(" + str(ID) + ", " + str(ID) + ")", end="")

            # print payoffs on a seperate line
            print("")
            print("Your payoffs are: ", self.nodes[curr - 1].payoffs)

        except IndexError:
            print("Indalid index!")
            print("Allowable range is [" + str(1) + ", " + str(self.numNodes) + "]")