import random
import math

def _random_generator(num):
    return math.floor(random.random() * num + 1)

class SudokuGenerator:
    def __init__(self):
        self._number_of_rows = 9
        self._number_of_blocks_in_row = 3
        self._number_of_digits_te_be_removed = 75
        self._matrix = [[0 for _ in range(self._number_of_rows)] for _ in range(self._number_of_rows)]

    def _fill_values(self):
        self._fill_diagonal()
        self._fill_remaining(0, self._number_of_blocks_in_row)
        self._remove_k_digits()

    def _fill_diagonal(self):
        for i in range(0, self._number_of_rows, self._number_of_blocks_in_row):
            self._fill_box(i, i)

    def _unused_in_box(self, row_start, col_start, num):
        for i in range(self._number_of_blocks_in_row):
            for j in range(self._number_of_blocks_in_row):
                if self._matrix[row_start + i][col_start + j] == num:
                    return False
        return True

    def _fill_box(self, row, col):
        num = 0
        for i in range(self._number_of_blocks_in_row):
            for j in range(self._number_of_blocks_in_row):
                while True:
                    num = _random_generator(self._number_of_rows)
                    if self._unused_in_box(row, col, num):
                        break
                self._matrix[row + i][col + j] = num

    def _check_if_safe(self, i, j, num):
        return (self._unused_in_row(i, num) and
                self._unused_in_col(j, num) and
                self._unused_in_box(i - i % self._number_of_blocks_in_row, j - j % self._number_of_blocks_in_row, num))

    def _unused_in_row(self, i, num):
        for j in range(self._number_of_rows):
            if self._matrix[i][j] == num:
                return False
        return True

    def _unused_in_col(self, j, num):
        for i in range(self._number_of_rows):
            if self._matrix[i][j] == num:
                return False
        return True

    def _fill_remaining(self, i, j):
        if i == self._number_of_rows - 1 and j == self._number_of_rows:
            return True
        if j == self._number_of_rows:
            i += 1
            j = 0
        if self._matrix[i][j] != 0:
            return self._fill_remaining(i, j + 1)
        for num in range(1, self._number_of_rows + 1):
            if self._check_if_safe(i, j, num):
                self._matrix[i][j] = num
                if self._fill_remaining(i, j + 1):
                    return True
                self._matrix[i][j] = 0

        return False

    def _remove_k_digits(self):
        count = self._number_of_digits_te_be_removed
        while count != 0:
            i = _random_generator(self._number_of_rows) - 1
            j = _random_generator(self._number_of_rows) - 1
            if self._matrix[i][j] != 0:
                count -= 1
                self._matrix[i][j] = 0


    def generate(self):
        self._fill_values()
        return self._matrix