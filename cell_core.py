import pygame
import time
import numpy as np
import os
import random
from parameters import *


class Cells(object):
    def __init__(self, current_person):
        self.current_person = current_person
        self.current_person_path = os.path.join(DATA_PATH, current_person)
        self.pic_path_list = [os.path.join(self.current_person_path, name)
                              for name in os.listdir(self.current_person_path)]
        self.cells = self.get_random_cells()

    def get_random_cells(self):
        full_list = np.arange(len(self.pic_path_list))
        np.random.shuffle(full_list)
        while len(full_list) < GRID_LENGTH * GRID_LENGTH:
            full_list = np.copy(np.concatenate((full_list, full_list)))
        return full_list[:GRID_LENGTH*GRID_LENGTH].reshape((GRID_LENGTH, GRID_LENGTH))

    def draw(self, screen):
        for x in range(GRID_LENGTH):
            for y in range(GRID_LENGTH):
                load_pic = self.pic_path_list[self.cells[x][y]]
                image = pygame.image.load(load_pic).convert_alpha()
                image = pygame.transform.scale(image, (CELL_PIXEL - 1, CELL_PIXEL - 1))
                screen.blit(image, (x * CELL_PIXEL + 1, y * CELL_PIXEL + 1))

    def update(self):
        self.cells = self.get_random_cells()


