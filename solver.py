from functools import reduce
from queue import PriorityQueue
import utilities
from sudoku import Sudoku


# from sudoku import Sudoku

class Solver:
    def __init__(self, initial_board):
        self.start = Sudoku(initial_board)
        self.visited_set = set()
        self.queue = PriorityQueue()

    def solve(self):
        current_sudoku_state = self.start
        current_sudoku_state.fill_cells_with_only_one_possible_value()
        dist = current_sudoku_state.distance_to_goal()
        self.queue.put((dist, current_sudoku_state))

        while not current_sudoku_state.distance_to_goal() == 0 and self.queue.qsize():
            current_sudoku_state = self.queue.get()[1]
            self.visited_set.add(current_sudoku_state)

            for c in current_sudoku_state.expand():
                if c not in self.visited_set:
                    dist = c.distance_to_goal()
                    self.queue.put((dist, c))

        return current_sudoku_state.matrix
