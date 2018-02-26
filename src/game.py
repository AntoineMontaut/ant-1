import sys
import pygame
from pygame.locals import *

from src.collider import Collider
from src.renderer import Renderer
from src.world import World

class Game():
    def __init__(self):
        self.screen_size = (800, 600)
        self.FPS = 60
        self.fps_clock = pygame.time.Clock()

        self.world = World(self.screen_size) # generate the world
        self.world.generate() # populate the world

        self.collider = Collider(self.world.objects, 
                                self.world.walls,
                                self.screen_size)

        # print(self.world.objects)

        self.win_surf = pygame.display.set_mode(self.screen_size,
                                                0, 32)
        pygame.display.set_caption('Ant-1!')

        self.renderer = Renderer(self.win_surf, self.world, self.fps_clock)

    def run(self):

        frame_counter = 0

        while True:
            # main game loop
            dt = self.fps_clock.tick(self.FPS)
            # dt = self.fps_clock.tick()
            frame_counter += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.teminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.teminate()
                    elif event.key == K_p:
                        self.pause_game()
                    elif event.key == K_LEFT:
                        print('left')
                    elif event.key == K_RIGHT:
                        print('right')
                    elif event.key == K_SPACE:
                        print('space')

            self.world.update(dt * 1)
            self.collider.update()
            self.renderer.render()

    def terminate(self):
        """Shut all down"""
        pygame.quit()
        sys.exit()