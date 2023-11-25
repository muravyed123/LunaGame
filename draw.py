import pygame as pg
import importlib
import globalsc as G

screen = pg.Surface((1280, 720), G.WHITE) 
now_scene = None
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
    def __init__(self, screen, x, y, v_y = 0):
        self.x = x
        self.floor = 450
        self.y = y
        self.v = 5
        self.v_y = v_y
        self.rect = pg.Rect(self.x , self.y, 40, 20)
        self.jump = -16
        self.gravity = 0.5
        self.screen = screen
        self.is_on_floor = False
    def move(self, vector):
        self.move_x(vector[0])
        self.move_y(vector[1])
        self.rect = pg.Rect(self.x, self.y, 40, 20)
        return(self.rect)
    def move_x(self, vel):
        self.x += self.v * vel
        return pg.Rect(self.x, self.y, 40, 20)
    def move_y(self, vel):
        new_y = self.y

        new_y += self.v_y
        self.v_y += self.gravity
        if vel == 1 and self.is_on_floor:
            self.v_y = self.jump
            self.is_on_floor = False
                
        if new_y >= self.floor - 20:
            new_y = self.floor - 20
            self.is_on_floor = True
        self.y = new_y
        return pg.Rect(self.x, self.y, 40, 20)
    def push(self, y):
        self.y = y
        if self.v_y > 0:
            self.is_on_floor = True
        self.v_y = 0    
    def draw(self):
        pg.draw.rect(screen, G.GREEN, (self.x - camera.x +camera.width//2 , self.y, 40, 20))
        pg.draw.circle(screen, G.BLACK, (self.x - camera.x +camera.width//2, self.y), 5)
        pg.draw.rect(screen, G.BLACK, (0, self.floor, 1280, 20), 2)
        
class Scene:
    def __init__(self, number, player, camera):
        self.number = number
        self.player = player
        self.camera = camera
        self.me = importlib.import_module(f'scenes.scene{number}')
        self.me.start()
        
    def draw(self, vel, keys):
        surface = self.me.get_scene(keys)
        #pl.move(vel)
        screen.blit(surface, (-self.camera.x + camera.width//2, self.camera.y))
        return self.me.update(player, Player(screen, player.x, player.y, player.v_y), vel)

def change_scene(number):
    global now_scene
    now_scene = Scene(number + 1, player, camera)
        
camera = Camera(True)
player = Player(screen, 100, 200)
change_scene(0)
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
    vel = now_scene.draw(vel, keys)
    player.draw()
    player.move(vel)
    camera.move(player)

    return(screen)