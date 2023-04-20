from copy import deepcopy


class Node:
    _nodes_count = 0
    def __init__(self, data):
        self.board = deepcopy(data)
        self.gn = 0
        self.parent = None
        self.encoded_values = [[511 for j in range(9)] for i in range(9)]
        for i, rows in enumerate(self.board):
            for j, value in enumerate(rows):
                self._encode(i, j, value)

    def set_value(self, row, col, value):
        self.board[row][col] = value
        self._encode(row, col, value)

    def _encode(self, row, col, value):
        if not value:
            return
        self.encoded_values[row][col] = 0

        coded_value = 1 << value - 1
        masked_value = 511 - coded_value

        for i in range(9):
            self.encoded_values[row][i] &= masked_value
            self.encoded_values[i][col] &= masked_value


        brow = int(row / 3) * 3
        bcol = int(col / 3) * 3
        for i in range(brow, brow + 3):
            for j in range(bcol, bcol + 3):
                self.encoded_values[i][j] &= masked_value

    def heuristic_func(self):
        return [e for sub in self.board for e in sub].count(0)

    # def heuristic_func(self):
    #     score = 0
    #     x = [e for sub in self.board for e in sub]
    #     my_dict = {i: x.count(i) for i in x}
    #     if 0 in my_dict:
    #         my_dict.pop(0)
    #     for key in my_dict.keys():
    #         s = my_dict[key]
    #         if s > 1:
    #             score -= s
    #     return score



    def fn(self):
        return self.gn + self.heuristic_func()
    def __lt__(self, other):
        return self.fn() < other.fn()