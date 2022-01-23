import pygame as pg
from .settings import TILE_SIZE

def draw_text(screen,text,size,color,pos):
    font = pg.font.SysFont(None,size)
    text_surface = font.render(text,True,color).convert_alpha()
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface,text_rect)


def scale_image(image,w=None,h=None):

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


    if pos[0] > iso_poly[0][0]:
        pass


def cart_to_iso(x,y):
     iso_x = x - y
     iso_y = (x + y) / 2
     return iso_x,iso_y

def update_coord_with_player_move(x,y,camera_speed):
    if pg.key.get_pressed()[pg.K_d]:
        x -= camera_speed
    if pg.key.get_pressed()[pg.K_w]:
        y += camera_speed
    if pg.key.get_pressed()[pg.K_s]:
        y -= camera_speed
    if pg.key.get_pressed()[pg.K_a]:
        x += camera_speed

    return (x,y)

def pos_to_grid(x,y):
    x = int(x / TILE_SIZE * 2)
    y = int(y / TILE_SIZE / 2)
    return (x,y)

def determineSide(rect1, rect2):
    if rect1.midtop[1] > rect2.midtop[1]:
        return "top"
    elif rect1.midleft[0] > rect2.midleft[0]:
        return "left"
    elif rect1.midright[0] < rect2.midright[0]:
        return "right"
    else:
        return "bottom"