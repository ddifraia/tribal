import pygame as pg
import random
import noise
from .settings import TILE_SIZE
from .environment import Tree,Rock,Grass
from .utils import scale_image



class World:

    #always good to save params into objects
    def __init__(self,grid_length_x,grid_length_y,width,height):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.grass_tiles = pg.Surface((grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE * 2)).convert_alpha()

        self.map_border = None

        self.perlin_scale = grid_length_x/10
        self.tiles = self.load_images()
        self.world = self.create_world()

        #animal list
        self.animal = []

    def create_world(self):
        #initialize grid
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x,grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile.render_pos
                self.grass_tiles.blit(self.tiles["grass"],
                                      (render_pos[0] + self.grass_tiles.get_width()/2,render_pos[1]))

        return world

    def grid_to_world(self,grid_x,grid_y):
        #il rettangolo ha una posizione specifica dettata da grid_x and grid_y
        #deve essere poi messo nella posizione giusta
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
        ]

        iso_poly = [self.cart_to_iso(x,y) for x,y in rect]

        minx = min([x for x,y in iso_poly])
        miny = min([y for x,y in iso_poly])

        #choose if to put trees
        r = random.randint(1,100)
        perlin = 100 * noise.pnoise2(grid_x/self.perlin_scale,grid_y/self.perlin_scale)

        if (perlin >= 15) or perlin <= -35:
            trees = ["tree","tree2","tree3","tree4"]
            tile = trees[random.randint(0,len(trees)-1)]
            image = self.tiles[tile]
            obj = Tree(grid_x, grid_y, rect, iso_poly, [minx, miny], tile,image)
        else:
            if r == 1:
                tile = "rock"
                image = self.tiles[tile]
                obj = Rock(grid_x,grid_y,rect,iso_poly,[minx,miny],tile,image)
            elif r == 3:
                tile = "tree"
                image = self.tiles[tile]
                obj = Tree(grid_x,grid_y,rect,iso_poly,[minx,miny],tile,image)
            else:
                tile = "grass"
                image = self.tiles[tile]
                obj = Grass(grid_x,grid_y,rect,iso_poly,[minx,miny],tile,image)


        out = obj

        return out

    def load_images(self):
        grass = pg.image.load('assets/graphics/grass.png').convert_alpha()
        tree =  pg.image.load('assets/graphics/tree.png').convert_alpha()
        tree2 = pg.image.load('assets/graphics/tree2.png').convert_alpha()
        tree3 = pg.image.load('assets/graphics/tree3.png').convert_alpha()
        tree4 = pg.image.load('assets/graphics/tree4.png').convert_alpha()
        hut = pg.image.load('assets/graphics/hut01.png').convert_alpha()
        rock =  pg.image.load('assets/graphics/rock.png').convert_alpha()

        tree = pg.transform.scale(tree, (128, 128))
        tree2 = pg.transform.scale(tree2, (128, 128))
        tree3 = pg.transform.scale(tree3, (128, 128))
        tree4 = pg.transform.scale(tree4, (128, 128))
        hut = scale_image(hut,w=128)
        rock = pg.transform.scale(rock, (128, 128))
        grass = pg.transform.scale(grass,(128,128))

        return {"grass":grass,
                "tree":tree,"tree2":tree2,
                "tree3":tree3,"tree4":tree4,
                "rock":rock,
                "small_hut":hut}

    def cart_to_iso(self,x,y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x,iso_y


