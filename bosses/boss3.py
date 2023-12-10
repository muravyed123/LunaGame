import pygame as pg
import math
import sys
sys.path.append('..')
import globalsc as G
import random
hitpoints = 200
textures = ['materials/ghostbody2.png', 'materials/ghosthat.png', 'materials/ghosteyes2.png']
hands = 'materials/ghosthands2.png'
sizes = [(280, 280), (280, 280), (280, 280)]
coords = [(660, 30), (660, 30), (660, 30)]
can_move = [0, 0, 1]
music = 2
texts = ['Что ?? Что ты тут делаешь. На МОЕЙ кухне!!. Прочь!', 'Что? Мой брат? Спасение всех? Враки', 'Об этом давно стоило бы забыть!', 'Знаешь почему я использую огурцы? КОШКИ боятся огурцов АХаххахАХхаха Шубара, шубара', 'Знаешь, тут так редко кто-то бывает, что  я даже рад тебе']
defns = [2, 3, 5, 5, 5, 5, 5]
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
boss_attacks = []
draw_attacks = []
boss = None


def init_attack():
    global boss_attacks, boss
    boss = Boss()
    boss_attacks = [[{'attack': Knife, 'count': 2, 'time': 5},
                     {'attack': Cucum,'count': 5, 'time': 2}],
                    [{'attack': Knife, 'count': 3, 'time': 5},
                     {'attack': Knife, 'count': 5, 'time': 2},
                     {'attack': Knife, 'count': 3, 'time': 5},
                     {'attack': Knife, 'count': 5, 'time': 2}
                     ],
                    [{'attack': Cucum,'count': 5, 'time': 2},
                     {'attack': Knife, 'count': 2, 'time': 4},
                     {'attack': Cucum,'count': 5, 'time': 2},
                     {'attack': Knife, 'count': 2, 'time': 4},
                     {'attack': Cucum,'count': 5, 'time': 2},
                     ],
                    [{'attack': Cucum, 'count': 1, 'time': 1},
                     {'attack': Knife, 'count': 4, 'time': 4},
                     {'attack': Cucum, 'count': 1, 'time': 1},
                     {'attack': Knife, 'count': 4, 'time': 4},
                     {'attack': Cucum, 'count': 10, 'time': 2},
                     ],
                    [{'attack': Cucum, 'count': 3, 'time': -1},
                     {'attack': Knife, 'count': 4, 'time': 2},
                     {'attack': Knife, 'count': 4, 'time': 2},
                     {'attack': Cucum, 'count': 8, 'time': 10},
                     {'attack': Knife, 'count': 4, 'time': 2},
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
        self.ay = 0.5
        self.moveh = 1
        self.stage = 0
    def draw(self):
        self.n = 0
        screen.fill(G.WHITE)
        for i in range(len(self.textures)):
            screen.blit(self.textures[i], self.positions[i])
            if self.can_move[i] == 1:
                self.move(i)
        if self.stage == 3:
            image = pg.image.load(hands)
            image = pg.transform.scale(image, (230, 280))
            if self.moveh == 1:
                screen.blit(image, (682, 30 + self.vy))
            else:
                screen.blit(image, (682 + self.vy, 30))

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
        if abs(self.vy) > 30:
            self.ay *= -1
        self.vy += self.ay
        if self.vy == 0 and self.ay < 0:
            self.moveh *= -1
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
        text = ''
        if self.timer > 2 and self.timer < 6:
            text = 'Ну эээ, у меня огурцы кончились, дальше не прикольно будет'
        elif self.timer >= 7 and self.timer < 12:
            image = pg.image.load('materials/cucmb_price.png')
            image = pg.transform.scale(image, (300, 200))
            text = 'Знаешь какие цены  на них сейчас? О - го - го'
            screen.blit(image, (600, 220))
        elif self.timer >= 12.5 and self.timer < 18:
            text = 'Предлагаю сделку: Ты не скажешь никому, что здесь было, а я помогу тебе.'
        elif self.timer >= 19 and self.timer < 25:
            text = 'Когда- то давно во времена, которые я уже не смогу вспомнить, мы с братом жили на втором этаже и....'
        elif self.timer >= 25 and self.timer < 30:
            text = 'Ну в общем мы и хотели там остаться после.. Но.. неведомая сила, она, сделала так, что мы оказались здесь...'
        elif self.timer >= 30 and self.timer < 37:
            text = 'Больше я ничего не знаю и не смогу ничего рассказать. Мы жили у лестницы, что рядом с душем, сходи туда и проверь, что там живет вместо нас.'
        elif self.timer >= 38 and self.timer < 45:
            text = 'Думаю, так ты найдешь ответы на свои вопросы. Прощай. Спасибо за знакомство, хоть оно и было коротким. А я пошел собирать огурцы с пола.'
        elif self.timer >= 45:
            from draw import remove_checkpoints as ch
            ch(3)
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
class Cucum(Attack):
    def __init__(self, player):
        tex, siz, rs = ('materials/cucumber.png', (70, 70), (70, 30))
        self.player = player
        from battle_scene import give_angle
        count_x = G.WIDTH // 2
        while count_x <= G.WIDTH // 2 + 150 and count_x > G.WIDTH // 2 - 150:
            count_x = random.randint(200, G.WIDTH - 200)
        pos = (count_x, random.randint(100, 300))

        angle = 0
        need_rotate = False
        self.speeds = [6 * (random.randint(0,1) - 0.5), 0]
        speed = 6
        Attack.__init__(self, pos, angle, speed, tex, siz, rs, need_rotate)
        self.count = 0
    def move(self):
        self.y += self.speeds[1]
        self.x += self.speeds[0]
        self.speeds[1] += 0.1
        if self.y > G.HEIGHT:
            self.y -= self.speeds[1]
            self.speeds[1] *= -0.8
            self.count += 1
        if self.x < 200 or self.x > G.WIDTH - 200:
            self.x -= self.speeds[0]
            self.speeds[0] *= -0.8
            self.count += 1
        if self.count >= 4:
            del draw_attacks[draw_attacks.index(self)]
class Knife(Attack):
    def __init__(self, player):
        tex, siz, rs = ('materials/knife.png', (100, 100), (70, 30))
        from battle_scene import create_random_coord
        count_x = 0
        self.player = player
        while count_x <= G.WIDTH // 2 - 250 + 100 + 300 and count_x > G.WIDTH // 2 - 150:
            count_x = random.randint(100, G.WIDTH - 100)
        pos1 = random.randint(max(400, int(math.floor(player.y)) - 50), min(650, int(math.floor(player.y)) + 50))
        pos0 = create_random_coord()[0]
        pos = (pos0, pos1)
        angle = 3.14/2 * random.randint(0, 3)
        speed = 8
        self.need_rot = True
        Attack.__init__(self, pos, angle, speed, tex, siz, rs, True)
    def move(self):
        if self.need_rot:
            from battle_scene import give_angle
            need_angle = give_angle((self.x, self.y), (self.player.x + self.player.rect.width // 2, self.player.y + self.player.rect.height // 2))
            if abs(self.angle - need_angle) % 6.28 > 0.05:
                self.angle += 0.03
            else:
                self.need_rot = False
                self.angle = need_angle
        else:
            self.y += math.sin(self.angle) * self.speed
            self.x += math.cos(self.angle) * self.speed
            if self.x < 0 or self.y < 0 or self.x > G.WIDTH or self.y > G.HEIGHT:
                del draw_attacks[draw_attacks.index(self)]
init_attack()