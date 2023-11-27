import pygame as pg
import sys

import globalsc as G

objects = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
bord = (490, 400, 300, 300, 5)
player = None

class Player:
    def __init__(self, x, y, typ):
        self.x = x
        self.floor = 450
        self.y = y
        self.v = 5
        self.rect =  pg.Rect(self.x, self.y, 40, 40) 
        self.image = pg.image.load('materials/cat_dgap.png')
        self.image = pg.transform.scale(
            self.image, (self.rect.width, self.rect.height))             
    def move(self, vel):
        self.x += self.v * vel[0]
        self.y -= self.v * vel[1]
        grans = [bord[0] + bord[-1], bord[0] + bord[2] - bord[-1] - self.rect.width, bord[1] + bord[-1], bord[1] + bord[3] - bord[-1] - self.rect.height]
        if self.x >= grans[1]:
            self.x = grans[1]
        elif self.x <= grans[0]:
            self.x = grans[0]
        if self.y >= grans[3]:
            self.y = grans[3]
        elif self.y <= grans[2]:
            self.y = grans[2]        
        self.rect = pg.Rect(self.x, self.y, self.rect.width, self.rect.height)
    def draw(self):
        #pg.draw.rect(screen, G.GREEN, self.rect)
        screen.blit(self.image, self.rect)
class Object():
    def __init__(self, fig, color, parameters,x = 0, y = 0):
        self.fig = fig
        self.x = x
        self.y = y
        self.color = color
        self.parameters = parameters
    def draw(self):
        if self.fig == 'rect':
            x, y, w, h, r = self.parameters
            pg.draw.rect(screen, self.color, (x, y, w, h), r)
def start(number):
    global player
    borders = Object('rect', G.WHITE, bord)
    objects.append(borders)
    player = Player(640, 400, number)
def get_scene(keys):
    screen.fill(G.BLACK)
    for i in objects:
        i.draw()
    player.draw()
    return(screen)
def update(vel):
    player.move(vel)
    return vel