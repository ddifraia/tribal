import random

import pygame as pg
from .settings import SCROLL_SPEED, TILE_SIZE

class Camera:
    def __init__(self,width,height,grid_length_x,grid_length_y):
        self.width = width
        self.height = height

        #start with random position
        start_pos_x = 0
        start_pos_y = 0

        self.scroll = pg.Vector2(start_pos_x,start_pos_y)
        self.dx = 0
        self.dy = 0
        self.speed = SCROLL_SPEED

    def update(self):
        #get mouse pos
        mouse_pos = pg.mouse.get_pos()
        key_pressed = pg.key.get_pressed()

        #check x position
        if (mouse_pos[0] > self.width * 0.97) or (key_pressed[pg.K_d]):
            self.dx = -self.speed
        elif (mouse_pos[0] < self.width * 0.03) or (key_pressed[pg.K_a]):
            self.dx = self.speed
        else:
            self.dx = 0

        #check y position of mouse
        if (mouse_pos[1] > self.height * 0.97) or (key_pressed[pg.K_s]):
            self.dy = -self.speed
        elif (mouse_pos[1] < self.height * 0.03) or (key_pressed[pg.K_w]):
            self.dy = self.speed
        else:
            self.dy = 0


        self.scroll.x += self.dx
        self.scroll.y += self.dy

