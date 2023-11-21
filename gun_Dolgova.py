import math
from random import choice
import numpy as np
import sys

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
PINK = (255, 20, 147)
CORAL = (255, 127, 80)
ORANGE = (255, 69, 0)
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
x1 = 100
y1 = 500
x2 = 700
y2 = 500
xb = 100
yb = 100




class Ball:
    def __init__(self, screen: pygame.Surface, obj):
        self.screen = screen
        self.x = obj.x
        self.y = obj.y
        self.r = 10
        self.vx = 10
        self.vy = 10
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x >= 800:
            self.vx = - self.vx
            self.x = 1600 - self.x
        if self.x <= 0:
            self.vx = - self.vx
            self.x = - self.x
        if self.y >= 600:
            self.vy = - self.vy
            self.y = 1200 - self.y
        if self.y <= 0:
            self.vy = - self.vy
            self.y = - self.y   
        self.vy -= 1

    def draw(self):
        surf = pygame.image.load('камень.png').convert()
        surf = pygame.transform.scale(surf, (50, 50))
        surf.set_colorkey((0, 0, 0))
        rect = surf.get_rect(center=(self.x, self.y))
        self.screen.blit(surf, rect)
        
    def hittest(self, obj):        
        return ((obj.x - self.x)**2 + (obj.y - self.y)**2)**0.5 <= obj.r + self.r
        
class Ball_2(Ball):
        
    def draw(self):        
        surf = pygame.image.load('золото.png').convert()
        surf = pygame.transform.scale(surf, (50, 50))
        surf.set_colorkey((0, 0, 0))
        rect = surf.get_rect(center=(self.x, self.y))
        self.screen.blit(surf, rect)

class Gun:
    def __init__(self, screen, x = x1, y = y1):
        self.screen = screen 
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.y = y
        self.vx = 1
        self.r = 50
        self.live = 1
        self.points = 0
        self.new_gun()
        
    def new_gun(self):
        x = self.x = x1
        y = self.y = y1

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):        
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):        
        if event:
            self.an = math.degrees(math.atan((event.pos[1]-self.y-0.00001) / (event.pos[0]-self.x-0.00001)))
    
    def hit(self, points=1):            
            self.points += points

    def draw(self):        
        surf1 = pygame.image.load('танк 2.png').convert()
        surf1 = pygame.transform.scale(surf1, (200, 100))
        surf1.set_colorkey((0, 0, 0))
        surf2 = pygame.image.load('дуло 2.png').convert()
        surf1 = pygame.transform.flip(surf1, True, False)
        surf2 = pygame.transform.scale(surf2, (200, 30))
        surf2.set_colorkey((0, 0, 0)) 
        rect = surf2.get_rect(center=(0, 0))
        rot = pygame.transform.rotate(surf2, -self.an)
        rot_rect = rot.get_rect(center=(self.x + 40, self.y - 30))
        rect_ = surf1.get_rect(center=(self.x, self.y))
        self.screen.blit(rot, rot_rect)
        self.screen.blit(surf1, rect_)
        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            
    def move(self):
        self.x += self.vx
        if self.x >= 700:
            self.vx = - self.vx
            self.x = 1400 - self.x
        if self.x <= 100:
            self.vx = - self.vx
            self.x = 200 - self.x  
        
class Gun_2:
    def __init__(self, screen, x = x2, y = y2):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.y = y
        self.vx = 1
        self.r = 50
        self.points = 0
        self.live = 1
        self.new_gun()        
    
    def new_gun(self):
        x = self.x = x2
        y = self.y = y2

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):        
        global balls, bullet
        bullet += 1
        new_ball = Ball_2(self.screen, self)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):        
        if event:
            self.an =math.degrees(math.atan((event.pos[1]-self.y-0.00001) / (event.pos[0]-self.x-0.00001)))
            
    def hit(self, points=1):            
            self.points += points

    def draw(self):        
        surf1 = pygame.image.load('танк.png').convert()
        surf1 = pygame.transform.scale(surf1, (200, 100))
        surf1.set_colorkey((0, 0, 0))
        surf2 = pygame.image.load('дуло.png').convert()
        surf2 = pygame.transform.flip(surf2, True, False)
        surf2 = pygame.transform.scale(surf2, (250, 60))
        surf2.set_colorkey((0, 0, 0)) 
        rect = surf2.get_rect(center=(0, 0))
        rot = pygame.transform.rotate(surf2, - self.an - 180)
        rot_rect = rot.get_rect(center=(self.x - 40, self.y - 30))
        rect_ = surf1.get_rect(center=(self.x, self.y))
        self.screen.blit(rot, rot_rect)
        self.screen.blit(surf1, rect_)
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
            
    def move(self):
        global x2
        self.x += self.vx
        if self.x >= 700:
            self.vx = - self.vx
            self.x = 1400 - self.x
        if self.x <= 100:
            self.vx = - self.vx
            self.x = 200 - self.x
    
