import pygame as pg
import sys
import menu
import draw

import globalsc as G 

active = True
 
clock = pg.time.Clock()
sc = pg.display.set_mode((G.WIDTH, G.HEIGHT))
def exit_pr():
    active = False
    sys.exit()
menu.start()
draw.change_scene(1)
pg.display.set_caption('Game')
while active:
    clock.tick(G.FPS)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            sys.exit()
            
    keys = pg.key.get_pressed()
    sc.fill(G.WHITE)
    sc.blit(draw.update(events, keys), (0,0))
    sc.blit(menu.update(events), (0,0))
    pg.display.update()