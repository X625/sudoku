from copy import deepcopy
from queue import PriorityQueue
import utilities

_range9 = range(9)

class Sudoku:

    def __init__(self, data):
        self.matrix = data

        self.encoded_possible_values = [[511 for j in _range9] for i in _range9]
        for r, row in enumerate(self.matrix):
            for c, val in enumerate(row):
                self.update_possible_row_column_block_values(r, c, val)


    def set_cell_value(self, row, col, value):
        self.matrix[row][col] = value
        self.update_possible_row_column_block_values(row, col, value)

    def update_possible_row_values(self, row, masked_value):
        for i in _range9:
            self.encoded_possible_values[row][i] &= masked_value

    def update_possible_column_values(self, col, masked_value):
        for i in _range9:
            self.encoded_possible_values[i][col] &= masked_value

    def update_possible_block_values(self, row, col, masked_value):
        block_start_row = int(row/3) * 3
        block_start_column = int(col/3) * 3
        block_end_row = block_start_row + 3
        block_end_column = block_start_column + 3

        for i in range(block_start_row, block_end_row):
            for j in range(block_start_column, block_end_column):
                self.encoded_possible_values[i][j] &= masked_value


    def update_possible_row_column_block_values(self, row, col, val):
        if not val:
            return
        self.encoded_possible_values[row][col] = 0
        coded_val = 1 << val - 1
        masked_value = 511 - coded_val
        self.update_possible_row_values(row, masked_value)
        self.update_possible_column_values(col, masked_value)
        self.update_possible_block_values(row, col, masked_value)

    def get_possible_expansions(self):
        pq = PriorityQueue()
        for i, row in enumerate(self.encoded_possible_values):
            for j, val in enumerate(row):
                number_of_values_can_be_assigned_to_cell = bin(val).count("1")
                if number_of_values_can_be_assigned_to_cell:
                    decoded_values_list = utilities.decode(self.encoded_possible_values[i][j])
                    pq.put((number_of_values_can_be_assigned_to_cell, i, j, decoded_values_list))
        return pq

    def fill_cells_with_only_one_possible_value(self):
        """
        Scan the board for obvious next moves, and go ahead and make those.
        In particular this means repeatedly looking for cells that we've marked
        as having a single possible value and actually placing that value on the
        board.
        """
        cells_need_updating = True
        while cells_need_updating:
            cells_need_updating = False
            for r, row in enumerate(self.encoded_possible_values):
                for c, poss_vals in enumerate(row):
                    pc = bin(poss_vals).count("1")#count_ones(poss_vals)
                    if pc == 1:
                        if not cells_need_updating:
                            cells_need_updating = True
                        val = utilities.decode(poss_vals)[0]
                        self.set_cell_value(r, c, val)

    def distance_to_goal(self):
        x = [e for sub in self.matrix for e in sub]
        return x.count(0)

    def expand(self):
        next_steps = self.get_possible_expansions()
        if next_steps.qsize():
            # pc, row, col, choices = self.get_scored_next_steps().get()
            pc, row, col, choices = next_steps.get()
            children = []
            for val in choices:
                child = deepcopy(self)
                child.set_cell_value(row, col, val)
                child.fill_cells_with_only_one_possible_value()
                children.append(child)

            return children
        return []

    def pretty_print(self):
        int2str = lambda s: str(s).replace('0', ' ')
        rows = [','.join(map(int2str, row)) for row in self.matrix]
        print('\n'.join(rows))

    def __lt__(self, other):
        return self.distance_to_goal() < other.distance_to_goal()