import pygame
from generator import SudokuGenerator


pygame.font.init()
matrix_size = 9
mode_size = 250 * 3
grid = SudokuGenerator().get_sudoku_2d()
pygame.display.set_caption("** SUDOKU **")
screen = pygame.display.set_mode((mode_size, mode_size))
dif = mode_size / matrix_size
font1 = pygame.font.SysFont("times new roman", 50)
cell_bg = (0, 153, 153)

def draw():
    # Draw the lines
    for i in range(matrix_size):
        for j in range(matrix_size):
            if grid[i][j] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, cell_bg, (i * dif, j * dif, dif + 1, dif + 1))
                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))

    # Draw horizontal & vertical lines
    for i in range(10):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (mode_size, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, mode_size), thick)


run = True
while run:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False

        draw()
        # Update window
        pygame.display.update()

# Quit pygame window
pygame.quit()
