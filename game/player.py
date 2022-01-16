import pygame as pg
from .settings import PLAYER_HEALTH
from .utils import draw_text
from .settings import RES_WOOD
from .resources import Resources

class Player:

    def __init__(self,width,heigth):

        self.width = width
        self.height = heigth
        self.health = PLAYER_HEALTH
        self.images = self.load_images()
        self.rect = self.images["player_static"].get_rect(topleft=(self.width/2,self.height/2))
        self.state = "static"
        self.event = pg.event

    def scale_image(self,image,w=None,h=None):

        if (w == None) and (h==None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image,(int(w),int(h)))
        elif w == None:
            scale = h / image.get_heigth()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image,(int(w),int(h)))

        return image

    def load_images(self):

        #Load images for player - static
        player_static = pg.image.load('assets/graphics/player/player_stick_base.png').convert_alpha()
        player_axe = pg.image.load('assets/graphics/player/player_stick_axe.png').convert_alpha()

        player_static = self.scale_image(player_static,w=50).convert_alpha()
        player_axe = self.scale_image(player_axe,w=50).convert_alpha()

        return {
                "player_static": player_static,
                "player_axe":player_axe
                }

    def draw(self,screen):

        #draw the different player state
        if self.state == "static":
            screen.blit(self.load_images()["player_static"],(self.width/2,self.height/2))
        elif self.state == "axe":
            screen.blit(self.load_images()["player_axe"],(self.width/2,self.height/2))

    def harvest_tree(self,obj,screen,events,resources):
        #only if the object is a tree
        if obj.name == "tree":

            #function for harvesting tree
            if self.rect.colliderect(obj.rect_coll) and self.state == "axe":
                #check if mouse is in position and on click
                mouse_pos = pg.mouse.get_pos()
                mouse_action = pg.mouse.get_pressed()

                #if mouse collide with rect of obje and left click
                if obj.rect_coll.collidepoint(mouse_pos) and mouse_action[0]:
                    obj.health -= 10
                    resources.w += 0.01
                    draw_text(screen, str(obj.health), 24, (255, 0, 0), obj.rect_coll.center)

                #check if the tree has less than 0 points
                if obj.health < 0:
                   obj.name = "grass"




