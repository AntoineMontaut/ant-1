import sys
import numpy as np
import pygame
from pygame.locals import *

from src.collider import Collider
from src.renderer import Renderer
from src.world import World
from src.brain import Brain
from src.config_ants import *

class Game():
    def __init__(self):
        self.screen_size = (500, 300)
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

        self.brain = Brain()
        self.reward_total = 0
        self.reward_previous = 0

    def run(self, max_frames=3e+2):

        # -------------------------------- to re-initialize world
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

        self.reward_total = 0
        self.reward_previous = 0
        # ----------------------------------------

        frame_counter = 0
        eps_start = .99
        eps_end = .3
        eps_steps = 1e4

        phero = 'pheromones'
        rendering = True

        while frame_counter < max_frames + 1:
            if frame_counter % 500 == 0:
                delta_reward = self.reward_total - self.reward_previous
                print("frame #{} | total reward: {} | Delta: {}".format(
                    frame_counter, self.reward_total, delta_reward))
                self.reward_previous = self.reward_total

            # main game loop
            dt = self.fps_clock.tick(self.FPS)
            # dt = self.fps_clock.tick()
            frame_counter += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_r:
                        rendering = not rendering
                    # elif event.key == K_p:
                        # self.pause_game()
                    elif event.key == K_LEFT:
                        if phero == 'pherofoods':
                            phero = 'pheromones'
                            print('Displaying pheromones')
                        else:
                            phero = 'pherofoods'
                            print('Displaying pherofoods')
                    elif event.key == K_RIGHT:
                        if phero == 'pherofoods':
                            phero = 'pheromones'
                            print('Displaying pheromones')
                        else:
                            phero = 'pherofoods'
                            print('Displaying pherofoods')
                #     elif event.key == K_SPACE:
                #         print('space')

            if frame_counter >= eps_steps:
                epsilon = eps_end
            else:
                epsilon = eps_start + frame_counter * (eps_end - eps_start) / eps_steps

            for ant in self.world.ants:
                ant.update_epsilon(epsilon)
                ant.reinitialize_r()
                ant.update_state(self.world.get_state(ant))
                # print(ant.s)
                p = self.brain.predict_p(ant.s)[0]
                ant.update_p(p)

                (x, y) = ant.pos
                if x < 0:
                    x = 0
                elif x > self.screen_size[0]:
                    x = self.screen_size[0]

                if y < 0:
                    y = 0
                elif y > self.screen_size[1]:
                    y = self.screen_size[1]

                ant.pos = (x, y)

                # ant.pos[0] = np.clip(ant.pos[0], 0, self.screen_size[0])
                # ant.pos[1] = np.clip(ant.pos[1], 0, self.screen_size[1])

            # self.world.update(dt * 1)
            self.world.update(60)
            self.collider.update()
            if rendering:
                self.renderer.render(phero)
                # if frame_counter % 100 == 0:
                #     self.renderer.render(phero)

            for ant in self.world.ants:
                ant.update_state_(self.world.get_state(ant))

                s, a, r, s_ = ant.get_info()
                self.reward_total += r
                a_cats = np.zeros(NUM_ACTIONS)
                a_cats[a] = 1
                self.brain.train_push(s, a_cats, r, s_)

            self.brain.optimize()

    def run_episodes(self, num_episodes=1, num_frames=1e4):
        for episode in range(num_episodes):
            print('-'*50)
            print('Episode #{}'.format(episode))
            self.run(num_frames)


    def terminate(self):
        """Shut all down"""
        pygame.quit()
        sys.exit()
