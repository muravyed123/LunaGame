import pygame as pg
import sys
import menu
 
FPS = 60
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1280
HEIGHT = 720
active = True
 
clock = pg.time.Clock()
sc = pg.display.set_mode((WIDTH, HEIGHT))
def exit():
    sys.exit()
menu.start()

pg.display.set_caption('Game')
while active:
    clock.tick(FPS)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            sys.exit()
    sc.fill(WHITE)
    sc.blit(menu.update(events), (0,0))
    pg.display.update()