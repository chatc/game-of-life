import sys
import pygame
import patterns
from utils import *
from cell_core import *

# control Flags
PAUSE = False
INTERVAL = 0.8


def create_grid():
    grid_shape = (GRID_LENGTH * CELL_PIXEL + 1, GRID_LENGTH * CELL_PIXEL + 1)
    new_grid = pygame.Surface(grid_shape)
    new_grid = new_grid.convert()
    new_grid.fill(BLACK_RGB)
    return new_grid


def create_control_panel():
    start_x = GRID_LENGTH * CELL_PIXEL + 1
    start_y = 1

    return Buttons([Button('icons/skip_to_start_48px_1169504_easyicon.net - chn.png',
                           'icons/skip_to_start_48px_1169504_easyicon.net.png',
                           (start_x + 50, start_y + 50)),
                    Button('icons/music_rewind_button_48px_1182982_easyicon.net - chn.png',
                           'icons/music_rewind_button_48px_1182982_easyicon.net.png',
                           (start_x + 50, start_y + 100)),
                    Button('icons/music_fastforward_button_48px_1182964_easyicon.net - chn.png',
                           'icons/music_fastforward_button_48px_1182964_easyicon.net.png',
                           (start_x + 50, start_y + 150)),
                    Button('icons/arrows_circle_remove_48px_1182472_easyicon.net - chn.png',
                           'icons/arrows_circle_remove_48px_1182472_easyicon.net.png',
                           (start_x + 50, start_y + 200)),
                    Button('icons/magic_64px_1150582_easyicon.net - chn.png',
                           'icons/magic_64px_1150582_easyicon.net.png',
                           (start_x + 50, start_y + 300)),
                    ],
                    ['start_pause', 'speed_up', 'slown_down', 'clear', 'load'])


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
                if buttons.get_button_by_id(0).is_over():
                    PAUSE = not PAUSE
                if buttons.get_button_by_id(1).is_over():
                    if INTERVAL <= 15:
                        INTERVAL *= 2
                if buttons.get_button_by_id(2).is_over():
                    if INTERVAL >= 0.01:
                        INTERVAL /= 2
                if buttons.get_button_by_id(3).is_over():
                    cells.clear()
                if buttons.get_button_by_id(4).is_over():
                    history_pause = PAUSE
                    PAUSE = True
                    cells.load_pattern(patterns.pattern_dic[patterns.cur_patterns])
                    patterns.cur_patterns = (patterns.cur_patterns + 1) % len(patterns.pattern_dic)
                    PAUSE = history_pause


if __name__ == '__main__':
    # setting screen
    pygame.init()
    pygame.display.set_caption('Game of Life')
    window_shape = (GRID_LENGTH * CELL_PIXEL + 1 + CONTROL_PANEL_SIZE, GRID_LENGTH * CELL_PIXEL + 1)
    screen = pygame.display.set_mode(window_shape)
    clock = pygame.time.Clock()

    # draw different parts
    grid = create_grid()
    buttons = create_control_panel()
    cells = Cells()

    # load pattern
    cells.load_pattern(patterns.pattern_dic[patterns.cur_patterns])
    patterns.cur_patterns = (patterns.cur_patterns + 1) % len(patterns.pattern_dic)

    while True:
        clock.tick(100)
        screen.fill(GRAY_RGB)
        screen.blit(grid, (0, 0))
        buttons.render(screen)
        deal_with_events()

        if not PAUSE and cells.ready_for_refresh(INTERVAL):
            cells.update()

        cells.draw(screen)
        screen.blit(screen, (0, 0))
        pygame.display.flip()




