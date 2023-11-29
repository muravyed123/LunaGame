import pygame as pg
import sys

import math
import globalsc as G
import random

objects = []
attacks = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
bord = (490, 350, 230, 230, 5)
player = None
max_health = 100
health = None
all_at = [( 'materials/arrow.png',(100,100), (70,20))]
bosses = []
def in_bosses():
    global bosses
    bosses = [[[(create_random_coord, 0) for x in range(20)
        ],
            ]
              ]     
pg.font.init()
now_played = None
now_scene = 0
timer = 0
spawn = True

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
        self.ltime = 0.5
        self.c_timer = self.ltime
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
        if self.c_timer + 1/ G.FPS < self.ltime:
            self.c_timer += 1/G.FPS
        else:
            self.c_timer = self.ltime
    def draw(self):
        #pg.draw.rect(screen, G.GREEN, self.rect)
        screen.blit(self.image, self.rect)
    def hit(self):
        if self.c_timer == self.ltime:
            self.health -= 10
            self.c_timer = 0
            health.hit(0.5)
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
        self.color = (255,255,255)
        self.timer = 0
    def draw(self):
        if self.timer <-1:
            self.timer += 1/ G.FPS
        elif self.timer <0:
            self.timer = 0
            self.color = (255,255,255)
        pg.draw.rect(screen, G.RED, (self.x, self.y + 2, self.width, self.height))
        hl = player.health
        if hl >= 0:
            length = self.width * hl // max_health
            pg.draw.rect(screen, G.GREEN, (self.x, self.y + 2, length, self.height))
            text = self.font.render(str(int(hl//1)) + ' / ' + str(max_health), True, self.color)     
            screen.blit(text, (self.x + 100, self.y))
    def hit(self, time):
        self.color = G.RED
        self.timer = -1 - time
            
        
class Attack():
    def __init__(self, pos, angle, speed, texture, size, rect_size):
        self.x = pos[0]
        self.y = pos[1]
        self.angle = angle
        self.speed = speed
        self.image = pg.image.load(texture)
        self.size = size
        self.image = pg.transform.scale(
            self.image, (size[0], size[1]))  
        self.rect = pg.Rect(self.x, self.y, rect_size[0], rect_size[1])
        self.rect.center = (self.x + rect_size[0]//2, self.y + rect_size[1]//2)
        self.fi = math.atan2(rect_size[0], rect_size[1])
        self.l = (self.rect.width ** 2//4 + self.rect.height ** 2//4) ** 0.5
    def move(self):
        
        self.y += math.sin(self.angle) * self.speed
        self.x += math.cos(self.angle) * self.speed
        if self.x < 0 or self.y <0 or self.x >G.WIDTH or self.y > G.HEIGHT:
            del attacks[attacks.index(self)] 
    def draw(self):
        image_r = pg.transform.scale(self.image, (self.size[0] ,self.size[1]))             
        rect = image_r.get_rect()
        
        new_r = pg.transform.rotate(image_r , -self.angle *180/3.14 - 90)  
        rect = new_r.get_rect() 
        rect.center = (self.x, self.y)  
        screen.blit(new_r , rect) 
        #pg.draw.rect(screen, G.GREEN, self.rect)
    def is_collide(self, rect):
        cent = (self.x , self.y )
        d_x = math.sin(-self.angle + self.fi ) * self.l
        d_y = math.cos(-self.angle + self.fi ) * self.l
        d_sx = math.sin(-self.angle - self.fi ) * self.l
        d_sy = math.cos(-self.angle - self.fi ) * self.l
        #print(d_x, d_y, self.angle)
        points = [(cent[0] + d_x, cent[1] + d_y), (cent[0] - d_x, cent[1] - d_y), (cent[0] + d_sx, cent[1] + d_sy), (cent[0] - d_sx, cent[1] - d_sy)]
        t = False
        for i in points:
            if rect.collidepoint(i):
                t = True
                break
            #pg.draw.circle(screen, G.BLUE, i, 5)
        return(t)
        

def start(number):
    global player, health, now_played
    borders = Object('rect', G.WHITE, bord)
    objects.append(borders)
    player = Player(640, 400, number, 100)
    s = Label(G.name, (390 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    s1 = Label('HP', (610 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    s2 = Label('LV ' + str(G.level), (510 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    health = Health((680, 600), 'showcardgothic')
    objects.append(s)
    objects.append(s1)
    objects.append(s2)
    objects.append(health)
    in_bosses()
    now_played = bosses[number-1]
def spawn():
    global timer
    time_spawn = 10/ len(now_played[now_scene])
    new_timer = (timer + 1/G.FPS)
    if math.floor(new_timer)  != math.floor(timer):
        if math.floor(new_timer) == len(now_played[now_scene]):
            spawn_end()
            return None
        at1 = now_played[now_scene][math.floor(new_timer)]
        attacks.append(give_Attack(at1[0](), at1[1]))
    timer = new_timer
def spawn_end():
    global spawn
    spawn = False
def get_scene(keys):
    screen.fill(G.BLACK)
    for i in objects:
        i.draw()
    for i in attacks:
        i.draw()
        if i.is_collide(player.rect):
            player.hit()
        i.move()
    player.draw()
    if spawn:
        spawn()
    return(screen)
def update(vel):
    player.move(vel)
    return vel
def give_angle(point1, point2):
    angle = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
    return(angle)
def give_Attack(pos, number):
    tex, siz, rs = all_at[number]
    return Attack(pos, give_angle(pos, (player.x + player.rect.width//2, player.y + player.rect.height//2)), 6, tex, siz, rs)
def create_random_coord():
    count_x = bord[0]
    count_y = bord[1]
    while count_x <= bord[0] + 20 and count_x > bord[2] - 20:
        count_x = random.randint(100, G.WIDTH - 100)
    while count_y < bord[1] + 20 and count_y > bord[3] - 20:
        count_y = random.randint(100, G.HEIGHT - 400)
    return(count_x, count_y)
        