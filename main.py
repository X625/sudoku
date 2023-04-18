import pygame
from generator import SudokuGenerator
from solver import Solver

pygame.font.init()
resolution = (1050, 750)
screen = pygame.display.set_mode(resolution)
width = screen.get_width()
height = screen.get_height()
cell_size = height / 9


light = (170, 170, 170)
dark = (100, 100, 100)
c1 = (2, 117, 216)
c2  = (64, 131, 190)

green = 'green'
white = 'white'
red = 'red'
pygame.display.set_caption("** Aidin Haghparast, Yuhan Liu **")

grid = SudokuGenerator().generate()
font = pygame.font.SysFont("times new roman", 50)
smallfont = pygame.font.SysFont('Corbel',30)


btn_width = 140
btn_height = 40
def draw_lines():
    for i in range(10):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * cell_size), (height, i * cell_size), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, height), thick)

def fill_grid():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, green, (i * cell_size, j * cell_size, cell_size + 1, cell_size + 1))
                text = font.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text, (i * cell_size + 15, j * cell_size + 15))

def draw(m):
    screen.fill(white)
    fill_grid()
    draw_lines()
    draw_new_button(m)
    draw_solve_button(m)
    pygame.display.update()

def draw_new_button(m):
    col, row = 825, 40
    position = [col, row, btn_width, btn_height]
    color = c2 if m[0] in range(col, col + btn_width) and m[1] in range(row, row + btn_height) else c1
    pygame.draw.rect(screen, color, position)
    text = smallfont.render('New', True, white)
    screen.blit(text, (col + 50, row + 10))

def draw_solve_button(m):
    col, row = 825, 100
    position = [col, row, btn_width, btn_height]
    color = c2 if m[0] in range(col, col + btn_width) and m[1] in range(row, row + btn_height) else c1
    pygame.draw.rect(screen, color, position)
    text = smallfont.render('Solve', True, white)
    screen.blit(text, (col + 50, row + 10))

def get_mouse_col_row(m):
    return int(mouse[0] / cell_size), int(mouse[1] / cell_size)


run = True
while run:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = get_mouse_col_row(mouse)
            if mpos == (10,0):
                grid = SudokuGenerator().generate()
                print(type(grid))
                print(grid)
            elif mpos == (10,1):
                solver = Solver(grid)
                grid = solver.solve()
                print(grid)

    draw(mouse)

pygame.quit()