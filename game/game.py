import random

import pygame as pg
import sys
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from .world import World
from .settings import TILE_SIZE
from .utils import draw_text,determineSide
from .camera import Camera
from .hud import Hud
from .player import Player
from .resources import Resources
from .buildings import Hut, Wall, Tower
from .environment import Grass,Animal
from .projectile import Projectile


class Game:
    #init game
    def __init__(self,screen,clock):

        self.screen = screen
        self.clock = clock
        self.width,self.height = screen.get_size()

        #Create World
        self.world = World(10,10,self.width,self.height)
        # Player
        self.player = Player(self.width, self.height)

        #Add Camera
        self.camera = Camera(self.width,self.height,self.world.grid_length_x,self.world.grid_length_y,self.player)

        # Resources
        self.resources = Resources(0, 0, 0)
        # Hud
        self.hud = Hud(self.width, self.height, self.world, self.player,self.resources)
        #projectile
        self.projectile = []

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
                #Check if we need to initialize a projectile
                self.inizialize_projectile(event=event)
                if event.key == pg.K_r:
                    self.rotate_builing_tile()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LALT and self.player.projectiles_count>0:
                    #here it appends the projectile to the game
                    self.projectile.append(self.player.projectiles)
                    self.player.projectiles = None
                    self.player.projectiles_count -= 1
            #mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                #left click of the mouse
                if event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    # Control menu, select object
                    self.hud.select_tool(mouse_pos)
                    self.place_builing_in_grid()
                    self.player.pick_projectile(self.projectile)
                # if it is right click exit build mode
                if event.button == 3:
                    self.hud.builds = False
            #mouse release button, when building, but not when selecting axe
            if event.type == pg.MOUSEBUTTONUP and self.hud.selected_tile is not None and self.hud.selected_tile["name"] != "axe":
                if event.button == 1:
                    self.hud.builds = True

        #Check if we need to load a projectiles
        self.load_projectiles()
        #Check if animal is hit by projectile
        self.animal_hits()


    def update(self):
        self.camera.update()
        self.hud.update()

    def draw_env_element(self,obj):

        # check if we are placing an element
        position = (obj.render_pos[0] + self.world.grass_tiles.get_width() / 2 + self.camera.scroll.x,
                    obj.render_pos[1] - TILE_SIZE + self.camera.scroll.y)

        pos_offset_x = self.world.grass_tiles.get_width() / 2 + self.camera.scroll.x
        pos_offset_y = self.camera.scroll.y

        #make collision rect
        obj.set_collision_rect(position)

        if obj.type == "enviroment":
            # extract tile
            tile = obj.tile
            # update render position
            render_pos = obj.render_pos.copy()
            # blit on screen
            self.screen.blit(self.world.tiles[tile], position)

        if obj.type == "building":
            tile = obj.tile
            #tower must be placed with a biggest offset
            if obj.name == "tower" and obj.complete:
                h = (tile.get_height() + TILE_SIZE) / 2
                self.screen.blit(tile, (position[0],position[1]-h))
            else:
                self.screen.blit(tile,position)
            if pg.key.get_pressed()[pg.K_SPACE]:
                pg.draw.rect(self.screen, pg.Color("Red"), obj.rect_coll)


        # Show tree rectangle
        if obj.name == "tree" and pg.key.get_pressed()[pg.K_SPACE]:
            # update rect position
            pg.draw.rect(self.screen, pg.Color("White"), obj.rect_coll, width=1)
            new_pol = self.polygon_offset(obj.iso_poly, pos_offset_x, pos_offset_y)
            obj.poly_coll = new_pol
            pg.draw.polygon(self.screen, pg.Color("Green"), obj.poly_coll, width=1)

        # Show grass rectangle and update isometric polygon position
        if obj.name == "grass":
            new_pol = self.polygon_offset(obj.iso_poly,pos_offset_x,pos_offset_y)
            obj.poly_coll = new_pol

    #Main game drawing/display loop
    def draw(self):
        self.set_map_border()
        self.screen.fill((0,0,0))
        self.screen.blit(self.world.grass_tiles,(self.camera.scroll.x,self.camera.scroll.y))
        self.move_projectiles()
        self.spread_animal(p=10)
        self.hud.draw_player(self.screen)

        #print world tiles and check some player actions
        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                # extract the object
                obj = self.world.world[x][y]
                #draw enviroment elements
                self.draw_env_element(obj)
                #Check if player harvest a tree <<< this could probably be removed from here
                self.player.harvest_tree(obj,self.screen,self.resources)
                #player builds the object ?
                self.player.builds_time(obj)
                #draw any building process bar
                self.draw_building_progress(obj)

        #Draw hud
        self.hud.draw(self.screen)
        draw_text(self.screen,'fps={}'.format(round(self.clock.get_fps())),25,(255,255,255),(0,0))
        #show animal health with L_CTR
        self.draw_animal_health()
        pg.draw.rect(self.screen,pg.Color("Blue"),self.player.base_rect)
        draw_text(self.screen, self.player.move, 20, pg.Color("White"), (60, 60))
        #update display
        pg.display.flip()

    def draw_tile(self,render_pos,tile):
        self.screen.blit(self.world.tiles[tile], (render_pos[0] + self.width / 2, render_pos[1] + self.height / 8))

    #Function that places building in the right place
    def player_builds(self,obj,x,y):
        # get mouse pos
        mouse_pos = pg.mouse.get_pos()

        #check if mouse collide with object
        if obj.rect_coll.collidepoint(mouse_pos):
            #use Polygon <<
            point = Point(mouse_pos[0],mouse_pos[1])
            polygon = Polygon(obj.poly_coll)

            #If mouse is inside isometric polygon
            if polygon.contains(point):
                self.place_buildings(obj,x,y)

    def polygon_offset(self,iso_poly,pos_offset_x,pos_offset_y):
        new_poly = []
        for x,y in iso_poly:
            x = x + pos_offset_x
            y = y + pos_offset_y
            coords = (x,y)
            new_poly.append(coords)

        return new_poly

    #function that place the different buildings
    def place_builing_in_grid(self):
        # check if we are builing mode
            for x in range(self.world.grid_length_x):
                for y in range(self.world.grid_length_y):
                    obj = self.world.world[x][y]
                    #if we are in building more we need to place buildings in grid
                    if self.hud.builds:
                        self.player_builds(obj, x, y)

    def place_buildings(self,obj,x,y):
        #choose what to place << Hut
        if self.hud.selected_tile["name"] == "small_hut":
            # check if you have resources
            tile = self.world.tiles["small_hut"]
            #place a HUT <<<<<<<<<<<<<
            if self.resources.w >= self.resources.hut_cost_w:
                self.world.world[x][y] = Hut(obj.pos_x, obj.pos_y, obj.render_pos,tile)
                self.world.buildings.append(self.world.world[x][y])
                #remove resources
                self.resources.w -= self.resources.hut_cost_w

        #place a WALL <<<<<<<<<<<<
        if self.hud.selected_tile["name"] == "wall":
            tile = self.world.tiles["wall"]
            # check if you have resources
            if self.resources.w >= self.resources.wall_cost_w:
                self.world.world[x][y] = Wall(obj.pos_x, obj.pos_y, obj.render_pos,tile)
                self.world.buildings.append(self.world.world[x][y])
                # remove resources
                self.resources.w -= self.resources.wall_cost_w

        # place a TOWER <<<<<<<<<<<<
        if self.hud.selected_tile["name"] == "tower":
            tile = self.world.tiles["tower"]
            # check if you have resources
            if self.resources.w >= self.resources.wall_cost_w:
               self.world.world[x][y] = Tower(obj.pos_x, obj.pos_y, obj.render_pos, tile)
               self.world.buildings.append(self.world.world[x][y])
               # remove resources
               self.resources.w -= self.resources.wall_cost_w

    def set_map_border(self):
        #Take map border
        rect = self.world.grass_tiles.get_rect()
        rect.width = rect.width / 2
        rect.height = rect.height / 2
        #add camera offset
        pos_offset_x = self.world.grass_tiles.get_width() / 2 + self.camera.scroll.x
        pos_offset_y = self.camera.scroll.y

        # covert to a isometric polygon
        poly = [rect.topleft, rect.topright,rect.bottomright, rect.bottomleft]
        iso_poly = [self.world.cart_to_iso(x,y) for x,y in poly]
        rect.x += pos_offset_x
        rect.y += pos_offset_y

        #create new polygon
        new_pol = self.polygon_offset(iso_poly, pos_offset_x, pos_offset_y)

        #show map border with shift
        if pg.key.get_pressed()[pg.K_LSHIFT]:
            pg.draw.polygon(self.screen, pg.Color("Red"), new_pol, width=2)

        self.world.map_border = new_pol

    def draw_building_progress(self,obj):
        if obj.type == "building" and obj.building_time > 0:
            text = 'Building : {}'.format(round(obj.perc_completed*100))+"% completed..."
            progress_bar = pg.Rect((obj.rect_coll.x,obj.rect_coll.y-20),(obj.building_rect.width,obj.building_rect.height))

            draw_text(self.screen,text,20,pg.Color("White"),(obj.rect_coll.x,obj.rect_coll.y-40))
            #pg.draw.rect(self.screen,pg.Color("Blue"),obj.rect_coll,width=2)
            pg.draw.rect(self.screen, pg.Color("Green"), progress_bar)

    def rotate_builing_tile(self):
        #if we are in building mode
        if self.hud.selected_tile is not None:
            #Get selected tile from hud
            tile =  self.hud.selected_tile["image"]
            tile_name = self.hud.selected_tile["name"]
            #rotate the selected tile and the tile in the world
            tile_w = self.world.tiles[tile_name]

            self.hud.selected_tile["image"] =  pg.transform.flip(tile,True,False)
            self.world.tiles[tile_name] = pg.transform.flip(tile_w,True,False)

    ## Function for projectiles handling

    def set_projectile_speed(self,speed=0):
        if pg.key.get_pressed()[pg.K_LALT]:
            speed += 1
        if speed >= 10:
            speed = 10
        return speed

    def draw_projective(self,projectile):
        pg.draw.rect(self.screen,pg.Color("Brown"),projectile.rect,0)

    def clean_projectiles(self,projectiles):
        if projectiles.expires <= 0:
            del projectiles

    def move_projectiles(self):# draw projectiles <<<< function
        for x in self.projectile:
            x.move(self.camera.speed)
            self.draw_projective(x)
            self.clean_projectiles(x)

    def load_projectiles(self):
        # Check if we need to load projectile <<< function
        if pg.key.get_pressed()[pg.K_LALT] and self.player.projectiles is not None:
            load = 0.001
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < (self.player.width / 2):
                self.player.projectiles.speed -= 0.1
            if mouse_pos[0] > (self.player.width / 2):
                self.player.projectiles.speed += 0.1

            if (self.player.projectiles.speed) >= 10:
                self.player.projectiles.speed = 10 + random.randint(0, 3)
            if (self.player.projectiles.speed) <= -10:
                self.player.projectiles.speed = -10 + random.randint(0, 3)

    def inizialize_projectile(self,event):
        if event.key == pg.K_LALT and self.player.projectiles is None:
            if self.player.projectiles_count > 0:
                projectile = Projectile(self.player.width / 2, self.player.height / 2,
                                        (self.player.height + 64) / 2, 0)
                self.player.projectiles = projectile
    #Managing animals, main animal manager
    #main animal manager
    def spread_animal(self, p=100):
        # always place an animal
        if random.randint(1, p) == 2 and len(self.world.animal) <= 3:

            x_pos = random.randint(min([i[0] for i in self.world.map_border]),
                                   max([i[0] for i in self.world.map_border]))
            y_pos = random.randint(min([i[1] for i in self.world.map_border]),
                                   max([i[1] for i in self.world.map_border]))
            p = Point(x_pos, y_pos)
            poly = Polygon(self.world.map_border)

            if poly.contains(p):
                # check if x_pos and y_pos collide with grass surface
                animal = Animal(x_pos, y_pos,self.player)
                self.world.animal.append(animal)

        # for all animals
        for animal in self.world.animal:
            animal.move(camera=self.camera,player=self.player)
            self.screen.blit(animal.sprite, (animal.x,
                                             animal.y))
            if animal.move_time <= 0:
                del animal

            # pos
            pos = Point(animal.x, animal.y)
            poly = Polygon(self.world.map_border)

            # check if the animal is harvested by player are harvested
            self.player.harvest_food(animal=animal, resources=self.resources,
                                     screen=self.screen)

            # if it goes outise the map delete
            if not poly.contains(pos):
                self.world.animal.remove(animal)

            # check if no food is left in animal, remove it
            if animal.food <= 0:
                self.world.animal.remove(animal)

    #check if animal is hit
    def animal_hits(self):
        draw_text(self.screen,'cacca', 25, (255, 255, 255), (200, 200))

        for anim in self.world.animal:
            anim_rect = anim.rect
            for prj  in self.projectile:
                prj_rect = prj.rect
                if abs(prj.speed) > 0 and anim_rect.colliderect(prj_rect):
                    damage = abs(prj.speed) * 2
                    anim.health -= damage
                    anim.check_alive()

    #draw animal stats, and if is harvested
    def draw_animal_health(self):
        #show health and rectangle
        for an in self.world.animal:
            an.show_health(screen=self.screen)

