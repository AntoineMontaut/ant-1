import math
import random as rnd
import numpy as np

from pygame import Rect
from src.config_ants import *

class Ant():
    """
    An ant
    """

    def __init__(self, pos, breed='black', caste='worker'):
        """initiate an ant at position pos"""
        self.name = 'ant'
        self.type = 'insect'
        self.breed = breed
        self.caste = caste
        self.carry_food = False

        self.pos = pos

        self.speed = {'black': 80.0, 'red': 80.0}[breed]
        self.width = {'black': 10, 'red': 5}[breed]
        self.height = {'black': 4, 'red': 2}[breed]
        self.mass = {'black': 5, 'red': 2}[breed]
        self.color = {
            'black': (128, 128, 128, 128),
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

        # ---------
        self.epsilon = 0.99
        self.s = None
        self.a = None
        self.r = 0
        self.s_ = None
        self.p = None

    def update(self, dt=None):
        # self.turn(dt)
        # get observation, send it to NN, and get turn/orientation output

        # get state:

        a = self.act(self.s)
        self.orientation += (a-1) * np.pi / 5
        self.orientation = self.orientation % (2 * np.pi)

        self.move(dt)

    def turn(self, dt=None):
        """Turn"""
        self.orientation += rnd.uniform(-0.2, 0.2)
        if self.orientation >= 2 * math.pi:
            self.orientation -= 2 * math.pi
        elif self.orientation < 0:
            self.orientation += 2 * math.pi

    def move(self, dt=3.0):
        """Move"""
        distance = dt / 1000.00 * self.speed
        # distance = dt / 1000.0 * float(self.speed) if dt else 3.0
        dx = distance * math.cos(self.orientation)
        dy = distance * math.sin(self.orientation)
        self.pos = (self.pos[0] + dx, self.pos[1] - dy)
        self.rect.center = self.pos

    def collide(self, obj):
        """Ant turns around when it hits something"""
        if obj.type == 'food':
            if self.carry_food == False:
                self.r += 1
                self.color = (0, 255, 0, 128)
            self.carry_food = True
        if self.mass > obj.mass:
            pass
        elif self.mass*5 < obj.mass:
            self.orientation += math.pi
            if (obj.type == 'wall') and (obj.colony):
                if self.carry_food == True:
                    self.r += 100
                    self.carry_food = False
                    self.color = (128, 128, 128, 128)
        else:
            pass
            # self.orientation += rnd.choice([math.pi / 4, - math.pi / 4])
        # else:
            # print('collision')
            # self.orientation += math.pi

    def update_epsilon(self, epsilon):
        self.epsilon = epsilon

    def act(self, s):
        if rnd.random() < self.epsilon:
            return rnd.randint(0, NUM_ACTIONS-1)

        else:
            # s = np.array([s])
            # p = brain.predict_p(s)[0]
            p = self.p

            a = np.random.choice(NUM_ACTIONS, p=p)
            # a = np.argmax(p)
            self.a = a

            return a

    def update_state(self,s):
        self.s = s

    def update_state_(self, s_):
        self.s_ = s_

    def reinitialize_r(self):
        self.r = 0

    def get_info(self):
        return self.s, self.a, self.r, self.s_

    def update_p(self, p):
        self.p = p
