import sys
import pygame
import patterns
from label_data import Dataset
from utils import *
from cell_core import *

# global vars
start_x = GRID_LENGTH * CELL_PIXEL + 1
start_y = 1


def create_grid():
    grid_shape = (GRID_LENGTH * CELL_PIXEL + 1, GRID_LENGTH * CELL_PIXEL + 1)
    new_grid = pygame.Surface(grid_shape)
    new_grid = new_grid.convert()
    new_grid.fill(BLACK_RGB)
    return new_grid


def create_control_panel():
    return Buttons([Button('rsc/icons/skip.png',
                           'rsc/icons/skip.png',
                           (start_x + 50, start_y + 50)),
                    Button('rsc/icons/black_male.png',
                           'rsc/icons/black_male.png',
                           (start_x + 50, start_y + 100)),
                    Button('rsc/icons/black_female.png',
                           'rsc/icons/black_female.png',
                           (start_x + 50, start_y + 150)),
                    Button('rsc/icons/white_male.png',
                           'rsc/icons/white_male.png',
                           (start_x + 50, start_y + 200)),
                    Button('rsc/icons/white_female.png',
                           'rsc/icons/white_female.png',
                           (start_x + 50, start_y + 250)),
                    ],
                    ['start_pause', 'speed_up', 'slown_down', 'clear', 'load'])


def deal_with_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE \
           or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if in_rect(event.pos, (1, 1, GRID_LENGTH * CELL_PIXEL, GRID_LENGTH * CELL_PIXEL)):
                cells.update()
            if in_rect(event.pos, (GRID_LENGTH * CELL_PIXEL + 1, 1,
                                   GRID_LENGTH * CELL_PIXEL + 1 + CONTROL_PANEL_SIZE,
                                   GRID_LENGTH * CELL_PIXEL + 1)):
                if buttons.get_button_by_id(1).is_over():
                    dataset.add_data(BLACK_MALE)
                if buttons.get_button_by_id(2).is_over():
                    dataset.add_data(BLACK_FEMALE)
                if buttons.get_button_by_id(3).is_over():
                    dataset.add_data(WHITE_MALE)
                if buttons.get_button_by_id(4).is_over():
                    dataset.add_data(WHITE_FEMALE)
                cells.__init__(dataset.get_next_person())
                dataset.save()
        fonts.update(dataset.get_data_info())


if __name__ == '__main__':
    # set dataset
    dataset = Dataset()

    # setting screen
    pygame.init()
    pygame.display.set_caption('Super Label -- ChatC')
    window_shape = (GRID_LENGTH * CELL_PIXEL + 1 + CONTROL_PANEL_SIZE, GRID_LENGTH * CELL_PIXEL + 1)
    screen = pygame.display.set_mode(window_shape)
    clock = pygame.time.Clock()

    # draw different parts
    grid = create_grid()
    buttons = create_control_panel()
    cells = Cells(dataset.get_next_person())
    fonts = Fonts(dataset.get_data_info(),
                  (start_x + 50, start_y + 300))

    while True:
        clock.tick(100)
        screen.fill(GRAY_RGB)
        screen.blit(grid, (0, 0))
        buttons.render(screen)
        deal_with_events()

        cells.draw(screen)
        fonts.render(screen)
        screen.blit(screen, (0, 0))
        pygame.display.flip()




