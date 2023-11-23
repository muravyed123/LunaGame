import pygame as pg

import globalsc as G
screen = pg.Surface((1280, 720), G.WHITE) 
class camera:
    def __init__(self, active):
        self.x = 0
        self.y = 0
        self.active = active
    def move(self, vel):
        self.x += vel[0]
        self.y += vel[1]
def update(event):
    pg.draw.rect(screen, G.BLACK, (600, 12, 400, 20))

    return(screen)