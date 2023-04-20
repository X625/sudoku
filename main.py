import time
from copy import deepcopy

import pygame
from generator import SudokuGenerator
from sudoku import Sudoku

pygame.font.init()
resolution = (1050, 750)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("** Aidin Haghparast, Yuhan Liu **")

width = screen.get_width()
height = screen.get_height()
cell_size = int(height/9)

info = None
grid = None
original = None
completed_node = None
animate_flag = False
font = pygame.font.SysFont("times new roman", 50)

def draw_lines():
    for i in range(10):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * cell_size), (height, i * cell_size), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, height), thick)

def fill_grid():
    if not grid:
        return

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, 'green', (j * cell_size, i * cell_size, cell_size + 1, cell_size + 1))
                text = font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (j * cell_size + 30, i * cell_size + 15))

def draw(m, info_obj):
    screen.fill('white')
    fill_grid()
    draw_lines()
    draw_button(m,'New', 20, 825)
    draw_button(m,'Solve',100,825)
    draw_button(m,'Reset', 180, 825)
    if info_obj:
        screen_text('Execution Time:   %d ms' % info_obj.execution_time, 775, 250)
        screen_text('Nodes Generated:  %d' % info_obj.nodes_generated, 775, 300)
        screen_text('Nodes Expanded:   %d' % info_obj.nodes_expanded, 775, 350)
        screen_text('Depth of Tree:    %d' % info_obj.depth_of_tree, 775, 400)
        screen_text('Branching Factor: %.2f' % info_obj.effective_branching_factor, 775, 450)
        screen_text('Total Path:       %d' % len(info_obj.path), 775, 500)
    pygame.display.update()

def draw_button(m, caption, row, col):
    rgb1, rgb2 = (2, 117, 216), (64, 131, 190)
    btn_width, btn_height = 140, 40
    position = [col, row, btn_width, btn_height]
    color = rgb2 if m[0] in range(col, col + btn_width) and m[1] in range(row, row + btn_height) else rgb1
    pygame.draw.rect(screen, color, position)
    text = pygame.font.SysFont('Arial', 20).render(caption, True, 'white')
    screen.blit(text, (col + 45, row + 8))

def get_mouse_col_row(mpos):
    return int(mpos[0] / cell_size), int(mpos[1] / cell_size)

def screen_text(caption, col, row):
    text = pygame.font.SysFont("times new roman", 20).render(caption, True, (0, 0, 0))
    screen.blit(text, (col, row))

run = True
while run:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = get_mouse_col_row(mouse)
            if mouse_position == (10,0): # New Button Clicked
                completed_node, info = None, None
                grid = SudokuGenerator().generate()
                original = deepcopy(grid)
                animated = False
            elif mouse_position == (10,1) and grid: # Solve Button Clicked
                sudoku = Sudoku(grid)
                completed_node, info = sudoku.solve()
                if not animate_flag:
                    grid = completed_node.board

            elif mouse_position == (10, 2): # Reset Button Clicked
                grid = deepcopy(original)
                completed_node, info = None, None
                animated = False

    if animate_flag and info and not animated:
        for node in info.path:
            grid = node.board
            time.sleep(0.5)
            draw(mouse, info)
        animated = True
    else:
        draw(mouse, info)

pygame.quit()