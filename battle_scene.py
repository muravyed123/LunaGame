import pygame as pg
import sys

import math
import globalsc as G
import random

objects = []
attacks = []
buttons = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
bord = (525, 350, 230, 230, 5)
player = None
max_health = 50
health = None
attack = False
all_at = [( 'materials/arrow.png',(100,100), (70,20))]
bosses = []
arrows_types = []
arrow = 'materials/arrow2.png'
boss = None
boss_hp = 10
animation = None
ready = True
now_spawn = 'cant'
now_button = '-1'
now_score = 0
now_kick = 0
die = None
last = 0

def in_bosses():
    global bosses
    bosses = [[(['materials/tar_1.png', 'materials/tar_2.png', 'materials/tar_3.png'], [(515, 100), (515, 100), (515, 100)], [(250, 250), (250, 250), (250, 250)], [1, 0, 0], die1),
        [(create_random_coord, 0) for x in range(1)
        ] + ['Çucaracha applauds!', 5],  [(create_random_coord, 0) for x in range(5)
        ] + ['Çucaracha applauds faster!', 5],  [(create_random_coord, 0) for x in range(10)
        ] + ['Çucaracha laughs!', 5],  [(create_random_coord, 0) for x in range(20)
        ] + ['Auuufff', 5]
            ]
              ]     
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
    def __init__(self, textures, positions, sizes, can_move):
        self.textures = []
        self.abs_pos = []
        self.can_move = True
        for i in range(len(textures)):
            image = pg.image.load(textures[i]) 
            self.textures.append(pg.transform.scale(image, (sizes[i][0], sizes[i][1])))
            self.abs_pos.append(positions[i])
        self.positions = positions
        self.can_move = can_move
        self.vel = [(0.05,0.1)] * sum(can_move)
        self.n = 0
    def draw(self):
        self.n = 0
        for i in range(len(self.textures)):
            screen.blit(self.textures[i], self.positions[i])
            if self.can_move[i] == 1:
                self.move(i)
    def move(self, i):
        if self.can_move:
            vel = self.vel[self.n]
            if abs(self.positions[i][0] - self.abs_pos[i][0]) >= 3:
                self.vel[self.n]  = ( -vel[0], vel[1])
                vel = (-vel[0], vel[1])
            elif abs(self.positions[i][1] - self.abs_pos[i][1]) >= 3:
                self.vel[self.n] = (vel[0], -vel[1])
                vel = (vel[0], -vel[1])
            self.positions[i] = (self.positions[i][0] + vel[0], self.positions[i][1] + vel[1])
            self.n += 1
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
        if keys[self.key]:
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
    
