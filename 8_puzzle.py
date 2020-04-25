class Board:
    def __init__(self,state: list,parent = None,cost= 0,moves = None,depth = 0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.moves = moves
        self.depth = depth

    def print_board(self):
        print("",self.state[0:3],"\n",self.state[3:6],"\n",self.state[6:9],"\n\n")
    
    def move_up(self):
        new_state = list(self.state)
        index = new_state.index(0)
        new_state[index] = self.state[index - 3]
        new_state[index-3] = self.state[index]
        self.state = new_state
        return new_state

    def move_down(self):
        new_state = list(self.state)
        index = new_state.index(0)
        new_state[index] = self.state[index + 3]
        new_state[index+3] = self.state[index]
        self.state = new_state
        return new_state

    def move_left(self):
        new_state = list(self.state)
        index = new_state.index(0)
        new_state[index] = self.state[index - 1]
        new_state[index-1] = self.state[index]
        self.state = new_state
        return new_state

    def move_right(self):
        new_state = list(self.state)
        index = new_state.index(0)
        new_state[index] = self.state[index + 1]
        new_state[index+1] = self.state[index]
        self.state = new_state
        return new_state

    def can_move_up(self):
        index = self.state.index(0)
        if(index in range(0,3)):
            return False
        return True

    def can_move_down(self):
        index = self.state.index(0)
        if(index in range(6,9)):
            return False
        return True

    def can_move_left(self):
        index = self.state.index(0)
        if(index in range(0,7,3)):
            return False
        return True
    
    def can_move_right(self):
        index = self.state.index(0)
        if(index in range(2,9,3)):
            return False
        return True
        

b = Board([1,2,4,3,8,5,7,6,0])
b.print_board()

