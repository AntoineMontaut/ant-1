"""
renderer is in charge of drawing graphics to the screen

the game did define the screen size, but otherwise the rest is here
"""

import math
import numpy as np

import pygame

class Renderer():
    def __init__(self, surface, world, clock):
        self.surface = surface
        self.world = world
        self.clock = clock

    def render(self, phero='pheromones'):
        self.surface.fill(self.world.bg_color)
        self.__render_phero(phero)
        self.__render_ants()
        self.__render_items()
        self.__render_colony()
        self.__render_fps()
        pygame.display.update()

    def __render_phero(self, phero):

        if phero == 'pheromones':
            pheromones_render = self.world.pheromones[5:-5, 5:-5]
        elif phero == 'pherofoods':
            pheromones_render = self.world.pherofoods[5:-5, 5:-5]

        surf = pygame.surfarray.make_surface(pheromones_render)
        self.surface.blit(surf, (0, 0))


    def __render_fps(self):
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text = '{:.2f}'.format(self.clock.get_fps())
        text_surface = font.render(text, True, (200, 155, 155))
        text_pos = text_surface.get_rect(centerx=self.surface.get_width()/2)
        self.surface.blit(text_surface, text_pos)

    def __render_ants(self):
        for ant in self.world.ants:
            ant_surf = pygame.Surface((ant.width, ant.height),
                                        pygame.SRCALPHA, 32)
            ant_surf.fill(ant.color)
            ant_surf = pygame.transform.rotate(ant_surf,
                math.degrees(ant.orientation))
            # re-center the ant, after rotation
            w, h = ant_surf.get_width(), ant_surf.get_height()
            pos_x, pos_y = ant.rect.center
            top_left = (pos_x - w/2, pos_y - h/2)
            self.surface.blit(ant_surf, top_left)

            # draw outline and center
            # outline = pygame.Rect(top_left[0], top_left[1], w, h)
            # pygame.draw.rect(self.surface, (0, 255, 0, 255), outline, 1)
            # pygame.draw.circle(self.surface, (255, 0, 0, 255), ant.rect.center, 20, 1)

    def __render_items(self):
        for obj in self.world.items:
            obj_surf = pygame.Surface((obj.width, obj.height),
                                        pygame.SRCALPHA, 32)
            obj_surf.fill(obj.color)
            top_left = (obj.pos[0] - obj.width/2, obj.pos[1] - obj.height/2)
            self.surface.blit(obj_surf, top_left)

            # draw outline and center
            # outline = pygame.Rect(top_left[0], top_left[1], obj.width, obj.height)
            # pygame.draw.rect(self.surface, (0, 255, 0, 255), outline, 1)
            # pygame.draw.circle(self.surface, (255, 0, 0, 255), obj.rect.center, 20, 1)

    def __render_colony(self):
        (width, height) = self.world.colony.get_dimensions()
        colony_surface = pygame.Surface((width, height),
                                    pygame.SRCALPHA, 32)
        colony_surface.fill(self.world.colony.get_color())
        pos = self.world.colony.get_position()
        top_left = (pos[0] - width/2, pos[1] - height/2)
        self.surface.blit(colony_surface, top_left)
