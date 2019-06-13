import pygame
from parameters import *

def in_rect(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx + rw)and(ry <= y <= ry + rh):
        return True
    return False


class Button(object):
    def __init__(self, up_image, down_image, position):
        self.imageUp = pygame.image.load(up_image).convert_alpha()
        self.imageDown = pygame.image.load(down_image).convert_alpha()
        self.position = position

    def is_over(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageUp.get_size()

        in_x = x - w / 2 < point_x < x + w / 2
        in_y = y - h / 2 < point_y < y + h / 2
        return in_x and in_y

    def render(self, screen):
        w, h = self.imageUp.get_size()
        x, y = self.position

        if self.is_over():
            screen.blit(self.imageUp, (x - w / 2, y - h / 2))
        else:
            screen.blit(self.imageDown, (x - w / 2, y - h / 2))


class Buttons(object):
    def __init__(self, buttons, names):
        self.buttons = buttons
        self.names = names

    def render(self, screen):
        for button in self.buttons:
            button.render(screen)

    def get_button_by_name(self, name):
        return self.buttons[self.names.index(name)]

    def get_button_by_id(self, button_id):
        return self.buttons[button_id]
