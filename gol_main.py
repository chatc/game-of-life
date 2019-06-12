import pygame

# consts
GRID_LENGTH = 100
CONTROL_PANEL_SIZE = 250
CELL_PIXEL = 5

# colors
GRAY_RGB = (127, 127, 127)


def create_grid():
    grid_shape = (GRID_LENGTH * CELL_PIXEL + 1, GRID_LENGTH * CELL_PIXEL + 1)
    grid = pygame.Surface(grid_shape)
    grid = grid.convert()
    grid.fill(GRAY_RGB)
    return grid


if __name__ == '__main__':
    # setting screen
    pygame.init()
    pygame.display.set_caption('Game of Life')
    window_shape = (GRID_LENGTH * CELL_PIXEL + 1 + CONTROL_PANEL_SIZE, GRID_LENGTH * CELL_PIXEL + 1)
    screen = pygame.display.set_mode(window_shape)
    clock = pygame.time.Clock()

    grid = create_grid()

    while 1:
        screen.blit(grid, (0, 0))
