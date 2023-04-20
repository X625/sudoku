import time
from queue import PriorityQueue
from node import Node

def decode(bit_string):
    decoded_list = []
    x = 1
    while bit_string != 0:
        if bit_string & 1:
            decoded_list.append(x)
        x += 1
        bit_string >>= 1

    return decoded_list

class Info:
    def __init__(self):
        self.execution_time = 0
        self.nodes_generated = 0
        self.nodes_expanded = 0
        self.depth_of_tree = 0
        self.path = []
        self.effective_branching_factor = 0

class Sudoku:


    def __init__(self, initial_board):
        self.start = Node(initial_board)
        self.info = Info()


    def solve(self):
        start_time = time.time()
        CLOSED = set()
        OPEN = PriorityQueue()

        BEST_NODE = self.start
        OPEN.put((BEST_NODE.fn(), BEST_NODE))

        while not BEST_NODE.heuristic_func() == 0 and OPEN.qsize():
            BEST_NODE = OPEN.get()[1]
            CLOSED.add(BEST_NODE)
            self.info.path.append(BEST_NODE)
            self.info.nodes_expanded += 1
            for child in Sudoku.get_children(BEST_NODE, self.info):
                if child not in CLOSED:
                    OPEN.put((child.fn(), child))
        self.info.execution_time = (time.time() - start_time) * 1000
        self.info.depth_of_tree = BEST_NODE.gn
        self.info.effective_branching_factor = round(self.info.nodes_generated / BEST_NODE.gn, 2)
        return BEST_NODE, self.info

    def get_children(node, info):
        pq = PriorityQueue()
        for i, rows in enumerate(node.encoded_values):
            for j, val in enumerate(rows):
                count1 = bin(val).count("1")
                if count1:
                    decoded_list = decode(node.encoded_values[i][j])
                    pq.put((count1, i, j, decoded_list))

        if pq.qsize():
            _, row, col, choices = pq.get()
            children = []
            for val in choices:
                info.nodes_generated += 1
                child = Node(node.board)
                child.gn = node.gn + 1
                child.parent = node
                child.set_value(row, col, val)
                children.append(child)
            return children
        return []
