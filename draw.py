import pygame as pg
import importlib
import globalsc as G

import Scene_class as Sc

import battle_scene as Bscene
screen = pg.Surface((1280, 720), G.WHITE) 
now_scene = None

last_scene = None
in_battle = False


class Camera:
    def __init__(self, active):
        self.y = 0
        self.x = G.WIDTH//2
        self.width = G.WIDTH
        self.v =  -1
        self.active = active
    def move(self, player):
        r = self.x - player.x
        if abs(r) > 200:
            self.x += self.v * r// abs(r) * 0.12 * (abs(r)) ** 0.5
class Player:
    def __init__(self, screen, x, y, v_y = 0, animations = {}, animated = True):
        self.x = x
        self.floor = 450
        self.y = y
        self.v = 5
        self.v_y = v_y
        self.rect = pg.Rect(self.x , self.y, 70, 70)
        self.jump = -16
        self.gravity = 0.5
        self.screen = screen
        self.is_on_floor = False
        self.animation = 'walk'
        self.animations = animations
        self.timer = 0
        self.animated = animated
        self.add_x = 0
        self.flip_h = True
    def move(self, vector):
        self.move_x(vector[0])
        self.move_y(vector[1])
        new_animation = 'nothing'
        if self.animated:
            if vector[1] == 1 or not self.is_on_floor:
                new_animation = 'jump'
            else:
                if vector[0] == 0:
                    new_animation = 'stay'
                else:
                    new_animation = 'walk'
            if new_animation == self.animation:
                self.timer += 1 / self.animations[new_animation][1]
            else:
                self.animation = new_animation
                self.timer = 0
            #print(new_animation)
            if vector[0]>0:
                self.flip_h = False
                self.add_x = 0
            elif vector[0] < 0:
                self.flip_h = True
                self.add_x = 20
        self.rect = pg.Rect(self.x, self.y, self.rect.width, self.rect.height)
        return(self.rect)
    def move_x(self, vel):
        self.x += self.v * vel
        return pg.Rect(self.x, self.y, self.rect.width, self.rect.height)
    def move_y(self, vel):
        new_y = self.y      
        if vel == 1 and self.is_on_floor:
            self.v_y = self.jump  
            self.timer = 0
        new_y += self.v_y
        self.v_y += self.gravity          
        if self.is_on_floor and abs(self.v_y) > 1:
            self.is_on_floor = False            
        if new_y >= self.floor - self.rect.height:
            new_y = self.floor - self.rect.height
            if vel != 1:
                self.v_y = 0
            self.is_on_floor = True
        self.y = new_y
        #if self.animated: print(self.v_y, self.is_on_floor, vel) 
        return pg.Rect(self.x, self.y, self.rect.width, self.rect.height)
    def push(self, y):
        self.y = y
        if self.v_y > 0:
            self.is_on_floor = True
        self.v_y = 0    
    def draw(self):
        images = self.animations[self.animation][0]
        #print(images)
        timer = int(self.timer//1)    
        if timer < len(images):
            #print(timer)
            image = pg.image.load(images[timer]) 
        else: 
            if self.animation != 'jump': 
                self.timer = 0 
                image = pg.image.load(images[0]) 
            else:          
                image = pg.image.load(images[-1])
        image = pg.transform.scale(
                image, (self.rect.width * 1.32, self.rect.height *1.32))   
        image = pg.transform.flip(image, self.flip_h, False)
        #pg.draw.rect(screen, G.BLACK, (self.rect.x - camera.x + camera.width // 2, self.y, self.rect.width, self.rect.height))
        screen.blit(image, (self.x - camera.x +camera.width//2 - self.add_x, self.y))  
        #pg.draw.circle(screen, G.BLACK, (self.x - camera.x +camera.width//2, self.y), 5)
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
        pl =  Player(screen, player.x, player.y, player.v_y, {}, False)
        return self.me.update(player, pl, vel)
class BattleScene:
    def __init__(self, number):
        self.number = number
        self.me = Bscene
        self.me.start(number)
        
    def draw(self, vel, keys):
        surface = self.me.get_scene(keys)
        self.me.update(vel)
        screen.blit(surface, (0, 0))
        return (0, 0)   

def change_scene(number):
    global now_scene
    now_scene = Scene(number + 1, player, camera)

def go_in_battle(number):
    global now_scene, last_scene, in_battle
    last_scene = now_scene
    now_scene = BattleScene(number)
    in_battle = True
camera = Camera(True)
animations = {'walk' : [Sc.give_list_an('Animations/wh_cat_walk'), 5], 
                     'jump' : [Sc.give_list_an('Animations/wh_cat_jump'), 8], 
                     'stay' : [Sc.give_list_an('Animations/wh_cat_stay'), 10] }
player = Player(screen, 100, 200, 0, animations)
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
        if in_battle:
            vel[1] = -1
    vel = now_scene.draw(vel, keys)
    if not in_battle:
        player.draw()
        player.move(vel)
        camera.move(player)

    return(screen)