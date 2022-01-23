import pygame as pg


class Resources:

    def __init__(self,w,r,f):
        self.w = 0
        self.r = 0
        self.f = 0

        #Cost of bulding hut
        self.hut_cost_w = 0
        self.hut_cost_f = 0
        self.hut_cost_r = 0

        #cost of a wall
        self.wall_cost_w = 0

        #cost of a tower
        self.tower_cost_w = 0

