import os

import pygame as pg
from .utils import scale_image

class Hut:

    def __init__(self,pos_x,pos_y,render_pos):

        self.wood_cost = 10
        self.food_cost = 0
        self.rock_cost = 0

        self.name = "small_hut"
        self.health = 2000

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.render_pos = render_pos

        self.tile = "building_site"
        self.tile_complete = "small_hut"

        #take image and scale image for bulding site and not complete
        self.image = pg.image.load("assets/graphics/building_site.png").convert_alpha()
        self.complete = False

        self.building_time = 200
        self.building_time_original = self.building_time
        self.perc_completed = 0

        self.building_rect = pg.Rect((0,0),(0,4))

        image_complete = pg.image.load("assets/graphics/hut01.png").convert_alpha()
        self.image_complete = scale_image(image_complete,w=128)
        self.rect = self.image_complete.get_rect()

        self.grid = [self.pos_x, self.pos_y]
        self.state = "alive"

        #object type
        self.type = "building"

        # Rectange
        self.rect_coll = None
        self.poly_coll = None

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
        pass

