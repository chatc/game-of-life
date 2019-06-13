import pygame
import time
from parameters import *


class Cells(object):
    def __init__(self):
        self.cells = [[0] * GRID_LENGTH for _ in range(GRID_LENGTH)]
        self.last_refresh = time.time()

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
        self. last_refresh = time.time()

    def load_pattern(self, pattern):
        self.clear()
        pos_x, pos_y = (GRID_LENGTH//2 - len(pattern)//2, GRID_LENGTH//2 - len(pattern[0])//2)
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                self.cells[j + pos_y][i + pos_x] = pattern[i][j]
        self.last_refresh = time.time()

    def toggle_status(self, x, y):
        self.cells[x][y] = int(not self.cells[x][y])

    def ready_for_refresh(self):
        return time.time() - self.last_refresh > INTERVAL

    def clear(self):
        self.cells = [[0] * GRID_LENGTH for _ in range(GRID_LENGTH)]
        self.last_refresh = time.time()
