import random as rnd
import numpy as np

from pygame import Rect

import src.items as items
import src.maps as maps
from src.ant import Ant
from src.wall import Wall
from src.colony import Colony
from src.config_ants import *

class World():
    """a world contains all the objects"""

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.bg_color = (100, 100, 100)
        self.ants = []
        self.items = []
        self.walls = []
        self.colony = None
        self.pheromones = np.zeros((screen_size[0] + 10, screen_size[1] + 10)) # plus 20 margin
        self.pherofoods = np.zeros((screen_size[0] + 10, screen_size[1] + 10))

    def generate(self):
        print('Generating world!')
        #TODO: load the map here...
        map_data = maps.load_level_file(1)
        self.generate_walls(self.screen_size)
        self.generate_map_objects(map_data)
        self.generate_colony((self.screen_size[0]/2, self.screen_size[0]/2))
        self.generate_ants(NUM_ANTS)
        self.generate_queens(0)
        return None

    def generate_colony (self, pos):
        self.colony = Colony(pos)

    def generate_walls(self, size):
        """generate the wall objects, for collision detection"""
        t = 5e1 # wall thickness, off screen
        self.walls = [
            Wall(Rect((-t, -t), (size[0] + 2*t, t)), colony=False), # top
            Wall(Rect((size[0], -t), (t, size[1] + 2 * t)), colony=False),  # right
            Wall(Rect((-20, size[1]), (size[0] + 2 * t, t)), colony=False),  # bot
            Wall(Rect((-t, -t), (t, size[1] + 2 * t)), colony=False),  # left
        ]
        return None

    def generate_map_objects(self, map_data):
        """add map object to the world"""
        print(map_data)
        item_data = map_data['items']
        for item in item_data:
            for class_name, coords in item.items():
                #instantiate different classes depending on item name
                # obj = getattr(items, class_name.title())(coords)
                obj = None
                if class_name == "apple":
                    obj = items.Apple(coords)
                if obj != None:
                    self.items.append(obj)

    def generate_ants(self, ant_count):
        """generate normal ants"""
        print('\tGenerating the ants')
        for _ in range(ant_count):
            breed = rnd.choice(['black', 'red'])
            x = int(rnd.random() * self.screen_size[0] / 100)
            y = int(rnd.random() * self.screen_size[1] / 1)
            self.ants.append(Ant((x, y), breed))
        return None

    def generate_queens(self, queen_count):
        """generate queen ants"""
        print('\tGenerating the queens')
        for _ in range(queen_count):
            breed = rnd.choice(['black', 'red'])
            x = int(rnd.random() * self.screen_size[0])
            y = int(rnd.random() * self.screen_size[1])
            self.ants.append(Ant((x, y), breed, 'queen'))
        return None

    def update(self, dt=None):
        """update the world and all its contents"""
        decay_rate = DECAY_RATE

        self.pheromones = self.pheromones*decay_rate # pheromones diffuse in time
        self.pherofoods = self.pherofoods*decay_rate
        # print(self.pheromones.max())

        for ant in self.ants:
            ant.update(dt)

            # x, y = pos + 5 because of "margin"
            x, y = abs(int(ant.pos[0])) + 5, abs(int(ant.pos[1])) + 5
            if x > (self.screen_size[0] - 1):
                x = self.screen_size[0] - 1
            if y > (self.screen_size[1] - 1):
                y = self.screen_size[1] - 1

            try:
                if not ant.carry_food:
                    self.pheromones[x, y] += 1
                    # self.pheromones[x + 1, y] += 1
                    # self.pheromones[x - 1, y] += 1
                    # self.pheromones[x, y + 1] += 1
                    # self.pheromones[x, y - 1] += 1
                    # self.pheromones[x - 1, y - 1] += 1
                    # self.pheromones[x + 1, y + 1] += 1
                else:
                    self.pherofoods[x, y] += 1
                    # self.pherofoods[x + 1, y] += 1
                    # self.pherofoods[x - 1, y] += 1
                    # self.pherofoods[x, y + 1] += 1
                    # self.pherofoods[x, y - 1] += 1
                    # self.pherofoods[x - 1, y - 1] += 1
                    # self.pherofoods[x + 1, y + 1] += 1
                # self.pheromones[x, y] += 50
                # self.pheromones[x-1, y-1] += 50
            except Exception as e:
                print('x = {}\ty = {}'.format(x, y))
                print(e)

            s_ = self.get_state(ant)

        # for phero in [self.pheromones, self.pherofoods]:
        #     phero = np.clip(phero, 0, 255)

    def get_state(self, ant):
        # state consist of : carry_food, orientation, pheromones/pherofoods around the ant
        x, y = int(ant.pos[0]+5), int(ant.pos[1]+5)
        w = 2 # "vision quandrants" of size 5 x 5
        # ie size of squares seen by ants (1 square where ant is and 8 squares around)
        # phero_center = np.mean(pheromones[x - w, x + w + 1])
        pherom_vision = np.array([
            np.mean(self.pheromones[x - w: x + w + 1, y - w: y + w + 1]),
            np.mean(self.pheromones[x - w: x + w + 1, y - 3*w - 1: y - w]),
            np.mean(self.pheromones[x - 3*w - 1: x - w, y - 3*w - 1: y - w]),
            np.mean(self.pheromones[x - 3*w - 1: x - w, y - w: y + w + 1]),
            np.mean(self.pheromones[x - 3*w - 1: x - w, y + w + 1: y + 4*w]),
            np.mean(self.pheromones[x - w: x + w + 1, y + w + 1: y + 4*w]),
            np.mean(self.pheromones[x + w + 1: x + 4*w, y + w + 1: y + 4*w]),
            np.mean(self.pheromones[x + w + 1: x + 4*w, y - w: y + w + 1]),
            np.mean(self.pheromones[x + w + 1: x + 4*w, y - 3*w -1: y - w])
        ])
        if np.max(pherom_vision) != 0:
            pherom_vision = (pherom_vision - np.min(pherom_vision)) / (np.max(pherom_vision) - np.min(pherom_vision))

        pherof_vision = np.array([
            np.mean(self.pherofoods[x - w: x + w + 1, y - w: y + w + 1]),
            np.mean(self.pherofoods[x - w: x + w + 1, y - 3*w - 1: y - w]),
            np.mean(self.pherofoods[x - 3*w - 1: x - w, y - 3*w - 1: y - w]),
            np.mean(self.pherofoods[x - 3*w - 1: x - w, y - w: y + w + 1]),
            np.mean(self.pherofoods[x - 3*w - 1: x - w, y + w + 1: y + 4*w]),
            np.mean(self.pherofoods[x - w: x + w + 1, y + w + 1: y + 4*w]),
            np.mean(self.pherofoods[x + w + 1: x + 4*w, y + w + 1: y + 4*w]),
            np.mean(self.pherofoods[x + w + 1: x + 4*w, y - w: y + w + 1]),
            np.mean(self.pherofoods[x + w + 1: x + 4*w, y - 3*w -1: y - w])
        ])
        if np.max(pherof_vision) != 0:
            pherof_vision = (pherof_vision - np.min(pherof_vision)) / (np.max(pherof_vision) - np.min(pherof_vision))

        food = 1. if ant.carry_food else 0.
        orientation = ant.orientation / (2*np.pi)

        temp = np.array([orientation, food]) # in an array before concatenating everything

        pherom_vision = np.nan_to_num(pherom_vision)
        pherof_vision = np.nan_to_num(pherof_vision)

        state = np.concatenate([
            temp,
            pherom_vision,
            pherof_vision
        ])
        # state = state.reshape((20,))
        state = state.reshape(1,20)

        return state

    @property
    def objects(self):
        """report all our objects"""
        return self.ants + self.items + self.colony