class Target:    
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()
        self.x = choice(range(600, 780))
        self.y = choice(range(300, 550))
        self.r = choice(range(30, 50))
        self.vx = 1
        self.vy = 1

    def new_target(self):
        x = self.x = choice(range(600, 780))
        y = self.y = choice(range(300, 550))
        r = self.r = choice(range(30, 50))
        color = self.color = RED

    def hit(self, points=1):
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)
        
    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x >= 800:
            self.vx = - self.vx
            self.x = 1600 - self.x 
        if self.x <= 0:
            self.vx = - self.vx
            self.x = - self.x
        if self.y >= 600:
            self.vy = - self.vy
            self.y = 1200 - self.y
        if self.y <= 0:
            self.vy = - self.vy
            self.y = - self.y
            
class Target_2(Target):    
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()
        self.x = choice(range(300, 500))
        self.y = choice(range(300, 500))
        self.r = choice(range(20, 30))
        self.vx = -1
        self.vy = 2

    def new_target(self):
        x = self.x = choice(range(600, 700))
        y = self.y = choice(range(300, 500))
        r = self.r = choice(range(20, 30))
        color = self.color = CORAL
        
class Bomb(Ball):    
    def __init__(self, screen, x = xb, y = yb):
        self.screen = screen
        self.points = 0
        self.live = 30
        self.x = x
        self.y = y
        self.vx = 1
        self.vy = 1
        self.r = 50
        self.time = 0

    def draw(self):        
        surf = pygame.image.load('бомба.png').convert()
        surf = pygame.transform.scale(surf, (100, 100))
        surf.set_colorkey((0, 0, 0))
        rect = surf.get_rect(center=(xb, yb))
        self.screen.blit(surf, rect)

pygame.init()
pygame.mixer.music.load('скибиди.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

font = pygame.font.Font('Raindrop.otf', 36)
counter = 0
score1 = 0
score2 = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load('фон.png').convert()
bg = pygame.transform.scale(bg, (800, 600))

pygame.display.set_caption("Ворлд оф тэнкс")
bullet = 0
balls = []

step = 0

clock = pygame.time.Clock()
gun = Gun(screen)
gun_2 = Gun_2(screen)
target = Target(screen)
target_2 = Target_2(screen)
bomb = Bomb(screen)
finished = False

attack = pygame.USEREVENT + 0
pygame.time.set_timer(attack, 1000)


while not finished:
    screen.blit(bg, (0, 0))
    
    counter_text = font.render(f"Your score: {counter}", True, (240, 240, 240))
    screen.blit(counter_text, (10, 10))
    
    score1_text = font.render(f"{score1} : {score2}", True, (240, 240, 240))
    screen.blit(score1_text, (400, 50))
    
    gun.draw()
    gun_2.draw()
    target.draw()
    target_2.draw()
    bomb.draw()
    
    for b in balls:
        b.draw()    
    pygame.display.update()
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if step % 2 == 0:
                gun.fire2_start(event)
            else:
                gun_2.fire2_start(event)
            step += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if step % 2 == 0:
                gun.fire2_end(event)
            else:
                gun_2.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            if step % 2 == 0:
                gun.targetting(event)
            else:
                gun_2.targetting(event)        
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                yb += 50
                if ((xb - x1)**2 + (yb - y1)**2)**0.5 <= 75:
                    yb = 50
                    score1 -= 1
        elif event.type == attack:
            screen.blit(font.render(f"Skibidi dop dop yes yes", True, (240, 240, 240)), (280, 150))            
        pygame.display.update()
        
    target.move()
    target_2.move() 
    bomb.move()
    gun.move()  
    gun_2.move() 
      
    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.hit()
            counter += 1
            balls.remove(b)
            target.new_target()
        elif b.hittest(target_2) and target_2.live: 
            target_2.hit()
            counter += 1
            balls.remove(b)
            target_2.new_target()
        if step % 2 == 0:
             if b.hittest(gun_2) and gun_2.live:
                 gun_2.hit()
                 score1 += 1
                 balls.remove(b)
                 gun_2.new_gun()
        else:
            if b.hittest(gun) and gun.live:
                gun.hit()
                score2 += 1
                balls.remove(b)
                gun.new_gun()  
        
    gun.power_up()
    gun_2.power_up()

pygame.quit()
