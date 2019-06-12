import pygame
import sys
import time
import patterns
from utils import *

# consts
GRID_LENGTH = 100
CONTROL_PANEL_SIZE = 250
CELL_PIXEL = 5

# colors
GRAY_RGB = (127, 127, 127)
YELLOW_RGB = (255, 255, 0)

DIRECTIONS = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]


class Cells(object):
    def __init__(self):
        self.cells = [[0] * GRID_LENGTH for _ in range(GRID_LENGTH)]

    def draw(self, screen):
        for x in range(GRID_LENGTH):
            for y in range(GRID_LENGTH):
                if self.cells[x][y] == 1:
                    rect = [x * CELL_PIXEL + 1, y * CELL_PIXEL + 1, CELL_PIXEL - 1, CELL_PIXEL - 1]
                    pygame.draw.rect(screen, YELLOW_RGB, rect)

    def count_live_neighbours(self, x, y):
        cnt = 0
        for x_bias, y_bias in DIRECTIONS:
            if 0 <= x + x_bias < GRID_LENGTH and\
               0 <= y + y_bias < GRID_LENGTH:
                cnt += self.cells[x + x_bias][y + y_bias]
        return cnt

    def update(self):
        new_cells = [[0] * GRID_LENGTH for _ in range(GRID_LENGTH)]
        for x in range(GRID_LENGTH):
            for y in range(GRID_LENGTH):
                cnt = self.count_live_neighbours(x, y)
                if cnt == 2:
                    new_cells[x][y] = self.cells[x][y]
                elif cnt == 3:
                    new_cells[x][y] = 1
        self.cells = new_cells

    def load_pattern(self, pattern):
        pos_x, pos_y = (GRID_LENGTH//2 - len(pattern)//2, GRID_LENGTH//2 - len(pattern)//2)
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                self.cells[i + pos_x][j + pos_y] = pattern[i][j]

    def toggle_status(self, x, y):
        self.cells[x][y] = int(not self.cells[x][y])


def create_grid():
    grid_shape = (GRID_LENGTH * CELL_PIXEL + 1, GRID_LENGTH * CELL_PIXEL + 1)
    new_grid = pygame.Surface(grid_shape)
    new_grid = new_grid.convert()
    new_grid.fill(GRAY_RGB)
    return new_grid


def set_speed(speed):
    clock.tick(speed)


def deal_with_events():
    mouse_activate = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE \
           or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_activate = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_activate = False
        if event.type == pygame.MOUSEMOTION:
            if mouse_activate:
                mouse_x, mouse_y = event.pos
                if in_rect(event.pos, (1, 1, GRID_LENGTH * CELL_PIXEL, GRID_LENGTH * CELL_PIXEL)):
                    cells.toggle_status(int((mouse_x - 1)/5), int((mouse_y - 1)/5))



if __name__ == '__main__':
    # setting screen
    pygame.init()
    pygame.display.set_caption('Game of Life')
    window_shape = (GRID_LENGTH * CELL_PIXEL + 1 + CONTROL_PANEL_SIZE, GRID_LENGTH * CELL_PIXEL + 1)
    screen = pygame.display.set_mode(window_shape)
    clock = pygame.time.Clock()

    grid = create_grid()
    cells = Cells()
    cells.load_pattern(patterns.GLIDER)
    while 1:
        set_speed(0)
        screen.blit(grid, (0, 0))
        deal_with_events()

        cells.update()
        cells.draw(screen)

        screen.blit(screen, (0, 0))
        pygame.display.flip()




