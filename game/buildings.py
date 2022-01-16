import os

import pygame as pg
from .utils import scale_image

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

        self.tile = "small_hut"

        #take image and scale
        image = pg.image.load("assets/graphics/hut01.png").convert_alpha()
        self.image = scale_image(image,w=128)

        self.grid = [self.pos_x, self.pos_y]
        self.state = "alive"

        #object type
        self.type = "building"

        # Rectange
        self.rect_coll = None

    #create collision rect according to render
    def set_collision_rect(self, render_pos):
        self.rect_coll = self.image.get_rect(topleft=render_pos)

    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_heigth()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image
    def produce(self):
        while self.state == "produce":
            os.wait(1)
            self.timer += 1

