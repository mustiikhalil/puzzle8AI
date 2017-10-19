# Solves a randomized 8-puzzle using A* algorithm with plug-in heuristics

"""
Name: Mustafa Khalil
ID: 140201100

"""
import random
import math
from collections import deque

finishState = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8]]

# finishState = [[1, 2, 3],
#                [4, 5, 6],
#                [7, 8, 0]]

def index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
    try:
        return seq.index(item)
    except:
        return -1

class Puzzle8:

    def __init__(self):
        # heuristic value
        self._hval = 0
        # search depth of current instance
        self._depth = 0
        # parent node in search path
        self._parent = None
        # the action (i.e., the direction of the move) that has applied to the parent node.
        self.direction = None 
        self.matrix = []
        for i in range(3):
            self.matrix.append(finishState[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.matrix == other.matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.matrix[row]))
            res += '\r\n'
        return res
    
    def change_state(self, l):
        """ change the state of the current puzzle to l"""
        if len(l) != 9:
            print('length of the list should be 9')
        self.matrix = []    
        for i in range(3):
            self.matrix.append(l[i*3:i*3+3])


    def clone(self):
        """ Create a copy of the existing puzzle"""
        p = Puzzle8()
        for i in range(3):
            p.matrix[i] = self.matrix[i][:]
        return p

    def getLegalMoves(self):
        """ Returns the set of available moves as a list of tuples, each tuple contains the row and col position 
        with which the free space (0) may be swapped """
        # get row and column of the empty piece
        row, col = self.find(0)
        free = []

        # find which pieces can move there
        if row > 0:
            free.append((row - 1, col, 'up'))

        if row < 2:
            free.append((row + 1, col, 'down'))
        if col > 0:
            free.append((row, col - 1, 'left'))
        if col < 2:
            free.append((row, col + 1, 'right' ))

        return free
       
    
    def generateMoves(self):
        """ Returns a set of puzzle objects that are successors of the current state   """
        free = self.getLegalMoves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self.clone()
            p.swap(a,b[0:2])
            p.direction = b[2] # up, down, left or right
            p._depth = self._depth + 1
            p._parent = self
            return p
        # map applies the function swap_and_clone to each tuple in free, returns a list of puzzle objects

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def generateSolutionPath(self, path):
        """ construct the solution path by recursively following the pointers to the parent  """
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent.generateSolutionPath(path)



    def shuffle(self, step_count):
        """shuffles the puzzle by executing step_count number of random moves"""
        for i in range(step_count):
            row, col = self.find(0)
            free = self.getLegalMoves()
            target = random.choice(free)
            self.swap((row, col), target[0:2])
            row, col = target[0:2]

    def find(self, value):
        """returns the row, col coordinates of the specified value
           in the graph"""
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.matrix[row][col] == value:
                    return row, col

    def peek(self, row, col):
        """returns the value at the specified row and column"""
        return self.matrix[row][col]

    def poke(self, row, col, value):
        """sets the value at the specified row and column"""
        self.matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        """swaps values at the specified coordinates"""
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)
        
    def isGoal(puzzle):
        """check if we reached  the goal state"""
        return puzzle.matrix == finishState



    ## Breath first Search algorithm to that will solve the puzzle by
    ## Generating the moves and running through them.

    def BFS(self):

        ## frontier is a queue First in first out

        frontier = deque()

        ## Explored is a dictionary to hold the explored sets since an infinite loop can accrue
        ## A dictionary was picked since we can hash the value and get a O(1) access time for it
        explored = {}

        ## counts the amount of nodes that are explored
        counter = 0

        ## according to BFS algorithm we need to append the first node in the frontier to explore it later
        frontier.append(self)

        ## Measures the depth
        depth = self._depth

        ## if the frontier is empty it exits, which means the solution wasn't found.
        while frontier.__len__() != 0:

            ## popping the first element in the queue
            node = frontier.popleft()
            ## adding the hash node into the explored set
            explored[node.__str__()] = True
            counter += 1

            ## check if we are in the goal state
            if node.matrix == finishState:

                ## gets the path by generating the solution path. and adding them to the path array
                path = []
                for child in node.generateSolutionPath([]):
                    path.append(child.direction)
                path.reverse()

                ## exporting the information gathered for the question into a txt file.
                file = open('bfsoutput.txt', 'w')
                file.writelines(f'path_to_goal: {path}\n')
                file.writelines(f'cost_of_path: {path.__len__()}\n')
                file.writelines(f'nodes_expanded: {counter}\n')
                file.writelines(f'search_depth: {path.__len__()}\n')
                file.writelines(f'max_search_depth: {depth}\n')
                file.close()
                return True

            ## generate the moves that are available.
            for child in node.generateMoves():

                ## checks of the node is in the explored set
                if child.__str__() not in explored:

                    ## gets the depth that we are at.
                    if depth < child._depth:
                        depth = child._depth

                    ## appends the available move to the frontier. so we can explore it later
                    frontier.append(child)

        return False


    ## Depth first Search algorithm to that will solve the puzzle by
    ## Generating the moves and running through them.

    def DFS(self):

        ## frontier is a queue First in first out
        frontier = []

        ## a frontier set since we need to check if the node is in the frontier or not. Like this we can has the node
        ## get an access time of O(1) instead of running through a huge frontier
        frontierSet = {}

        ## counts the amount of nodes that are explored
        counter = 0

        ## according to BFS algorithm we need to append the first node in the frontier to explore it later
        frontier.append(self)

        ## Explored is a dictionary to hold the explored sets since an infinite loop can accrue
        ## A dictionary was picked since we can hash the value and get a O(1) access time for it
        exploredSet = {}

        ## Measures the depth
        depth = self._depth

        while frontier.__len__() != 0:

            ## Pops the frontier first element,
            node = frontier.pop()
            counter += 1

            ## checks the depth that we reached so we can write it in the txt file that is going to be exported
            if depth < node._depth:
                depth = node._depth

            ## check if we are in the goal state
            if node.matrix == finishState:

                ## gets the path by generating the solution path. and adding them to the path array
                path = []
                for child in node.generateSolutionPath([]):
                    path.append(child.direction)
                path.reverse()

                ## exporting the information gathered for the question into a txt file.
                file = open('dfsoutput.txt', 'w')
                file.writelines(f'path_to_goal: {path}\n')
                file.writelines(f'cost_of_path: {path.__len__()}\n')
                file.writelines(f'nodes_expanded: {counter}\n')
                file.writelines(f'search_depth: {path.__len__()}\n')
                file.writelines(f'max_search_depth: {depth}\n')
                file.close()
                return True

            ## according to DFS this prevents the algorithm to go into an infinte loop state. By not allowing us to move
            ## back to a node we already visited

            if node.__str__() not in exploredSet:

                ## adding the hash node into the explored set
                exploredSet[node.__str__()] = True

                ## a stack to get all the nodes and then revert them since they will come in a reversed order
                stack = []
                for child in node.generateMoves():
                    stack.append(child)

                ## this will reverse the stack and checkes if the child node is not in the exploredSet and the
                ## FrontierSet. Then it appends it to the frontier
                for i in node.generateMoves():
                    child = stack.pop()
                    if child.__str__() not in exploredSet and child.__str__() not in frontierSet:
                        frontier.append(child)
                        frontierSet[child.__str__() ] = True

        return False

    # def heuristic(self):


    #def Astarsearch(self, h):
        """Performs A* search for goal state.
        h(move) - heuristic function, returns an integer
        """


        

def main():

    p = Puzzle8() # when we create the puzzle object, it's already in the goal state
    m = Puzzle8()

    p.shuffle(20) # that's why we shuffle to start from a random state which is 20 steps away from from the goal state
    # print(m)
    # print(p)
    # print(p.swap(p.find(4),p.find(3)))


    p.change_state([1,2,5,3,4,0,6,7,8])

    print(p.BFS())
    print("-------")
    print(p.DFS())
    print("-------")




if __name__ == "__main__":
    main()
