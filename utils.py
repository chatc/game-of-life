import pygame
import json
from parameters import *
import os


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


class Fonts(object):
    def __init__(self, text, position):
        self.fontObj = pygame.font.SysFont('宋体', 30)
        self.text_surface = self.fontObj.render(text, False, BLACK_RGB)
        self.position = position

    def render(self, screen):
        w, h = self.text_surface.get_size()
        x, y = self.position
        screen.blit(self.text_surface, (x - w / 2, y - h / 2))

    def update(self, text):
        self.text_surface = self.fontObj.render(text, False, BLACK_RGB)


def read_index_data(path="./LFWA/index_data.json"):
    with open(path, 'r', encoding='utf-8') as json_file:
        model = json.load(json_file)
    return model


def write_list_to_json(variable_values, path="./generate_dataset.json", indent=2):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(variable_values, json_file, ensure_ascii=False, indent=indent)

def read_photo(path):
    number = 0
    for _ in os.listdir(path):
        number = number+1
    return number