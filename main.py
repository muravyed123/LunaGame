import pygame as pg
import sys
import menu
import draw
import Sound as sound

import globalsc as G


active = True
 
clock = pg.time.Clock()
sc = pg.display.set_mode((0,0), pg.FULLSCREEN)
def exit_pr():
    active = False
    sys.exit()
menu.start()
draw.change_scene(1, 1)
pg.display.set_caption('Game')
#sound.start_play_fon_music(0)
while active:
    clock.tick(G.FPS)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            sys.exit()
            
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        sys.exit()
    sc.fill(G.WHITE)
    sc.blit(draw.update(events, keys), (0,0))
    sc.blit(menu.update(events), (0,0))
    pg.display.update()