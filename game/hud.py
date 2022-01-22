import pygame as pg
from .player import Player
from .utils import draw_text
from .settings import RES_WOOD
from .resources import Resources

class Hud:

    def __init__(self,width,heigth,world,player,resources):

        self.width = width
        self.height = heigth

        self.hud_color = (198,155,93,175) # last is trasparency

        #resource hud
        self.resources_surface = pg.Surface((width,heigth * 0.02),pg.SRCALPHA)
        self.resources_surface.fill(self.hud_color)

        #building hud
        self.build_surface = pg.Surface((width * 0.15,heigth * 0.25),pg.SRCALPHA)
        self.build_surface.fill(self.hud_color)

        #select hud
        self.select_surface = pg.Surface((width * 0.20,heigth* 0.25),pg.SRCALPHA)
        self.select_surface.fill(self.hud_color)

        #load images
        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        #selected object
        self.selected_tile = None
        self.builds = False

        #player
        self.player = player

        #world interaction
        self.world = world
        #Resources
        self.resources = resources


    def create_build_hud(self):

        #render pos
        render_pos = [self.width * 0.85 + 10,self.height * 0.75 + 10]
        #width of builing hud
        object_width = self.build_surface.get_width() // 3

        tiles = []

        for image_names,image in self.images.items():
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp,w=object_width)

            rect = image_scale.get_rect(topleft=pos)
            tiles.append({
                "name": image_names,
                "icon": image_scale,
                "rect": rect,
                "image": self.images[image_names]

            })

            render_pos[0] +=  image_scale.get_width() + 10
        #retunr the dictionary
        return tiles

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

    def draw(self,screen):

        #If you select the building
        if self.selected_tile is not None and self.selected_tile["name"] != "axe":
            img = self.selected_tile["image"].copy()
            img = self.scale_image(img,w=128)

            img.set_alpha(150)
            screen.blit(img,(pg.mouse.get_pos()[0]-img.get_width()/2,
                             pg.mouse.get_pos()[1]-img.get_height()/2))

        #draw resource rect
        screen.blit(self.resources_surface,(0,0))

        #draw resource count
        draw_text(screen,'Wood: {0:.0f}'.format(self.resources.w),24,(255,255,255),(self.width-400,0))
        draw_text(screen,'Food: {0:.0f}'.format(self.resources.f), 24, (255, 255, 255), (self.width - 300, 0))

        #build hub
        screen.blit(self.build_surface,(self.width * 0.85,self.height * 0.75))
        #select hud
        screen.blit(self.select_surface, (0, self.height * 0.75))

        #draw all bulding icon
        for tile in self.tiles:
            screen.blit(tile["icon"],tile["rect"].topleft)

    def draw_player(self,screen):

        if self.selected_tile is not None and self.selected_tile["name"] == "axe":
            self.player.state = "axe"
        elif self.selected_tile is None:
            self.player.state = "static"

        #draw the player
        self.player.draw(screen)

    def load_images(self):

        hut = pg.image.load('assets/graphics/hut01.png').convert_alpha()
        axe = pg.image.load('assets/graphics/axe.png').convert_alpha()
        return {
                "small_hut": hut,
                "axe":axe
                }

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

    def select_tool(self,mouse_pos):
        # Control menu
        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos):
                self.selected_tile = tile