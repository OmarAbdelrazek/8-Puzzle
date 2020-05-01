import time
import sys
from math import sqrt
from collections import deque
import heapq

goal = [0,1,2,3,4,5,6,7,8]
nodes_expanded = 0
moves =[]
explored = {}
frontier = []
board_length = 0
board_side = 0
frontier_U_explored = set()

class Board:
    def __init__(self,state: list,parent = None,move = "initial",cost= 0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.move = move
        self.key = 0
        
        

    def print_board(self):
        print(""+str(self.state[0:3])+"\n"+str(self.state[3:6])+"\n"+str(self.state[6:9])+"\n\n" )
        pass
    
    def move_up(self):
        new_state = list(self.state)
        index = new_state.index(0)
        new_state[index] = self.state[index - 3]
        new_state[index-3] = self.state[index]
        return Board(new_state, self, "up",self.cost + 1)

    def move_down(self):
        new_state = list(self.state)
        index = new_state.index(0)
        new_state[index] = self.state[index + 3]
        new_state[index+3] = self.state[index]
        return Board(new_state,  self, "down", self.cost +1 )

    def move_left(self):
        
        new_state = list(self.state)
        index = new_state.index(0)
        new_state[index] = self.state[index - 1]
        new_state[index-1] = self.state[index]
        # self.state = new_state
        return Board(new_state,  self, "left",self.cost + 1)

    def move_right(self):
        new_state = list(self.state)
        index = new_state.index(0)
        new_state[index] = self.state[index + 1]
        new_state[index+1] = self.state[index]
        # self.state = new_state
        return Board(new_state, self, "right",self.cost + 1)

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
    def get_parent(self):
        return self.parent

    def __eq__(self, other):
        return self.state == other.state
    def __lt__(self, other):
        return self.key < other.key


def get_neighbors(board :Board):
    global nodes_expanded
    neighbors = []
    nodes = []
    if  board.can_move_up() == True :
        neighbors.append(board.move_up())
        nodes_expanded += 1

    if board.can_move_down()== True :
        neighbors.append(board.move_down())
        nodes_expanded += 1
    if board.can_move_left()== True :
        neighbors.append(board.move_left())
        nodes_expanded += 1
    if board.can_move_right()== True :
        neighbors.append(board.move_right())
        nodes_expanded += 1

    return neighbors


def get_path(my_goal):
    while my_goal.move != "initial":
        moves.append(my_goal.move)
        my_goal = my_goal.parent
    return


def BFS(initial_board, goal_board_state):
    frontier_U_explored = set()
    frontier_U_explored.add(str(initial_board.state))    
    frontier.append(initial_board)
    while frontier:
        b = frontier.pop(0)
        if b.state == goal_board_state:
            return b
        neighbours = get_neighbors(b)
        for neighbour in neighbours:
            if  str(neighbour.state) not in frontier_U_explored:
                frontier_U_explored.add(str(neighbour.state))
                frontier.append(neighbour)
    return "fail"

def DFS(initial_board, goal_board_state):
    frontier_U_explored = set()
    frontier_U_explored.add(str(initial_board.state))    
    frontier.append(initial_board)
    while frontier:
        b = frontier.pop()
        if b.state == goal_board_state:
            return b
        neighbours = get_neighbors(b)
        for neighbour in neighbours:
            if  str(neighbour.state) not in frontier_U_explored:
                frontier_U_explored.add(str(neighbour.state))
                frontier.append(neighbour)
    return "fail"

def manhattan_distance(state):
    global board_length,board_side
    return sum(abs(b % board_side - g % board_side) + abs(b//board_side - g//board_side) for b, g in ((state.index(i), goal.index(i)) for i in range(1, board_length)))

def euclidean_distance(state):
    global board_length
    return sum(sqrt(pow(b % board_side - g % board_side,2)) + sqrt(pow(b//board_side - g//board_side,2)) for b, g in ((state.index(i), goal.index(i)) for i in range(1, board_length)))


def aStar_euclidean(initial_board, goal_board_state):
    heap_entry = {}
    key = euclidean_distance(initial_board.state)
    entry = (key,initial_board.state,initial_board)
    heapq.heappush(frontier,entry)
    frontier_U_explored = set()
    heap_entry[str(initial_board.state)] = entry
    while frontier:
        b = heapq.heappop(frontier)
        frontier_U_explored.add(str(b[2].state))
        if b[2].state == goal_board_state:
            return b[2]
        neighbours = get_neighbors(b[2])
        for neighbor in neighbours:
            neighbor.key = neighbor.cost + euclidean_distance(neighbor.state)
            entry = (neighbor.key, neighbor.move, neighbor)
            if  str(neighbor.state) not in frontier_U_explored:
                frontier_U_explored.add(str(neighbor.state))
                heapq.heappush(frontier,entry)
                heap_entry[str(neighbor.state)] = entry
            elif str(neighbor.state) in heap_entry and neighbor.key < heap_entry[str(neighbor.state)][2].key:
                hindex = frontier.index((heap_entry[str(neighbor.state)][2].key,heap_entry[str(neighbor.state)][2].move,heap_entry[str(neighbor.state)][2]))
                frontier[int(hindex)] = entry
                heap_entry[str(neighbor.state)] = entry
                heapq.heapify(frontier)
    return "fail"


def aStar_manhattan(initial_board, goal_board_state):
    heap_entry = {}
    key = manhattan_distance(initial_board.state)
    entry = (key,initial_board.state,initial_board)
    heapq.heappush(frontier,entry)
    heap_entry[str(initial_board.state)] = entry
    while frontier:
        b = heapq.heappop(frontier)
        frontier_U_explored.add(str(b[2].state))
        if b[2].state == goal_board_state:
            return b[2]
        neighbours = get_neighbors(b[2])
        for neighbor in neighbours:
            neighbor.key = neighbor.cost + manhattan_distance(neighbor.state)
            entry = (neighbor.key, neighbor.move, neighbor)
            if  str(neighbor.state) not in frontier_U_explored:
                frontier_U_explored.add(str(neighbor.state))
                heapq.heappush(frontier,entry)
                heap_entry[str(neighbor.state)] = entry
            elif str(neighbor.state) in heap_entry and neighbor.key < heap_entry[str(neighbor.state)][2].key:
                hindex = frontier.index((heap_entry[str(neighbor.state)][2].key,heap_entry[str(neighbor.state)][2].move,heap_entry[str(neighbor.state)][2]))
                frontier[int(hindex)] = entry
                heap_entry[str(neighbor.state)] = entry
                heapq.heapify(frontier)
    return "fail"

def print_output(final_state,running_time):
    global nodes_expanded
    print("Path to goal: ",moves)
    print("Cost of path: ",final_state.cost)
    print("Search depth: ",final_state.cost)
    print("Nodes expanded: ",(nodes_expanded))
    print("Running time: ",running_time)


def main():
    global goal,moves,board_length,board_side
    start_time = time.time()
    b = Board([8,6,4,2,1,3,5,7,0],"root")
    board_length = len(b.state)
    board_side = int(board_length ** 0.5)


    #A-star using euclidean formula
    final_state = aStar_euclidean(b,goal)


    #A-star using manhattan formula
    final_state = aStar_euclidean(b,goal)


    #DFS
    final_state = DFS(b,goal)


    #BFS
    final_state = BFS(b,goal)
    


    get_path(final_state)
    moves.reverse()
    running_time = time.time() - start_time
    print_output(final_state,running_time)

if __name__ == "__main__":
    main()