import pygame as pg
import math
import sys

import Scene_class

sys.path.append('..')
import globalsc as G
import random
hitpoints = 240
textures = ['materials/book.png', 'materials/bookeyebrows.png', 'materials/bookeyes.png']
sizes = [(280, 280), (280, 280), (280, 280)]
coords = [(660, 30), (660, 30), (660, 30)]
can_move = [0, 0, 1]
music = 4
texts = ['Неожиданно из двери выпала непонятная книга. О НЕТ    ЭТО ЖЕ     УЧЕБНИК МАТАНА',"Как же ты читаешь мои атаки..А! я же книга,точно", "Не думай, что я бьюсь без причины, у меня есть великая цель.", "Когда-то давно меня поставили охранять этот этаж от неучей вроде тебя и я исполню свой долг!", "Ха, я просто не дам тебе пройти дальше не сказав код от шкафчика делов-то.", 'А ты неплох...']
defns = [2, 3, 5, 5, 5, 5, 5]
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
boss_attacks = []
draw_attacks = []
boss = None


def init_attack():
    global boss_attacks, boss
    boss = Boss()
    boss_attacks = [[{'attack': Plane, 'count': 4, 'time': 2},
                     {'attack': Scissors,'count': 2, 'time': 2}],
                    [{'attack': Plane, 'count': 5, 'time': 5},
                     {'attack': Scissors, 'count': 2, 'time': 2},
                     {'attack': Scissors, 'count': 2, 'time': -1},
                     {'attack': Scissors, 'count': 1, 'time': 2},
                     {'attack': Plane, 'count': 4, 'time': 3}],
                    [{'attack': Plane, 'count': 2, 'time': 5},
                     {'attack': Plane, 'count': 3, 'time': -1},
                     {'attack': Scissors, 'count': 3, 'time': 2},
                     {'attack': Plane, 'count': 5, 'time': 2}],
                    [{'attack': Plane, 'count': 2, 'time': 5},
                     {'attack': Many_scissors, 'count': 1, 'time': 4},
                     {'attack': Plane, 'count': 5, 'time': 5}],
                    [{'attack': Plane, 'count': 2, 'time': 6},
                     {'attack': Scissors, 'count': 1, 'time': 2},
                     {'attack': Scissors, 'count': 3, 'time': 4},
                     {'attack': Plane, 'count': 5, 'time': 8},
                     {'attack': Scissors, 'count': 2, 'time': 4}],
                    [{'attack': Plane, 'count': 2, 'time': 5},
                     {'attack': Many_scissors, 'count': 1, 'time': 4},
                     {'attack': Plane, 'count': 5, 'time': 5},
                     {'attack': Scissors, 'count': 2, 'time': 4},
                     {'attack': Plane, 'count': 5, 'time': 3},
                     ]

                    ]
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
class Boss():
    def __init__(self):
        self.textures = []
        self.abs_pos = []
        for i in range(len(textures)):
            image = pg.image.load(textures[i])
            self.textures.append(pg.transform.scale(image, (sizes[i][0], sizes[i][1])))
            self.abs_pos.append(coords[i])
        self.positions = coords
        self.can_move = can_move
        self.vel = [(0.05, 0.1)] * sum(can_move)
        self.n = 0
        self.timer = 0
        self.vy = 1
        self.ay = 0.2
        self.moveh = 1
        self.stage = 0
    def draw(self):
        self.n = 0
        screen.fill(G.WHITE)
        if self.stage == 1:
            self.positions[1] = (self.positions[1][0], self.abs_pos[1][1] + self.vy)
            if abs(self.vy) > 5:
                self.ay *= -1
            self.vy += self.ay
        for i in range(len(self.textures)):
            screen.blit(self.textures[i], self.positions[i])
            if self.can_move[i] == 1 and self.stage!= 1:
                self.move(i)
        for i in draw_attacks:
            i.draw()
        return(screen)
    def is_collide(self, player):
        t = False
        for i in draw_attacks:
            i.move()
            t = t or i.is_collide(player.rect)
        return(t)
    def move(self, i):

        vel = self.vel[self.n]
        if abs(self.positions[i][0] - self.abs_pos[i][0]) >= 3:
            self.vel[self.n] = ( -vel[0], vel[1])
            vel = (-vel[0]*i  , vel[1] * i)
        elif abs(self.positions[i][1] - self.abs_pos[i][1]) >= 3:
            self.vel[self.n] = (vel[0], -vel[1])
            vel = (vel[0] * i, -vel[1] * i)
        self.positions[i] = (self.positions[i][0] + vel[0], self.positions[i][1] + vel[1])
        self.n += 1
    def give_attack(self, player , can_spawn):
        all_time = 0
        now_b = -1
        for i in boss_attacks[self.stage]:
            if i['time'] != -1:
                all_time += i['time']
            if all_time >= self.timer and now_b == -1:
                now_b = boss_attacks[self.stage].index(i)
        if self.timer >= all_time:
            self.stage += 1
            if self.stage == len(boss_attacks):
                self.stage -= 2
            self.timer = 0
            return('end')
        else:
            if can_spawn:
                new_timer = self.timer + 1/G.FPS
                attack = boss_attacks[self.stage][now_b]
                time_spawn = attack['time']
                if time_spawn == -1:
                    for i in range(attack['count']):
                        draw_attacks.append(attack['attack'](player))
                else:
                    delta_time = time_spawn / attack['count']
                    if math.floor(self.timer/ delta_time) != math.floor(new_timer/ delta_time):
                        draw_attacks.append(attack['attack'](player))
                self.timer = new_timer
                return('continue')
    def die(self):
        screen.fill(G.WHITE)
        image = pg.image.load('materials/booksad.png')
        self.textures[0] = pg.transform.scale(image, (sizes[0][0], sizes[0][1]))
        for i in range(len(self.textures)):
            screen.blit(self.textures[i], self.positions[i])
        size = (200, 50)
        text = ''
        if self.timer > 2 and self.timer < 6:
            text = 'НЕЕЕЕЕЕЕЕЕТ МОИ ДРАГОЦЕННЫЕ СТРАНИЦЫ НЕЕЕЕЕТ'
            surf1 = pg.Surface((120,200), G.WHITE)
            surf1.fill((255,255,255))
            surf2 = pg.Surface((120,200), G.WHITE)
            surf2.fill((255, 255, 255))
            screen.blit(surf1, (G.WIDTH // 2 + ((self.timer - 2) * 400) % (G.WIDTH // 2) - 50, 100))
            screen.blit(surf2, (G.WIDTH // 2 - ((self.timer - 2) * 400) % (G.WIDTH // 2) - 50, 100))
        elif self.timer >= 6 and self.timer < 12:
            surf1 = pg.Surface((120, 200), G.WHITE)
            surf1.fill((255, 255, 255))
            surf2 = pg.Surface((120, 200), G.WHITE)
            surf2.fill((255, 255, 255))
            screen.blit(surf1, (G.WIDTH // 2 + ((self.timer - 2) * 400) % (G.WIDTH // 2) - 50, 100))
            screen.blit(surf2, (G.WIDTH // 2 - ((self.timer - 2) * 400) % (G.WIDTH // 2) - 50, 100))
            text = 'Я ТЕБЕ НИ ЗА ЧТО НЕ СКАЖУ КООД НЕЕЕЕТ'
        elif self.timer >= 12 and self.timer < 18:
            text = 'ЧТООО СТРАНИИЦА С КОДОМ ?? ЭТО НЕЧЕСТНО!!'
            surf1 = pg.Surface((120, 200), G.WHITE)
            surf1.fill((255, 255, 255))
            screen.blit(surf1, (G.WIDTH // 2  - 50, 140 + ((self.timer - 12) * 50)))
        elif self.timer >= 18 and self.timer < 23:
            text = 'Код получен : это число  ' + str(G.password)
        elif self.timer >= 23 and self.timer < 27:
            text = 'Я ЕЩЕ ПОКВИТАЮСЬ С ТОБОЙ, ВОРИШКА!'
        elif self.timer >= 27:
            from draw import remove_checkpoints as ch
            ch(5)
            return (True)
        y_offset = 0
        text = wrap(text, 40)
        font = pg.font.SysFont('arial', 40)
        for line in text:
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.x = 450
            text_rect.y = 500 + y_offset
            screen.blit(text, text_rect)
            y_offset += text_rect.height
        self.timer += 1/ G.FPS

        return(False)
def clear():
    global hitpoints, draw_attacks
    hitpoints = 200
    draw_attacks = []
class Attack():
    def __init__(self, pos, angle, speed, texture, size, rect_size, nr, start_t, fire):
        self.x = pos[0]
        self.start_t = start_t
        self.y = pos[1]
        self.fire = fire
        self.angle = angle
        self.speed = speed
        self.image = pg.image.load(texture)
        self.size = size
        self.image = pg.transform.scale(
            self.image, (size[0], size[1]))
        self.rect = pg.Rect(self.x, self.y, rect_size[0], rect_size[1])
        self.rect.center = (self.x + rect_size[0] // 2, self.y + rect_size[1] // 2)
        self.fi = math.atan2(rect_size[0], rect_size[1])
        self.l = (self.rect.width ** 2 // 4 + self.rect.height ** 2 // 4) ** 0.5
        self.need_rotate = nr
    def draw(self):
        image_r = pg.transform.scale(self.image, (self.size[0], self.size[1]))
        rect = image_r.get_rect()
        if self.need_rotate == True:
            image_r = pg.transform.rotate(image_r, -self.angle * 180 / 3.14 - 90)
            rect = image_r.get_rect()
            if self.fire != False:
                self.fire.draw(self.x - 30, self.y - 55)
        else:
            if self.start_t != 'line':
                image_r = pg.transform.flip(image_r, True, False)
            else:
                if self.need_rotate == 2:
                    pg.draw.line(screen, (255, 255, 255), (0, self.y), (G.WIDTH, self.y))
                else:
                    pg.draw.line(screen, (255, 255, 255), (self.x, 0), (self.x, G.HEIGHT))
                image_r = pg.transform.rotate(image_r, -self.angle * 180 / 3.14 - 90)
                rect = image_r.get_rect()
        rect.center = (self.x, self.y)
        screen.blit(image_r, rect)
        #pg.draw.rect(screen, G.GREEN, self.rect)
        #self.is_collide(pg.Rect(0,0,0,0))

    def is_collide(self, rect):
        cent = (self.x, self.y)
        d_x = math.sin(-self.angle + self.fi) * self.l
        d_y = math.cos(-self.angle + self.fi) * self.l
        d_sx = math.sin(-self.angle - self.fi) * self.l
        d_sy = math.cos(-self.angle - self.fi) * self.l
        # print(d_x, d_y, self.angle)
        points = [(cent[0] + d_x, cent[1] + d_y), (cent[0] - d_x, cent[1] - d_y), (cent[0] + d_sx, cent[1] + d_sy),
                  (cent[0] - d_sx, cent[1] - d_sy)]
        t = False
        for i in points:
            #pg.draw.circle(screen, G.BLUE, i, 5)
            if rect.collidepoint(i):
                t = True
                break
        return (t)
class Plane(Attack):
    def __init__(self, player):
        tex, siz, rs = ('materials/plane.png', (70, 70), (70, 30))
        self.player = player
        from battle_scene import give_angle
        self.turn = 2 * (random.randint(0,1) - 0.5)
        self.start_rotating = False
        if self.turn > 0:
            count_x = 1500
            angle = 3.14
        else:
            count_x = 100
            angle = 0
        self.fire = False
        speed = 6
        if boss.stage == 2 or boss.stage == 5:
            self.fire = Fire()
            speed = 7
        pos = (count_x, random.randint(100,300))
        self.angle = give_angle(pos, (player.x + player.rect.width // 2, player.y + player.rect.height // 2))
        angle = self.angle
        need_rotate = True
        self.speeds = [6 * (random.randint(0,1) - 0.5), 0]
        Attack.__init__(self, pos, angle, speed, tex, siz, rs, need_rotate, True, self.fire)
        self.count = 0
    def move(self):
        self.y += math.sin(self.angle) * self.speed
        self.x += math.cos(self.angle) * self.speed
        if self.x < 0 or self.y < 0 or self.x > G.WIDTH or self.y > G.HEIGHT:
            del draw_attacks[draw_attacks.index(self)]
        if self.y > self.player.y and ((self.turn > 0 and self.player.x > self.x) or (self.turn < 0 and self.player.x < self.x)):
            self.start_rotating = True
        else:
            if not self.start_rotating:
                if self.player.y < self.y:
                    self.angle += 0.001 * self.turn
                else:
                    self.angle -= 0.001 * self.turn
        if self.start_rotating:
            if abs(self.angle) >= 8:
                self.start_rotating = False
                return None
            self.angle += 0.05 * self.turn
class Scissors(Attack):
    def __init__(self, player, g = -1):
        tex, siz, rs = ('materials/scissors.png', (100, 100), (60, 50))
        from battle_scene import create_random_coord
        count_x = 0
        self.timer = 0
        self.player = player
        l = random.randint(0, 1)
        speed = 10
        if l == 0:
            count_x = random.randint(G.WIDTH // 2 - 100, G.WIDTH // 2 + 100)
            count_y = 100
            angle = 3.14/2
        else:
            count_y = random.randint(450, 650)
            speed = 10
            s = random.randint(0, 1)
            if s == 0:
                count_x = 100
                angle = 0
            else:
                count_x = 1500
                speed *= -1
                angle = 3.14

        pos = (count_x, count_y)
        self.w = l
        need_rotate = False
        self.speed = speed
        self.angle = angle
        self.need_rot = True
        if g != -1:
            l = g
        Attack.__init__(self, pos, angle, speed, tex, siz, rs, l * 2, 'line', False)
    def move(self):
        if self.timer >= 1.5:
            if self.w == 0:
                self.y += self.speed
            else:
                self.x += self.speed
        else:
            self.timer += 1 / G.FPS
        if self in draw_attacks and (self.x < 0 or self.y < 0 or self.x > G.WIDTH or self.y > G.HEIGHT):
            del draw_attacks[draw_attacks.index(self)]
class Many_scissors():
    def __init__(self, player):
        self.my_scissors = []
        for i in range(3):
            sc = Scissors(player, 1)
            sc.x = 100
            sc.y = 450 + i * 120
            sc.angle = 0
            sc.w = 1
            sc.speed = 8
            self.my_scissors.append(sc)
    def move(self):
        for i in self.my_scissors:
            if i.x < 0 or i.y < 0 or i.x > G.WIDTH or i.y > G.HEIGHT:
                del self.my_scissors[self.my_scissors.index(i)]
                continue
            i.move()
        if len(self.my_scissors) == 0:
            del draw_attacks[draw_attacks.index(self)]
    def draw(self):
        for i in self.my_scissors:
            i.draw()
    def is_collide(self, rect):
        t = False
        for i in self.my_scissors:
            if i.is_collide(rect):
                t = True
                break
        return(t)
class Fire():
    def __init__(self):
        from Scene_class import give_list_an as give
        self.images = give('Animations/fire')
        self.n = 0
        self.size = (100,100)
        from battle_scene import create_random_coord
        self.timer = 0
        speed = 10

        need_rotate = False
        self.speed = speed
        angle = 0
        self.rect = (0, 0, 60, 60)
        self.need_rot = True
    def draw(self, x, y):
        self.rect = (x, y, 60, 60)
        self.image = pg.image.load(self.images[self.n//self.speed])
        self.image = pg.transform.scale(
            self.image, (self.size[0], self.size[1]))
        self.n += 1
        if self.n == len(self.images) * self.speed:
            self.n = 0
        screen.blit(self.image, self.rect)
init_attack()