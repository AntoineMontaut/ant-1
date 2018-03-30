"""classes for items on map"""

import pygame

class Item():
    def __init__(self):
        pass
        self.type = 'item'


class Apple():
    def __init__(self, pos):
        self.name = 'apple'
        self.type = 'food'
        self.pos = pos
        self.width = 20
        self.height = 20

        self.rect = pygame.Rect(self.pos[0] - self.width/2,
                                self.pos[1] - self.height/2,
                                self.width, self.height)

        # self.color = (255, 50, 50)
        self.color = (255, 255, 64)
        # self.masss = float('inf')
        self.mass = 999
