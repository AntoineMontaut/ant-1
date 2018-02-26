import math
import random as rnd

from pygame import Rect

class Ant():
    """An ant"""

    def __init__(self, pos, breed='black', caste='worker'):
        """initiate an ant at position pos"""
        self.name = 'ant'
        self.breed = breed
        self.caste = caste

        self.pos = pos 

        self.speed = {'black': 80.0, 'red': 80.0}[breed]
        self.width = {'black': 10, 'red': 5}[breed]
        self.height = {'black': 4, 'red': 2}[breed]
        self.mass = {'black': 5, 'red': 2}[breed]
        self.color = {
            'black': (0, 0, 0, 128),
            'red': (255, 0, 0, 128)
        }[breed]

        if caste == 'queen':
            self.width *= 2.5
            self.height *= 2.5
            self.speed /= 2.0
            self.mass *= 5

        self.rect = Rect(self.pos[0] - self.width // 2,
                        self.pos[1] - self.height // 2,
                        self.width, self.height)

        self.orientation = rnd.uniform(0, 2 * math.pi)

    def update(self, dt=None):
        self.turn(dt)
        self.move(dt)

    def turn(self, dt=None):
        """Turn"""
        self.orientation += rnd.uniform(-0.2, 0.2)
        if self.orientation >= 2 * math.pi:
            self.orientation -= 2 * math.pi
        elif self.orientation < 0:
            self.orientation += 2 * math.pi

    def move(self, dt=None):
        """Move"""
        distance = dt / 1000.0 * float(self.speed) if dt else 3.0
        dx = distance * math.cos(self.orientation)
        dy = distance * math.sin(self.orientation)
        self.pos = (self.pos[0] + dx, self.pos[1] - dy)
        self.rect.center = self.pos

    def collide(self, obj):
        """Ant turns around when it hits something"""
        if self.mass > obj.mass:
            pass
        else:
            self.orientation += math.pi