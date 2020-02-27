import pygame, sys, time
from pygame.locals import *
from setup import *

def __main__():
    bgMusic()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                run = False
        screen.blit(Variables.bgImage, [0, 0])
        MenuButton("New Game", 325, 400, 150, 30, Color.white, Color.Gray, "play")
        MenuButton("Load Game", 325, 450, 150, 30, Color.white, Color.Gray, "load")
        MenuButton("Option", 325, 500, 150, 30, Color.white, Color.Gray, 'option')
        MenuButton("Quit", 325, 550, 150, 30,  Color.white, Color.Gray, "quit")

        Title('PSB Battle Game', Variables.textX, Variables.textY)
        Player()
        pygame.display.flip()
        Variables.fpsClock.tick(Variables.FPS)


if __name__ == '__main__':
    __main__()
