"""
Collider classes manage and resolves collisions
"""

import itertools as it

import sys

class Segmenter():
    def __init__(self, window_size, shape=(4, 4), margin=10):
        self.cols = shape[0]
        self.rows = shape[1]
        self.width = window_size[0]
        self.height = window_size[1]
        self.margin = margin
        self.__gen_ranges()


    def __gen_ranges(self):
        # The low and high boundary values for the quadrants
        # e.g. [(0, 200), (200, 400), ...]
        self.x_ranges = [(self.width//self.cols * i - self.margin, \
                     self.width//self.cols * (i + 1) + self.margin) \
                     for i in range(self.cols)]
        self.y_ranges = [(self.height//self.rows * i - self.margin, \
                     self.height//self.rows * (i + 1) + self.margin) \
                     for i in range(self.rows)]


class Collider():
    """detect ant manage collisions"""

    def __init__(self, world_objects, walls, window_size):
        """init with objects"""
        self.objects = world_objects
        self.walls = walls
        self.segmenter = Segmenter(window_size)

    def update(self):
        # check for wall collisions
        wall_groups = self.find_ants_near_walls()
        for group, wall in zip(wall_groups, self.walls):
            self.wall_detect(group, wall)

        # segregate ants into quadrants
        groups = self.segregate_objects()
        for group in groups:
            # check ant-to-ant collisions
            self.detect(group)

    def find_ants_near_walls(self):
        group = [[] for _ in range(4)] # wall groups
        for obj in self.objects:
            if obj.rect.centery < self.segmenter.margin:
                group[0].append(obj) #top
            elif obj.rect.centery > self.segmenter.height - self.segmenter.margin:
                group[2].append(obj) # bottom
            if obj.rect.centerx > self.segmenter.width - self.segmenter.margin:
                group[1].append(obj) # right
            elif obj.rect.centerx < self.segmenter.margin:
                group[3].append(obj)

        return group

    def segregate_objects(self):
        """
        divide all objects into quadrants

        we only need to check for collisions against ants that are in
        the same quadrants, saving iterations
        """
        row_groups = [[] for _ in range(self.segmenter.rows)]
        groups = [[] for _ in range(self.segmenter.rows * \
                                    self.segmenter.cols)]

        #assign objects into columns
        for obj in self.objects:
            for num, (low, high) in enumerate(self.segmenter.x_ranges):
                if low < obj.rect.centerx < high:
                    row_groups[num].append(obj)
                    break;
        for col, group in enumerate(row_groups):
            for obj in group:
                for row, (low, high) in enumerate(self.segmenter.y_ranges):
                    if low < obj.rect.centery < high:
                        groups[col * len(row_groups) + row].append(obj)
                        # Just colorize for visualization's sake
                        # if row % 2 == 0:
                        #    if col % 2 == 0:
                        #        obj.color = (255, 255/(row+1), 255/(col+1))
                        #    else:
                        #        obj.color = (155, 255, 155/col)
                        # else:
                        #    if col % 2 == 0:
                        #        obj.color = (155, 255/(row+1), 255)
                        #    else:
                        #        obj.color = (0, 255/(row+1), 255/(col+1))
                        break;

        # print(groups)
        return groups

    def wall_detect(self, group, wall):
        """check ants in wall groups for wall collisions"""
        for obj in group:
            if obj.rect.colliderect(wall.rect):
                obj.collide(wall)

    def detect(self, group):
        """cycle though all objects and find collisions"""
        pass
        #detect ant-to-ant collisions
        for one, two in it.combinations(group, 2):
            if one.rect.colliderect(two.rect):
                # if two.name == 'apple':
                #     one.color = (50, 255, 50)
                # elif one.name == 'apple':
                #     two.color = (50, 255, 50)
                try:
                    one.collide(two)
                except AttributeError:
                    pass
                try:
                    two.collide(one)
                except AttributeError:
                    pass
