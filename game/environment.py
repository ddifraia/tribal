import random

import pygame as pg
import pybox2d as pb
from .utils import scale_image


class Tree:

    def __init__(self,pos_x,pos_y,rect,iso_poly,render_pos,tile,image):

        self.name = "tree"
        self.health = 2000

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.rect = rect
        self.iso_poly = iso_poly
        self.render_pos = render_pos

        self.tile = tile

        self.grid = [self.pos_x, self.pos_y]
        self.state = "alive"

        #type of object
        self.type = "enviroment"
        #image
        self.image = self.scale_image(image,w=128)
        #Rectange
        self.rect_coll = None
        self.poly_coll = None
        #state
        self.state = "busy"

    def update(self):
        if self.health <= 0:
            self.tile = "grass"
            self.state = "dead"

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

    def set_collision_rect(self,render_pos):
        self.rect_coll = self.image.get_rect(topleft=render_pos)



class Rock:

    def __init__(self, pos_x, pos_y, rect, iso_poly, render_pos, tile,image):

        self.wood_cost = 0
        self.food_cost = 0
        self.rock_cost = 0

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = "rock"

        self.grid = [self.pos_x,self.pos_y]

        self.rect = rect
        self.iso_poly = iso_poly
        self.render_pos = render_pos
        self.tile = tile
        self.image = self.scale_image(image, w=128)

        # type of object
        self.type = "enviroment"
        # state
        self.state = "busy"

        #collisions shapes
        self.rect_coll = None
        self.poly_coll = None

    def set_collision_rect(self,render_pos):
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

    def set_collision_rect(self, render_pos):
        self.rect_coll = self.image.get_rect(topleft=render_pos)



class Grass():

    def __init__(self, pos_x, pos_y, rect, iso_poly, render_pos, tile,image):
        self.wood_cost = 0
        self.food_cost = 0
        self.rock_cost = 0

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.grid = [self.pos_x,self.pos_y]
        self.name = "grass"
        self.rect = rect
        self.iso_poly = iso_poly
        self.render_pos = render_pos
        self.tile = tile
        self.image = self.scale_image(image, w=128)

        # type of object
        self.type = "grass"
        self.rect_coll = None
        self.poly_coll = None

        #state
        self.state = "free"

    def set_collision_rect(self,render_pos):
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



class Animal:

    def __init__(self,x,y):

        self.health = 50
        self.speed = 0.5
        self.food = 10

        self.x = x
        self.y = y

        self.rand_move = random.randint(60,300)
        self.move_dir = random.randint(1,6)
        self.move_time = random.randint(60,800)

        #load sprite
        sprite = pg.image.load("assets/graphics/food.png").convert_alpha()
        self.sprite = scale_image(sprite,w=20)

    def move(self):
        #move on x axis
        #Random movement
        if self.move_dir == 1 and self.rand_move > 0:
            #for how much
            self.x += self.speed
            self.y += self.speed / 2
            self.rand_move -= self.speed
        elif self.move_dir == 2 and self.rand_move > 0:
            self.x -= self.speed
            self.y -= self.speed / 2
            self.rand_move -= self.speed
        elif self.move_dir == 3 and self.rand_move > 0:
            self.y -= self.speed / 2
            self.x += self.speed
            self.rand_move -= self.speed
        elif self.move_dir == 4 and self.rand_move > 0:
            self.y += self.speed / 2
            self.x -= self.speed
            self.rand_move -= self.speed
        elif self.move_dir == 5 and self.rand_move > 0:
            self.y += self.speed
            self.rand_move -= self.speed
        elif self.move_dir == 6 and self.rand_move > 0:
            self.y -= self.speed
            self.rand_move -= self.speed

        #check if random movement is finished
        if self.rand_move <= 0:
            self.move_dir = random.randint(1,8)
            self.rand_move = random.randint(60,300)




