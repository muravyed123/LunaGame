import pygame as pg
import sys

import importlib
import math
import globalsc as G
import random

objects = []
buttons = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
bord = (G.WIDTH // 2 - 150, 400, 300, 300, 5)
player = None
max_health = 50
health = None
attack = False
bosses = []
arrows_types = []
arrow = 'materials/arrow2.png'
boss = None
boss_hp = 100
animation = None
ready = True
now_spawn = 'cant'
now_button = '-1'
now_score = 0
now_kick = 0
last = 0
die_boss = False

pg.font.init()
now_played = None
now_scene = 0
timer =  - 1/G.FPS
b_tim = -1/ G.FPS
can_spawn = True

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
        self.active = True
        self.v_x = 1
    def move(self, vel):
        if self.active:
            if abs(vel[0]) + abs(vel[1]) == 2:
                vel = (vel[0] / 2**0.5, vel[1] / 2**0.5)
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
            if self.health <= 0 and self.health != -50:
                self.v = -self.v * 2
                self.c_timer = 0
                self.v_x = random.randint(2,4) * (random.randint(0,1)- 0.5) * 2
                boss.scene.draw_attacks = [boss.scene.draw_attacks[0]]
                self.health = -50
                over(False)
    def die(self):
        #pg.draw.line(screen, G.RED, (self.x - 20, self.y + 10), (self.x + 46, self.y + 5), 5)
        self.rect = pg.Rect(self.x, self.y, self.rect.width, self.rect.height)
        screen.blit(self.image, self.rect)        
        if self.c_timer <= 3:
            pg.draw.line(screen, G.RED, (self.x - 18, self.y + 15), (self.x + 46, self.y + 7), 5)
        elif self.c_timer > 3 and self.c_timer <= 5:
            self.y += self.v
            if self.v <= 0:
                self.v += 0.2
            else:
                self.v += 0.4
            self.x += self.v_x
        elif self.c_timer > 5 and self.c_timer< 6:
            self.c_timer = 7
            from draw import lose
            lose()
        self.c_timer += 1/G.FPS
class Object():
    def __init__(self, fig, color, parameters,x = 0, y = 0):
        self.fig = fig
        self.x = x
        self.y = y
        self.color = color
        self.parameters = parameters
    def draw(self):
        if self.fig == 'rect':
            x, y, w, h, r = tuple(self.parameters)
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
class Boss:
    def __init__(self, number):
        self.scene = importlib.import_module(f'bosses.boss{number}')
        self.me = self.scene.boss
        self.scene.clear()
        self.can_move = True
    def draw(self):
        if self.can_move:
            screen.blit(self.me.draw(), (0,0))
        else:
            screen.blit(self.scene.screen, (0,0))
    def give_attacks(self, player, can_spawn):
        result = self.me.give_attack(player, can_spawn)
        if result == 'end':
            spawn_end()
    def is_collide(self, player):
        return(self.me.is_collide(player))
    def die(self):
        return(self.me.die())
class Animation():
    def __init__(self, obj, speed):
        self.e = random.randint(0,1)
        self.speed = speed
        self.obj = obj
    def animate(self):
        if self.e == 0:
            self.obj.parameters[0] += self.speed/2
            self.obj.parameters[2] -= self.speed
            if self.obj.parameters[2] <= 10:
                return False
        elif self.e == 1:
            self.obj.parameters[1] += self.speed/2
            self.obj.parameters[3] -= self.speed
            if self.obj.parameters[3] <= 10:
                return False
        self.speed += 1/ G.FPS * 5
        return True
class Button():
    def __init__(self, pos, fig, key, color):
        self.x = pos[0]
        self.y = pos[1]
        self.fig = fig
        self.key = key
        self.color = color
        self.width = 100
        self.height = 80
        self.vel = (0,0)
        self.need_move = False
        self.n_x = 0
        self.command = None
        self.can_press = False
    def draw(self, keys):
        if type(keys) == pg.key.ScancodeWrapper and keys[self.key]:
            pg.draw.rect(screen, G.RED, (self.x, self.y, self.width, self.height))
            if self.can_press:
                press(self.key, True)
        else:
            if self.can_press:
                press(self.key, False)            
            pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.fig == 'rec':
            pg.draw.rect(screen, (255,255,255), (self.x + 20, self.y + 10, self.width - 40, self.height - 20), 5)
        elif self.fig == 'cir':
            pg.draw.circle(screen, (255,255,255), (self.x + self.width // 2, self.y + self.height//2), self.height - 45, 5)
        elif self.fig == 'tri':
            pg.draw.polygon(screen, (255,255,255), [[self.x + 20, self.y + 10], [self.x + self.width - 20, self.y + 10], [self.x + self.width//2, self.y + self.height - 10]], 5)
        if self.need_move:
            self.move()
    def move(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
        
        self.vel = (self.vel[0] * 1.05, self.vel[1] * 1.05)
        if abs(self.x - self.n_x) <= abs(self.vel[0]):
            self.end_move()
    def start_move(self, end_pos, time, command):
        self.n_x = end_pos[0]
        self.vel = ((end_pos[0] - self.x)/(time * G.FPS), (end_pos[1] - self.y)/(time * G.FPS) )
        self.need_move = True
        self.command = command
    def end_move(self):
        self.need_move = False       
        self.command(self)

def spawn_end():
    global can_spawn, animation
    can_spawn = False
    animation = Animation(objects[0], 4)
def press(key, pres):
    global b_tim, now_button, now_kick, now_score
    if key == pg.K_UP:
        but = 4
    elif key == pg.K_RIGHT:
        but = 3
    elif key == pg.K_DOWN:
        but = 2
    elif key == pg.K_LEFT:
        but = 1
    if now_button == but and not pres:
        now_button = 0
        but = 0
    #print(but, arrow_types, now_kick)
    if but != now_button and pres:
        now_button = but
        b_tim = 0
        if arrow_types[now_kick] == but:
            now_score += 1
        now_kick += 1
    if now_kick == len(arrow_types):
        damage_boss(now_score)
def draw_arrow():
    global timer
    timer += 1/G.FPS
    count = boss.scene.defns[boss.me.stage]
    num = math.floor(timer * count// 5)
    if num >=count:
        timer = -1/G.FPS
        return False
    else:
        image = pg.image.load(arrow) 
        size = (100, 100)
        image = pg.transform.scale(image, (size[0], size[1]))
        angle = 90 * arrow_types[num]
        image = pg.transform.rotate(image, angle)   
        image.set_alpha(255 * (timer* count - num*5))
        screen.blit(image, (G.WIDTH//2 - size[0]//2, 450))
        return True
def draw_timer():
    global timer
    timer += 1/G.FPS
    time = 4 - timer
    if time <= 0:
        timer = -1/G.FPS
        return False
    else:
        pg.draw.rect(screen, G.RED, (G.WIDTH//2- 200 , G.HEIGHT // 2 - 50, time * 400 // 4, 40))
        return True    
def damage_boss(damage):
    global now_spawn , timer
    now_spawn = 'damage'
    timer = 0
    for i in buttons:
        i.can_press = False  
def show_text():
    global timer, now_spawn, attack
    now_spawn = 'text'
    attack = True
    timer = 0
def draw_damage(count):
    global timer
    timer += 1/G.FPS
    pg.draw.rect(screen, (82, 8, 78), (G.WIDTH//2 - 200, 350, 400 , 40))
    if timer < 0.5:
        pg.draw.rect(screen, G.GREEN, (G.WIDTH//2 - 200, 350,boss_hp * 4 *(100 / boss.scene.hitpoints) , 40))
    elif timer >= 0.5 and timer <= 3:
        if timer >= 2:
            length = (timer - 2) * count * 10
            pg.draw.rect(screen, G.GREEN, (G.WIDTH//2 - 200, 350,(boss_hp - length) * 4*(100 / boss.scene.hitpoints) , 40))
        else:
            pg.draw.rect(screen, G.GREEN, (G.WIDTH//2 - 200, 350, boss_hp * 4 *(100 / boss.scene.hitpoints), 40))
        for i in range(count):
            image = pg.image.load('materials/hit.png') 
            size = (100, 100)
            image = pg.transform.scale(image, (size[0], size[1]))
            screen.blit(image, (G.WIDTH//2 - size[0]//2, 120 + i * 20))
        font = pg.font.SysFont('arial', 70)
        if count <= 0:
            text1 = '???...'
        elif count == 1:
            text1 = 'So weak'
        elif count == 2:
            text1 = 'Normal'
        elif count == 3:
            text1 = 'Good !'
        elif count == 4:
            text1 = 'Nice'
        elif count == 5:
            text1 = 'PERFECT'
        Text = font.render(text1, True, G.RED)
        screen.blit(Text, (G.WIDTH//2 - Text.get_width()// 2, 400))
    elif timer > 3 and timer < 4:
        pg.draw.rect(screen, G.GREEN, (G.WIDTH//2 - 200, 350, (boss_hp - count * 10) * 4* (100 / boss.scene.hitpoints), 40))
    elif timer >= 4:
        return False
    return True
def wrap(text, max_length):
    words = text.split()
    lines = []
    now_line = ""
    for word in words:
        if len(now_line) + len(word) + 1 <= max_length:
            now_line += " " + word
        else:
            lines.append(now_line.strip())
            now_line = word
    if now_line:
        lines.append(now_line.strip())
    return lines
def draw_text(keys):
    global timer
    if True in keys:
        return False
    else:
        text = boss.scene.texts[boss.me.stage]
        if timer * G.FPS < 3 * len(text) + text.count(' '):
            count = int(timer * G.FPS // 3)
            count += text[:count].count(' ')
            text1 = text[:count]
                   
        else:
            if timer > 3*len(text)/G.FPS + 3:
                return False            
            text1 = boss.scene.texts[boss.me.stage]
        y_offset = 0
        text1 = wrap(text1, 40)
        font = pg.font.SysFont('arial', 40)
        for line in text1:
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.x = 450
            text_rect.y = 500 + y_offset
            screen.blit(text, text_rect)
            y_offset += text_rect.height
        timer += 1/G.FPS

        Text = font.render('...', True, (255, 255, 255))
        screen.blit(Text, (1000, 640))
        return True
def battle():
    global timer, now_scene, now_spawn, attack, borders, ready, buttons, now_kick, now_button
    objects[0].parameters = list(bord)   
    timer = 0
    now_scene += 1
    attack = False
    now_spawn = 'cant'
    now_kick = 0
    now_button = None
    ready = False
    b1 = Button((G.WIDTH // 2, 400), 'rec', pg.K_RIGHT, (205, 32, 228))
    b2 = Button((G.WIDTH // 2, 400), 'cir', pg.K_LEFT, (35, 199, 219))
    b3 = Button((G.WIDTH // 2, 400), 'tri', pg.K_UP, (19, 187, 61))
    b4 = Button((G.WIDTH // 2, 400), 'tri', pg.K_DOWN, (228, 235, 18))
    b1.start_move((G.WIDTH - 400, 450), 1.5, ready_to_spawn)
    b2.start_move((300, 550), 1.5, ready_to_spawn)
    b3.start_move((300, 450), 1.5, ready_to_spawn)
    b4.start_move((G.WIDTH - 400, 550), 1.5, ready_to_spawn)
    buttons = [b1, b2, b3, b4]


def update(vel):
    player.move(vel)
    return vel
def give_angle(point1, point2):
    angle = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
    return(angle)
def create_random_coord():
    count_x = bord[0]
    count_y = bord[1]
    while count_x <= bord[0] + 100 + bord[2] and count_x > bord[0] - 100:
        count_x = random.randint(100, G.WIDTH - 100)
    while count_y < bord[1] + 100 + bord[3] and count_y > bord[1] - 100:
        count_y = random.randint(100, G.HEIGHT - 400)
    return(count_x, count_y)
def ready_to_spawn(button):
    global now_spawn,arrow_types, timer
    if button.fig == 'rec':
        arrow_types = [random.randint(1, 4) for x in range(boss.scene.defns[boss.me.stage])]
        now_spawn = 'can'
        timer = 0
def is_ready():
    global timer, ready, can_spawn
    timer += 1/G.FPS
    if timer >= 1:
        ready = True
        can_spawn = True
        timer = - 1/ G.FPS
def over(p):
    global now_spawn, attack, can_spawn, die_boss
    if p:
        if not die_boss:
            from draw import change_scene as change
            change(last, -1)
            die_boss = True
    else:
        attack = True
        now_spawn = 'dead'
        player.active = False
        can_spawn = False
        player.c_timer = 0
def new_perem():
    global boss_hp, attack, now_spawn, can_spawn, ready, timer, objects , buttons, now_score, now_kick, now_button, die_boss
    boss_hp = 100
    attack = False
    now_spawn = 'çant'
    can_spawn = False
    ready = False
    timer = -1 / G.FPS
    objects = []
    buttons = []
    now_button = '-1'
    now_score = 0
    die_boss = False
    now_kick = 0    
def start(number, last_scene):
    global player, health, boss, last, boss_hp, n_start
    n_start = True
    new_perem()
    borders = Object('rect', G.WHITE, list(bord))
    objects.append(borders)
    player = Player(G.WIDTH//2 - 16, 600, number, 100)
    s = Label(G.name, (530 , 720 ), (255, 255, 255), 30, 'showcardgothic')
    s1 = Label('HP', (810 , 720 ), (255, 255, 255), 30, 'showcardgothic')
    s2 = Label('LV ' + str(G.level), (710 , 720 ), (255, 255, 255), 30, 'showcardgothic')
    health = Health((880, 720), 'showcardgothic')
    b1 = Button((G.WIDTH // 2, 400), 'rec', pg.K_RIGHT, (205, 32, 228))
    b2 = Button((G.WIDTH // 2, 400), 'cir', pg.K_LEFT, (35, 199, 219))
    b3 = Button((G.WIDTH // 2, 400), 'tri', pg.K_UP, (19, 187, 61))
    b4 = Button((G.WIDTH // 2, 400), 'tri', pg.K_DOWN, (228, 235, 18))
    buttons.append(b1)
    buttons.append(b2)
    buttons.append(b3)
    buttons.append(b4)
    b1.start_move((G.WIDTH - 400, 450), 1.5, ready_to_spawn)
    b2.start_move((300, 550), 1.5, ready_to_spawn)
    b3.start_move((300, 450), 1.5, ready_to_spawn)
    b4.start_move((G.WIDTH - 400, 550), 1.5, ready_to_spawn)
    objects.append(s)
    objects.append(s1)
    objects.append(s2)
    boss = Boss(number)
    boss_hp = boss.scene.hitpoints
    show_text()
    last = last_scene
def get_scene(keys):
    global attack, now_spawn, now_score, boss_hp, n_start
    screen.fill(G.BLACK)
    if now_spawn!='dead':
        boss.draw()
        if not n_start:
            health.draw()
            for i in objects[1:]:
                i.draw()
    if attack:
        if now_spawn != 'dead':
            boss.draw()
            if not n_start:
                for i in buttons:
                    i.draw(keys)
        if now_spawn == 'can':
            if not draw_arrow():
                now_spawn = 'press'
                #now_score = 0
                now_kick = 0
                for i in buttons:
                    i.can_press = True
        elif now_spawn == 'press':
            if not draw_timer():
                damage_boss(now_score)
        elif now_spawn == 'damage':
            if not draw_damage(now_score):
                boss_hp -= now_score * 10
                now_score = 0
                if boss_hp <= 0:
                    now_spawn = 'die'
                    from draw import change_music as change
                    change('nothing')
                    boss.can_move = False
                    boss.me.timer = 0
                else:
                    show_text()
        elif now_spawn == 'text':
            if not draw_text(keys):
                battle()
                n_start = False
        elif now_spawn == 'die':
            is_over = boss.die()
            if is_over:
                over(True)
        elif now_spawn == 'dead':
            player.die()
                
    else:
        objects[0].draw()
        if not ready or can_spawn:
            player.draw()
        if not ready:
            is_ready()
        if boss.is_collide(player):
            player.hit()
        boss.give_attacks(player, can_spawn)
    if not can_spawn:
        if len(boss.scene.draw_attacks) !=0:
            if now_spawn != 'dead':
                player.draw()
        else:
            if not attack and ready:
                attack = not animation.animate()
    return(screen)
