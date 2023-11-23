import pygame as pg
import sys
import menu
import draw

import globalsc as G 

active = True
 
clock = pg.time.Clock()
sc = pg.display.set_mode((G.WIDTH, G.HEIGHT))
def exit():
    sys.exit()
menu.start()

pg.display.set_caption('Game')
while active:
    clock.tick(G.FPS)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            sys.exit()
    sc.fill(G.WHITE)
    sc.blit(menu.update(events), (0,0))
    sc.blit(draw.update(events), (0,0))
    pg.display.update()