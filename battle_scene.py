import pygame as pg
import sys

import globalsc as G

objects = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
bord = (490, 350, 230, 230, 5)
player = None
max_health = 100

pg.font.init()

class Player:
    def __init__(self, x, y, typ, health):
        global max_health
        self.x = x
        self.floor = 450
        self.y = y
        self.v = 4
        self.rect =  pg.Rect(self.x, self.y, 32, 32) 
        self.image = pg.image.load('materials/cat_dgap.png')
        self.image = pg.transform.scale(
            self.image, (self.rect.width, self.rect.height))  
        self.health = health
        max_health = health
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
        self.health -= 0.1
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
class Label():
    def __init__(self, text,  pos, color, font, font_name):
        self.x, self.y = pos
        self.font = pg.font.SysFont(font_name, font)
        self.color = color
        self.text = text
    def draw(self):
        text = self.font.render(self.text, True, self.color)        
        screen.blit(text, (self.x, self.y)) 
class Health():
    def __init__(self, pos, fontname):
        self.x, self.y = pos
        self.width = 80
        self.font = pg.font.SysFont(fontname, 30)
        self.height = 20
    def draw(self):
        pg.draw.rect(screen, G.RED, (self.x, self.y + 2, self.width, self.height))
        hl = player.health
        if hl >= 0:
            length = self.width * hl // max_health
            pg.draw.rect(screen, G.GREEN, (self.x, self.y + 2, length, self.height))
            text = self.font.render(str(int(hl//1)) + ' / ' + str(max_health), True, (255,255,255))     
            screen.blit(text, (self.x + 100, self.y)) 
def start(number):
    global player
    borders = Object('rect', G.WHITE, bord)
    objects.append(borders)
    s = Label(G.name, (390 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    s1 = Label('HP', (610 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    s2 = Label('LV ' + str(G.level), (510 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    health = Health((680, 600), 'showcardgothic')
    objects.append(s)
    objects.append(s1)
    objects.append(s2)
    objects.append(health)
    player = Player(640, 400, number, 100)
def get_scene(keys):
    screen.fill(G.BLACK)
    for i in objects:
        i.draw()
    player.draw()
    return(screen)
def update(vel):
    player.move(vel)
    return vel