import os

import pygame as pg


class Hut:

    def __init__(self,pos_x,pos_y,render_pos):

        self.wood_cost = 30
        self.food_cost = 0
        self.rock_cost = 0

        self.name = "small_hut"
        self.health = 2000

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.render_pos = render_pos

        self.tile = pg.image.load("assets/graphics/hut01.png").convert_alpha()

        self.grid = [self.pos_x, self.pos_y]
        self.state = "alive"

        # Rectange
        self.rect_coll = None

    #create collision rect according to render
    def set_collision_rect(self, render_pos):
        self.rect_coll = self.tile.get_rect(topleft=render_pos)

    def produce(self):
        while self.state == "produce":
            os.wait(1)
            self.timer += 1

