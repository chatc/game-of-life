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
WHITE_RGB = (255, 255, 255)
AZURE_RGB = (137, 190, 178)

DIRECTIONS = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

# control Flags
PAUSE = False
INTERVAL = 0.8


class Cells(object):
    def __init__(self):
        self.cells = [[0] * GRID_LENGTH for _ in range(GRID_LENGTH)]
        self.last_refresh = time.time()

    def draw(self):
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
        pos_x, pos_y = (GRID_LENGTH//2 - len(pattern)//2, GRID_LENGTH//2 - len(pattern)//2)
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                self.cells[i + pos_x][j + pos_y] = pattern[i][j]
        self.last_refresh = time.time()

    def toggle_status(self, x, y):
        self.cells[x][y] = int(not self.cells[x][y])

    def ready_for_refresh(self):
        return time.time() - self.last_refresh > INTERVAL

    def clear(self):
        self.cells = [[0] * GRID_LENGTH for _ in range(GRID_LENGTH)]
        self.last_refresh = time.time()


def create_grid():
    grid_shape = (GRID_LENGTH * CELL_PIXEL + 1, GRID_LENGTH * CELL_PIXEL + 1)
    new_grid = pygame.Surface(grid_shape)
    new_grid = new_grid.convert()
    new_grid.fill(GRAY_RGB)
    return new_grid


def create_control_panel():
    start_x = GRID_LENGTH * CELL_PIXEL + 1
    start_y = 1
    return Buttons([Button('icons/beginning_48px_1153816_easyicon.net.ico',
                   (start_x + 50, start_y + 50)),
            Button('icons/music_fastforward_button_48px_1182964_easyicon.net.png',
                   (start_x + 100, start_y + 50)),
            Button('icons/music_rewind_button_48px_1182982_easyicon.net.png',
                   (start_x + 150, start_y + 50)),
            Button('icons/arrows_circle_remove_48px_1182472_easyicon.net.png',
                   (start_x + 200, start_y + 50))
            ],
            ['start_pause', 'speed_up', 'slown_down', 'clear'])


def deal_with_events():
    global PAUSE, INTERVAL
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE \
           or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if in_rect(event.pos, (1, 1, GRID_LENGTH * CELL_PIXEL, GRID_LENGTH * CELL_PIXEL)):
                cells.toggle_status(int((mouse_x - 1) / 5), int((mouse_y - 1) / 5))
            if in_rect(event.pos, (GRID_LENGTH * CELL_PIXEL + 1, 1,
                                   GRID_LENGTH * CELL_PIXEL + 1 + CONTROL_PANEL_SIZE,
                                   GRID_LENGTH * CELL_PIXEL + 1)):
                if buttons.get_button_by_id(0).isOver():
                    PAUSE = not PAUSE
                if buttons.get_button_by_id(1).isOver():
                    if INTERVAL <= 15:
                        INTERVAL *= 2
                if buttons.get_button_by_id(2).isOver():
                    if INTERVAL >= 0.01:
                        INTERVAL /= 2
                if buttons.get_button_by_id(3).isOver():
                    cells.clear()
                # PAUSE = not PAUSE # pause and start
                # if INTERVAL >= 0.1: INTERVAL /= 2  # speed up
                # if INTERVAL <= 100: INTERVAL *= 2  # slow down
                # cells.clear()  # clear screen
                # cells.load_pattern(patterns.GLIDER)  # load pattern


if __name__ == '__main__':
    # setting screen
    pygame.init()
    pygame.display.set_caption('Game of Life')
    window_shape = (GRID_LENGTH * CELL_PIXEL + 1 + CONTROL_PANEL_SIZE, GRID_LENGTH * CELL_PIXEL + 1)
    screen = pygame.display.set_mode(window_shape)
    screen.fill(AZURE_RGB)
    clock = pygame.time.Clock()
    # draw different parts
    grid = create_grid()
    buttons = create_control_panel()
    cells = Cells()
    cells.load_pattern(patterns.GLIDER)

    while True:
        clock.tick(0)
        screen.blit(grid, (0, 0))
        buttons.render(screen)
        deal_with_events()

        if not PAUSE and cells.ready_for_refresh():
            cells.update()

        cells.draw()
        screen.blit(screen, (0, 0))
        pygame.display.flip()




