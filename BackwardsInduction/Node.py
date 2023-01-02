class Node:
    
    # purpose: to initialize a node object
    # parameters: player (the player at the node), payoffs (the payoffs at a node. 'x' if 
    # internal)
    def __init__(self, player, payoffs, ID):
        #initializes the variable that will keep track of the node's descendants
        self.actions = []

        self.ID = ID

        # if the node is terminal, player=='x'
        if player == 'x':
            self.player = -1
        else:
            self.player = player
        
        # if the node is internal, payoffs=='x'
        if payoffs == 'x':
            self.payoffs = []
        else:
            self.payoffs = payoffs