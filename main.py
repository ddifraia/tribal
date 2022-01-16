import pygame as pg
from game.game import Game

def main():

    running = True
    playing = True

    #initialize pygame
    pg.init()
    pg.mixer

    #crate screen full screen mode
    screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
    #create clock
    clock = pg.time.Clock()

    #implement menues

    #implement game
    game = Game(screen,clock)

    while running:
        #here will go the menu
        #<<<<
        while playing:
            #game loop here
            game.run()


if __name__ == '__main__':
    main()
