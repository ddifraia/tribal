import random

import pygame as pg

class Projectile:
    
    def __init__(self,x,y,y_end,speed):

        self.origin_x = 0
        self.origin_y = 0

        self.x = x + random.randint(1,3)
        self.y = y + random.randint(1,3)

        self.y_end = y_end + random.randint(1,10)
        self.speed = speed + random.randint(0,2)
        
        self.gravity = 0.9
        self.expires = 10

        self.rect = pg.Rect((x,y),(50,2))

    def move(self,camera_speed):
        if self.speed != 0:
           self.rect.y += 1
           self.rect.x += self.speed
           self.speed -= 0.05

        if pg.key.get_pressed()[pg.K_d]:
            self.rect.x -= camera_speed
        if pg.key.get_pressed()[pg.K_w]:
            self.rect.y += camera_speed
        if pg.key.get_pressed()[pg.K_s]:
            self.rect.y -= camera_speed
        if pg.key.get_pressed()[pg.K_a]:
            self.rect.x += camera_speed

        if self.rect.y >= self.y_end:
            self.speed = 0
            self.expires += 1

        if self.expires <= 0:
            del self
