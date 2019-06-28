from parameters import *
import numpy as np
import os
import utils
import sys

class Dataset(object):
    def __init__(self):
        self.data_path = DATA_PATH
        self.person_list = [name for name in os.listdir(self.data_path)]
        self.index = utils.read_index_data(INDEX_PATH)
        if START_PERSON is None:
            self.cur_pos = self.person_list.index(self.get_minimum_person())
        else:
            self.cur_pos = START_PERSON

    def get_minimum_person(self):
        min_person = INF_PERSON
        for (k, v) in self.index.items():
            min_person = min(min_person, min(v))
        return min_person

    def get_next_person(self):
        self.cur_pos -= 1
        while self.cur_pos != 0\
                and self.is_labeled(self.cur_pos):
            self.cur_pos -= 1
        return self.person_list[self.cur_pos]

    def is_labeled(self, index):
        for (k, v) in self.index.items():
            if self.person_list[index] in v:
                return True
        return False

    def add_data(self, cata):
        self.index[cata].append(self.person_list[self.cur_pos])

    def save(self):
        utils.write_list_to_json(self.index, SAVE_INDEX_PATH)

    def get_data_info(self):
        info = str(self.cur_pos)
        user_numbers = []
        for (k, v) in self.index.items():
            photo_count = [utils.read_photo(self.data_path + person) for person in v]
            user_numbers.append(np.sum(photo_count, axis=0) // 64)
        sys_info = '\r black & white user count:' + str(user_numbers[0] + user_numbers[1]) + ' ' +\
                   str(user_numbers[2] + user_numbers[3])
        sys.stdout.write(sys_info)
        sys.stdout.flush()
        return info


