import pygame as pg
import math
import sys
sys.path.append('..')
import globalsc as G
import random
hitpoints = 200
textures = ['materials/ghostb.png', 'materials/ghosthands.png', 'materials/ghosteyes.png']
sizes = [(250, 250), (250, 250), (250, 250)]
coords = [(675, 100), (675, 100), (675, 100)]
can_move = [0, 1, 1]
texts = ['ДУХ ПРАЧЕЧНОЙ неодобрительно смотрит свысока','Эти пузырьки созданы с помощью белого стирального порошка : .    .   ..  Я забыл (здесь могла быть ваша реклама)','Как у тебя получается? Я стараюсь изо всех сил!', 'УУУ- уу - УУ- уу', 'Знаешь, порой мне страшно тут в одиночестве..', 'Не хочешь остаться здесь со мной?']
defns = [2, 3, 5, 5, 5, 5, 5]
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
boss_attacks = []
draw_attacks = []
boss = None


def init_attack():
    global boss_attacks, boss
    boss = Boss()
    boss_attacks = [[{'attack': Spit, 'count': 3, 'time': 5},
               {'attack': Ball, 'count': 5, 'time': 5}],
               [{'attack': Ball, 'count': 5, 'time': 5},
                {'attack': Ball, 'count': 10, 'time': 5},
                {'attack': Ball, 'count': 8, 'time': 5}],
                    [{'attack': Ball, 'count': 10, 'time': 1},
                     {'attack': Spit, 'count': 5, 'time': 5},
                     {'attack': Ball, 'count': 5, 'time': 5}],
                    [{'attack': Ball, 'count': 8, 'time': 1},
                     {'attack': Ball, 'count': 5, 'time': 5},
                     {'attack': Ball, 'count': 5, 'time': 5}],
                    [{'attack': Ball, 'count': 5, 'time': -1},
                    {'attack': Spit, 'count': 2, 'time': 5},
                    {'attack': Ball, 'count': 5, 'time': -1},
                    {'attack': Spit, 'count': 2, 'time': 5},
                    {'attack': Ball, 'count': 5, 'time': -1}],
                    [{'attack': Ball, 'count': 10, 'time': 1},
                     {'attack': Ball, 'count': 5, 'time': 5},
                     {'attack': Ball, 'count': 5, 'time': 5}]
                    ]

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
        self.vel = [(0.05,0.1)] * sum(can_move)
        self.n = 0
        self.timer = 0
        self.stage = 0
    def draw(self):
        self.n = 0
        screen.fill(G.WHITE)
        for i in range(len(self.textures)):
            screen.blit(self.textures[i], self.positions[i])
            if self.can_move[i] == 1:
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
        for i in range(len(self.textures)):
            screen.blit(self.textures[i], self.positions[i])
        size = (200, 50)
        image = pg.image.load('materials/tobrone.png')
        image = pg.transform.scale(image, (size[0], size[1]))
        kurs = pg.image.load('materials/kursor.png')
        kurs = pg.transform.scale(kurs, (30, 30))
        if self.timer > 2 and self.timer < 4:
            #image = pg.transform.rotate(image, (self.timer - 3) * 120)
            screen.blit(image, (G.WIDTH - size[0] - (self.timer - 2) * 60 + 30, 120))
        elif self.timer >= 4 and self.timer < 7:
            screen.blit(image, (G.WIDTH - size[0] - 90, 120))
        elif self.timer >= 7 and self.timer < 10:
            screen.blit(image, (G.WIDTH - size[0] - 90, 120))
            screen.blit(kurs, (G.WIDTH - size[0] - (self.timer - 7) * 60 + 200, 140))
        elif self.timer >= 10 and self.timer < 13:
            screen.blit(image, (G.WIDTH - size[0] - 90, 120))
            screen.blit(kurs, (G.WIDTH - size[0] - 3 * 60 + 200, 140))
        elif self.timer >= 13 and self.timer < 15:
            screen.blit(image, (G.WIDTH - size[0] - 90, 120))
            screen.blit(kurs, (G.WIDTH - size[0] - 3 * 60 + 200, 140))
            gas = pg.image.load('materials/pot.png')
            gas = pg.transform.scale(gas, (300, 200))
            screen.blit(gas, (G.WIDTH // 2, 140))
        elif self.timer >= 15:
            from draw import remove_checkpoints as ch
            ch(1)
            return(True)
        self.timer += 1/ G.FPS
        return(False)

class Attack():
    def __init__(self, pos, angle, speed, texture, size, rect_size, nr):
        self.x = pos[0]
        self.y = pos[1]
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
        if self.need_rotate:
            image_r = pg.transform.rotate(image_r, -self.angle * 180 / 3.14 - 90)
            rect = image_r.get_rect()
        else:
            if self.angle >= 3.14:
                image_r = pg.transform.flip(image_r, True, False)
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
class Ball(Attack):
    def __init__(self, player):
        tex, siz, rs = ('materials/ball.png', (50, 50), (30, 30))
        self.player = player
        from battle_scene import give_angle
        from battle_scene import create_random_coord
        pos = create_random_coord()

        angle = give_angle(pos, (player.x + player.rect.width // 2, player.y + player.rect.height // 2)) + random.randint(-30, 30)/ 180 * 2 * 3.14
        need_rotate = False
        speed = 6
        Attack.__init__(self, pos, angle, speed, tex, siz, rs, need_rotate)
    def move(self):
        self.y += math.sin(self.angle) * self.speed
        self.x += math.cos(self.angle) * self.speed
        from battle_scene import give_angle
        new_angle = give_angle((self.x, self.y), (self.player.x + self.player.rect.width // 2, self.player.y + self.player.rect.height // 2))
        w = 0.01
        if abs(self.angle - new_angle) % 6.28 > w:
            self.angle -= w * ((new_angle - self.angle) % 6.28 - 3.14) / (abs((new_angle - self.angle) % 6.28 - 3.14))
        if self.x < 0 or self.y < 0 or self.x > G.WIDTH or self.y > G.HEIGHT:
            del draw_attacks[draw_attacks.index(self)]
class Spit(Attack):
    def __init__(self, player):
        tex, siz, rs = ('materials/wave.png', (100, 70), (70, 40))
        from battle_scene import create_random_coord
        count_x = 0
        while count_x <= G.WIDTH // 2 - 250 + 100 + 300 and count_x > G.WIDTH // 2 - 150:
            count_x = random.randint(100, G.WIDTH - 100)
        pos1 = random.randint(max(400, int(math.floor(player.y)) - 50), min(650, int(math.floor(player.y)) + 50))
        pos0 = create_random_coord()[0]
        pos = (pos0, pos1)
        angle = int((pos[0] - G.WIDTH // 2 + 150) < 0) * 3.14
        speed = -8
        Attack.__init__(self, pos, angle, speed, tex, siz, rs, False)
    def move(self):
        self.y += math.sin(self.angle) * self.speed
        self.x += math.cos(self.angle) * self.speed
        if self.x < 0 or self.y < 0 or self.x > G.WIDTH or self.y > G.HEIGHT:
            del draw_attacks[draw_attacks.index(self)]
init_attack()