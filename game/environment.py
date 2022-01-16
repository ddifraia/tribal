import pygame as pg


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







