import pygame as pg

import globalsc as G
screen = pg.Surface((1280, 720), G.WHITE) 
class Camera:
    def __init__(self, active):
        self.y = 0
        self.x = G.WIDTH//2
        self.width = G.WIDTH
        self.v =  -2
        self.active = active
    def move(self, player):
        r = self.x - player.x
        if abs(r) > 200:
            self.x += self.v * r// abs(r) * 0.12 * (abs(r)) ** 0.5
class Player:
    def __init__(self, screen, x, y):
        self.x = x
        self.floor = 600
        self.y = y
        self.v = 5
        self.v_y = 0
        self.jump = -20
        self.gravity = 1
        self.screen = screen
    def move(self, vector):
        self.x += self.v * vector[0]
        new_y = self.y + self.v_y 
        if new_y >= self.floor:
            self.y = self.floor
            self.v_y = 0
        else:
            self.y = new_y
            self.v_y += self.gravity
        if vector[1] == 1 and self.y == self.floor:
            self.v_y = self.jump
    def draw(self):
        pg.draw.rect(screen, G.BLACK, (self.x - camera.x +camera.width//2 - 20, self.y , 40, 20))
        pg.draw.rect(screen, G.BLACK, (G.WIDTH//2 - 200, self.y - 150, 400, 600), 5)
        pg.draw.rect(screen, G.BLACK, (700 - camera.x + camera.width//2, 0 , 80, 200))
camera = Camera(True)
player = Player(screen, 100, 200)
def update(event, keys):
    screen.fill(G.WHITE)
    vel = [0,0]
    if keys[pg.K_LEFT]:
        vel[0] = -1
    if keys[pg.K_RIGHT]:
        vel[0] = 1   
    if keys[pg.K_UP]:
        vel[1] = 1
    if keys[pg.K_DOWN]:
        vel[1] = 0 
    player.draw()
    player.move(vel)
    camera.move(player)

    return(screen)