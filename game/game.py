import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE
from .utils import draw_text
from .camera import Camera
from .hud import Hud
from .player import Player
from .resources import Resources
from .buildings import Hut


class Game:
    #init game
    def __init__(self,screen,clock):

        self.screen = screen
        self.clock = clock
        self.width,self.height = screen.get_size()
        #Create World
        self.world = World(20,20,self.width,self.height)
        #Add Camera
        self.camera = Camera(self.width,self.height,self.world.grid_length_x,self.world.grid_length_y)

        #Player
        self.player = Player(self.width,self.height)
        # Resources
        self.resources = Resources(0, 0, 0)
        # Hud
        self.hud = Hud(self.width, self.height, self.world, self.player,self.resources)

    def run(self):
        self.playing = True

        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

            #check if there is a mouse left click
            if event.type == pg.MOUSEBUTTONDOWN:
               if event.button == 1:
                   return "left_click"

    def update(self):
        self.camera.update()
        self.hud.update()

    def draw_env_element(self,obj):
        if obj.type == "enviroment":
            # extract tile
            tile = obj.tile
            # update render position
            render_pos = obj.render_pos.copy()
            # check if we are placing an element
            position = (obj.render_pos[0] + self.world.grass_tiles.get_width() / 2 + self.camera.scroll.x,
                        obj.render_pos[1] - TILE_SIZE + self.camera.scroll.y)

            # make collision rect
            obj.set_collision_rect(position)

            # blit on screen
            self.screen.blit(self.world.tiles[tile], position)

            # Show tree rectangle
            if obj.name == "tree" and pg.key.get_pressed()[pg.K_SPACE]:
                # update rect position
                pg.draw.rect(self.screen, pg.Color("White"), obj.rect_coll, width=1)

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.world.grass_tiles,(self.camera.scroll.x,self.camera.scroll.y))
        self.hud.draw_player(self.screen)

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                #extract object
                obj = self.world.world[x][y]
                #draw enviroment elements
                self.draw_env_element(obj)
                #Check if player harvest a tree
                self.player.harvest_tree(obj,self.screen,self.events(),self.resources)

        #Draw hud
        self.hud.draw(self.screen)

        draw_text(self.screen,
                  'fps={}'.format(round(self.clock.get_fps())),
                  25,
                  (255,255,255),
                  (0,0))

        #update display
        pg.display.flip()

    def draw_tile(self,render_pos,tile):
        self.screen.blit(self.world.tiles[tile], (render_pos[0] + self.width / 2, render_pos[1] + self.height / 8))

    #Function that places building in the right place
    def player_builds(self,obj):
        #Check if player has selected a tile
        if self.hud.selected_tile not None:
            # get mouse pos
            mouse_pos = pg.mouse.get_pos()
            mouse_action = pg.mouse.get_pressed()
            #check if mouse collide with object
            if obj.rect_coll.collidepoint(mouse_pos) and mouse_action[0]:
                #place the correct object in drid
                if self.hud.selected_tile["name"] == "small_hut":
                    obj




