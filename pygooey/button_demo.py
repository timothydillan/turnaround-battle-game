
#button example use

import pygooey
import pygame as pg

pg.init()
screen = pg.display.set_mode((600,400))
screen_rect = screen.get_rect()
done = False

def print_on_press():
    print('button pressed')

#see all settings help(pygooey.Button.__init__)
settings = {
    "clicked_font_color" : (0,0,0),
    "hover_font_color"   : (205,195, 100),
    'font'               : pg.font.Font(None,16),
    'font_color'         : (255,255,255),
    'border_color'       : (0,0,0),
}

btn = pygooey.Button(rect=(10,10,105,25), command=print_on_press, text='Press Me', **settings)

while not done:
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        btn.get_event(event)
    btn.draw(screen)
    pg.display.update()
