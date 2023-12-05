import pygame as pg
import math
import sys
sys.path.append('..')
import globalsc as G
hitpoints = 10
textures = ['materials/tar_1.png', 'materials/tar_2.png', 'materials/tar_3.png']
sizes = [(250, 250), (250, 250), (250, 250)]
coords = [(675, 100), (675, 100), (675, 100)]
can_move = [1, 0, 0]
texts = ['ЗАЧЕМ ТЫ НАРУШИЛ МОЙ ПОКОЙ','Çucaracha applauds faster!','Çucaracha laughs!', 'Auuufff']
defns = [5, 5, 5, 5]
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
boss_attacks = []
draw_attacks = []
boss = None


def init_attack():
    global boss_attacks, boss
    boss = Boss()
    boss_attacks = [[{'attack': Arrow, 'count': 3, 'time': 5},
               {'attack': Arrow, 'count': 6, 'time': 5}],
               [{'attack': Arrow, 'count': 5, 'time': 5},
                {'attack': Arrow, 'count': 12, 'time': 5},
                {'attack': Arrow, 'count': 20, 'time': 5}]]

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
            self.vel[self.n]  = ( -vel[0], vel[1])
            vel = (-vel[0], vel[1])
        elif abs(self.positions[i][1] - self.abs_pos[i][1]) >= 3:
            self.vel[self.n] = (vel[0], -vel[1])
            vel = (vel[0], -vel[1])
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
        size = (200, 200)
        image = pg.image.load('materials/tapok.png')
        image = pg.transform.scale(image, (size[0], size[1]))
        if self.timer > 3 and self.timer < 6:
            image = pg.transform.rotate(image, (self.timer - 3) * 120)
            screen.blit(image, (G.WIDTH - size[0] - (self.timer - 3) * (G.WIDTH // 2 - size[0] // 2) // 3 + 30, 120))
        elif self.timer >= 6 and self.timer < 9:
            screen.blit(image, (G.WIDTH // 2 - size[0] // 2 + 30, 120))
        elif self.timer >= 9:
            from draw import checkpoints as ch
            ch[0] = True
            return(True)
        self.timer += 1/ G.FPS
        return(False)

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
        self.rect.center = (self.x + rect_size[0] // 2, self.y + rect_size[1] // 2)
        self.fi = math.atan2(rect_size[0], rect_size[1])
        self.l = (self.rect.width ** 2 // 4 + self.rect.height ** 2 // 4) ** 0.5
    def draw(self):
        image_r = pg.transform.scale(self.image, (self.size[0], self.size[1]))

        new_r = pg.transform.rotate(image_r, -self.angle * 180 / 3.14 - 90)
        rect = new_r.get_rect()
        rect.center = (self.x, self.y)
        screen.blit(new_r, rect)
        # pg.draw.rect(screen, G.GREEN, self.rect)

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
            if rect.collidepoint(i):
                t = True
                break
            # pg.draw.circle(screen, G.BLUE, i, 5)
        return (t)
class Arrow(Attack):
    def __init__(self, player):
        tex, siz, rs = ('materials/arrow.png', (100, 100), (70, 20))
        from battle_scene import give_angle
        from battle_scene import create_random_coord
        pos = create_random_coord()
        angle = give_angle(pos, (player.x + player.rect.width // 2, player.y + player.rect.height // 2))
        speed = 6
        Attack.__init__(self, pos, angle, speed, tex, siz, rs)
    def move(self):
        self.y += math.sin(self.angle) * self.speed
        self.x += math.cos(self.angle) * self.speed
        if self.x < 0 or self.y < 0 or self.x > G.WIDTH or self.y > G.HEIGHT:
            del draw_attacks[draw_attacks.index(self)]
init_attack()