def spawn():
    global timer
    time_spawn = 10/ (len(now_played[now_scene]))
    new_timer = (timer + 1/G.FPS)
    if math.floor(new_timer)  != math.floor(timer):
        if math.floor(new_timer)  == len(now_played[now_scene]) - 2:
            spawn_end()
            return None
        at1 = now_played[now_scene][math.floor(new_timer)]
        attacks.append(give_Attack(at1[0](), at1[1]))
    timer = new_timer
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
    count = now_played[now_scene][-1]
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
        screen.blit(image, (G.WIDTH//2 - size[0]//2, 350))
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
    global timer, now_spawn
    now_spawn = 'text'
    timer = 0
def draw_damage(count):
    global timer
    timer += 1/G.FPS
    pg.draw.rect(screen, (82, 8, 78), (440, 350, 400 , 40))
    if timer < 0.5:
        pg.draw.rect(screen, G.GREEN, (440, 350,boss_hp * 4 , 40))
    elif timer >= 0.5 and timer <= 3:
        if timer >= 2:
            length = (timer - 2) * count * 10
            pg.draw.rect(screen, G.GREEN, (440, 350,(boss_hp -  length) * 4 , 40))
        else:
            pg.draw.rect(screen, G.GREEN, (440, 350, boss_hp * 4 , 40))
        for i in range(count):
            image = pg.image.load('materials/hit.png') 
            size = (100, 100)
            image = pg.transform.scale(image, (size[0], size[1]))
            screen.blit(image, (G.WIDTH//2 - size[0]//2, 120 + i * 20))
            font = pg.font.SysFont('arial', 70)
            if count == 0:
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
        pg.draw.rect(screen, G.GREEN, (440, 350, (boss_hp - count * 10) * 4 , 40))
    elif timer >= 4:
        return False
    return True 
def draw_text(keys):
    global timer
    if True in keys:
        return False
    else:
        text = now_played[now_scene][-2]
        if timer * G.FPS < 3 * len(text) + text.count(' '):
            count = int(timer * G.FPS // 3)
            count += text[:count].count(' ')
            text1 = text[:count]
                   
        else:
            if timer > 3*len(text)/G.FPS + 3:
                return False            
            text1 = now_played[now_scene][-2]
        timer += 1/G.FPS
        font = pg.font.SysFont('arial', 30)
        Text = font.render(text1, True, (255, 255, 255))     
        screen.blit(Text, (400, 400))    
        Text = font.render('...', True, (255, 255, 255))     
        screen.blit(Text, (900, 540))              
        return True
def battle():
    global timer, now_scene, now_spawn, attack, borders, ready, buttons, now_kick, now_button
    objects[0].parameters = list(bord)   
    timer = 0
    now_scene += 1
    if now_scene == len(now_played):
        over(True)
        return None
    attack = False
    now_spawn = 'cant'
    now_kick = 0
    now_button = None
    ready = False
    b1 = Button((G.WIDTH // 2, 300), 'rec', pg.K_RIGHT, (205, 32, 228))
    b2 = Button((G.WIDTH // 2, 300), 'cir', pg.K_LEFT, (35, 199, 219))
    b3 = Button((G.WIDTH // 2, 300), 'tri', pg.K_UP, (19, 187, 61))
    b4 = Button((G.WIDTH // 2, 300), 'tri', pg.K_DOWN, (228, 235, 18))
    b1.start_move((G.WIDTH - 300, 350), 1.5, ready_to_spawn)
    b2.start_move((200, 450), 1.5, ready_to_spawn)
    b3.start_move((200, 350), 1.5, ready_to_spawn)
    b4.start_move((G.WIDTH - 300, 450), 1.5, ready_to_spawn)   
    buttons = [b1, b2, b3, b4]


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
def ready_to_spawn(button):
    global now_spawn,arrow_types, timer
    if button.fig == 'rec':
        arrow_types = [random.randint(1, 4) for x in range(now_played[now_scene][-1])]
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
    from draw import change_scene as change
    change(last)
def die1():
    size = (200, 200)
    image = pg.image.load('materials/tapok.png') 
    image = pg.transform.scale(image, (size[0], size[1]))
    if timer > 5 and timer <6:
        screen.blit(image, (G.WIDTH - size[0] - (timer - 5) * (G.WIDTH//2 - size[0]//2) , 120 ))
        image = pg.transform.rotate(image, (timer - 5) * 90)
    elif timer >= 6 and timer < 9:
        screen.blit(image, (G.WIDTH//2 - size[0]//2, 120))
    elif timer >= 9:
        over(True)
def new_perem():
    global boss_hp, attack, now_spawn, spawn, ready, timer, objects, attacks, buttons, now_score, now_kick, now_button
    boss_hp = 100
    attack = False
    now_spawn = 'çant'
    can_spawn = False
    ready = False
    timer = -1 / G.FPS
    objects = []
    attacks = []
    buttons = []
    now_button = '-1'
    now_score = 0
    now_kick = 0    
def start(number, last_scene):
    global player, health, now_played, now_scene, boss, last, die
    new_perem()
    borders = Object('rect', G.WHITE, list(bord))
    objects.append(borders)
    player = Player(640, 400, number, 100)
    s = Label(G.name, (390 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    s1 = Label('HP', (610 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    s2 = Label('LV ' + str(G.level), (510 , 600 ), (255, 255, 255), 30, 'showcardgothic')
    health = Health((680, 600), 'showcardgothic')
    b1 = Button((G.WIDTH // 2, 300), 'rec', pg.K_RIGHT, (205, 32, 228))
    b2 = Button((G.WIDTH // 2, 300), 'cir', pg.K_LEFT, (35, 199, 219))
    b3 = Button((G.WIDTH // 2, 300), 'tri', pg.K_UP, (19, 187, 61))
    b4 = Button((G.WIDTH // 2, 300), 'tri', pg.K_DOWN, (228, 235, 18))
    buttons.append(b1)
    buttons.append(b2)
    buttons.append(b3)
    buttons.append(b4)
    b1.start_move((G.WIDTH - 300, 350), 1.5, ready_to_spawn)
    b2.start_move((200, 450), 1.5, ready_to_spawn)
    b3.start_move((200, 350), 1.5, ready_to_spawn)
    b4.start_move((G.WIDTH - 300, 450), 1.5, ready_to_spawn)
    objects.append(s)
    objects.append(s1)
    objects.append(s2)
    in_bosses()
    text, pos, siz, c_m, die_f = bosses[number-1][0]
    die = die_f
    boss = Boss(text, pos, siz, c_m)
    now_played = bosses[number-1]
    now_scene = 1   
    last = last_scene
def get_scene(keys):
    global attack, now_spawn, now_score, boss_hp
    screen.fill(G.BLACK)
    boss.draw()
    for i in objects[1:]:
        i.draw()
    if attack:
        boss.draw()
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
                    boss.can_move = [0] * len(boss.can_move)
                else:
                    show_text()
        elif now_spawn == 'text':
            if not draw_text(keys):
                battle()
        elif now_spawn == 'die':
            draw_damage(now_score)
            die()
        
                
    else:
        objects[0].draw()
        if not ready or can_spawn:
            player.draw()
        if not ready:
            is_ready()
    for i in attacks:
        i.draw()
        if i.is_collide(player.rect):
            player.hit()
        i.move()
    health.draw()
    if can_spawn:
        spawn()
    else:
        if len(attacks) !=0:
            player.draw()
        else:
            if not attack and ready:
                attack = not animation.animate()
    return(screen)
