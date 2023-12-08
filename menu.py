#import main
import pygame as pg
import globalsc as G

panels = []

buttons = []

texts = []
pg.init()

dialogs =[['materials/Lunaface.png', (100, 100), 'dialogues\dialogue0.txt', 'Luna'], ['materials/ghostface.png', (100, 100), 'dialogues\dialogue1.txt', 'Ciesar']]
dialogues = []
index = 0

signal = True
now_active = True
can_return = True
timer = 0
length = 100

screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)

class Button:
    def __init__(self, text,  pos, size, font,  bg, screen):
        self.font = pg.font.SysFont('arial', font)
        self.screen = screen
        self.n = 0
        self.sost = False
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pg.Rect(self.x, self.y, 5, 5)
        self.text = text
        self.bg = bg
        self.Text = self.font.render(text, 1, pg.Color("Black"))
        #self.command()
        self.size = size
        self.change_colour()
        self.command = int
    def exit(self):
        #main.exit()
        self.text = str(self.n)
        self.n += 1
        self.Text = self.font.render(self.text, 1, pg.Color("Black"))
    def change_colour(self):
        #self.size = self.Text.get_size()
        self.rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
        if self.sost:
            fg = 'red'
        else:
            fg = self.bg
        self.surface = pg.Surface(self.size)
        self.surface.fill(fg)
        self.surface.blit(self.Text, (self.size[0]//2 - self.Text.get_width()//2, self.size[1]//2 - self.Text.get_height()//2))
    def show(self):
        screen.blit(self.surface, (self.x, self.y))
    def click(self, event):
        x, y = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x, y):
                self.sost = pg.mouse.get_pressed()[0]
                self.command()
                self.change_colour()
        else:
            self.sost = False
            self.change_colour()
class Sprite:
    def __init__(self, texture, pos, size):
        self.texture = texture
        self.pos = pos
        self.size = size
        self.image = pg.image.load(texture)
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pg.Rect(self.x, self.y, size[0], size[1])
        self.image = pg.transform.scale(
            self.image, (self.size[0], self.size[1]))
    def show(self):
        screen.blit(self.image, self.rect)
class Text:
    def __init__(self, text,  pos, color, font, screen):
        self.x, self.y = pos
        self.font = pg.font.SysFont("Arial", font)
        self.color = color
        self.text = text
        self.screen = screen
    def show(self):
        text = self.font.render(self.text, True, self.color)
        screen.blit(text, (self.x, self.y))
class Panel:
    def __init__(self,   pos, size,  color, screen):
        self.x, self.y = pos
        self.w, self.h = size
        self.color = color
        self.screen = screen
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
    def show(self):
        #pan = pg.Surface((self.w, self.h), self.color)
        pg.draw.rect(self.screen, self.color, self.rect)
        #screen.blit(pan, (self.x, self.y))
class Background:
    def __init__(self, screen):
        self.bg = pg.image.load("materials\sixth.jpg").convert()
        self.bg = pg.transform.scale(self.bg, (G.WIDTH, G.HEIGHT))
    def show(self):
        screen.blit(self.bg, (0, 0))
class Dialogue:
    def __init__(self, screen):
        self.screen = screen
        self.color = (255, 255, 255)
        self.x = 0
        self.y = G.HEIGHT // 2 - 350
        self.color_window = G.BLACK
        self.r = 10
        self.tx = G.WIDTH // 2 - 600
        self.ty = G.HEIGHT - 130
        self.active = False
        self.active_k = True
        self.index = 0
    def restart(self,index,  params, signal, sig_par):
        image, size, path_t, name = params
        self.signal = signal
        self.label = [name, G.name]
        text = separate(path_t)
        self.text = [self.label[0] + ": " + text[i] for i in range(len(text))]
        self.index = index
        self.active = True
        self.timer = 0
        self.now_length = 0
        self.font = pg.font.SysFont('times new roman', 30)
        self.typing_speed = 100
        self.rect = pg.Rect(250, 750, size[0], size[1])
        image = pg.image.load(image)
        self.image = pg.transform.scale(
            image, (size[0], size[1]))
        self.active_k = True
        self.sig_par = sig_par
    def show(self):
        if self.active:
            pg.draw.rect(self.screen, self.color_window, (200, 730, 1200, 800), border_radius=self.r)

            if self.index < len(self.text):
                now_text = self.text[self.index]
                if self.timer/5 < self.typing_speed:
                    self.now_length += 1
                    self.timer += 1/G.FPS
            else:
                self.active = False
                now_text = '...'
                self.signal(self.sig_par[0])
                if self.sig_par[-1] == 'delete_last':
                    from draw import now_scene as n
                    n.me.objects[-1].go_back()

                from draw import change_activity as ch
                ch(True)

            if self.now_length > len(now_text):
                self.now_length = len(now_text)

            if now_text != "":
                lines = self.wrap(now_text[:self.now_length], 70)
                y_offset = 0
                for line in lines:
                    text = self.font.render(line, True, self.color)
                    text_rect = text.get_rect()
                    text_rect.x = self.tx + 200
                    text_rect.y = self.ty - 20 + y_offset
                    self.screen.blit(text, text_rect)
                    y_offset += text_rect.height
                screen.blit(self.image, self.rect)
            else:
                self.index += 1
                self.now_length = 0
                if self.index >= len(self.text):
                    self.active = False


    def wrap(self, text, max_length):
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
    def update(self, keys):
        if sum(keys) > 0 :
            if self.active_k:
                self.index += 1
                self.now_length = 0
                self.active_k = False
        else:
            self.active_k = True
def separate(file):
    with open(file, 'r', encoding = 'utf-8') as file_text:
        text = file_text.read()
        phrases = text.split('@')
        return [phrase.strip() for phrase in phrases if phrase.strip()]
panload = Panel((500, 400), (length* 5, 50), G.GREEN, screen)
def start():
    global signal, index
    panload.screen = screen
    #Add function "Enter your name"
    d = Dialogue(screen)
    #d.restart(index, tuple(persons[0]))
    dialogues.append(d)
    #but = Button("Start", (600, 400), 30, "navy", screen)
    #but.command = but.exit
    #buttons.append(but)
    text = Text("Start", (800, 600), "navy", 30, screen)
    #texts.append(text)
    pan = Panel((800, 450), (30, 40), G.GREEN, screen)
    #panels.append(pan)
def create_dialog(number, signal, sig_par):
    dialogues[0].restart(index, tuple(dialogs[number]), signal, sig_par)
    from draw import change_activity as ch
    ch(False)
def pause(need_pause = True):
    global buttons, texts, panels, can_return
    if length >= 100:
        can_return = True
        if need_pause:
            pause(False)
            pan = Panel((0, 0), (G.WIDTH, G.HEIGHT), G.BLACK, screen)
            text = Text("Меню", (720, 120), "White", 70, screen)
            from main import unpause as unp
            from main import save as save
            but1 = Button("Настройки", (500, 400), ((G.WIDTH - 1000), 50), 30, (255, 255, 255), screen)
            but2 = Button("Выход в главное меню", (500, 500), ((G.WIDTH - 1000), 50), 30, (255, 255, 255), screen)
            but3 = Button("Сохранить игру", (500, 300), ((G.WIDTH - 1000), 50), 30, (255, 255, 255), screen)
            but4 = Button("Вернуться в игру", (500, 600), ((G.WIDTH - 1000), 50), 30, (255, 255, 255), screen)
            but4.command = unp
            but3.command = save
            but2.command = start_menu
            but1.command = settings

            panels.append(pan)
            texts.append(text)
            buttons.append(but1)
            buttons.append(but2)
            buttons.append(but3)
            buttons.append(but4)
        else:
            panels = []
            buttons = []
            texts = []
def settings():
    pause(False)
    pan = Panel((0, 0), (G.WIDTH, G.HEIGHT), G.BLACK, screen)
    text1 = Text("Настройки", (680, 120), "White", 70, screen)
    text2 = Text("Ну эээ а что здесь может быть?", (400, 290), "White", 70, screen)
    but1 = Button("Назад", (500, 600), ((G.WIDTH - 1000), 50), 30, (255, 255, 255), screen)
    but1.command = pause
    panels.append(pan)
    texts.append(text1)
    texts.append(text2)
    buttons.append(but1)
    pass
def start_menu():
    global can_return
    pause(False)
    can_return = False
    pan = Panel((0, 0), (G.WIDTH, G.HEIGHT), G.BLACK, screen)
    text1 = Text("Главное меню", (620, 120), "White", 70, screen)
    text2 = Text("M    T", (510, 200), (50, 50, 50), 280, screen)
    text3 = Text("  I P", (560, 185), (30, 30, 30), 280, screen)
    but1 = Button("Новая игра", (500, 550), ((G.WIDTH - 1000), 50), 30, (255, 255, 255), screen)
    but2 = Button("Загрузить игру", (500, 650), ((G.WIDTH - 1000), 50), 30, (255, 255, 255), screen)
    but3 = Button("Выйти", (500, 750), ((G.WIDTH - 1000), 50), 30, (255, 255, 255), screen)
    from main import clear as cl
    from main import load as load
    but1.command = cl
    but2.command = load
    sprite = Sprite('Animations/wh_cat_stay/1.png', (740, 370), (140, 140))
    #sprite2 = Sprite('materials/cateyes.png', (-400, 0), (2400, 900))
    but3.command = exit

    panels.append(pan)
    texts.append(text1)
    texts.append(text2)
    texts.append(text3)
    texts.append(sprite)
    #panels.append(sprite2)
    buttons.append(but1)
    buttons.append(but2)
    buttons.append(but3)
    loading()
def loading():
    pan  = Panel((0, 0), (G.WIDTH, G.HEIGHT), G.BLACK, screen)
    panels.append(pan)
    global timer, length, now_active
    now_active = False
    timer = 0
    length = 0
def update(events, keys):
    global length, timer, now_active
    screen.fill(G.WHITE)
    #Background(screen).show()
    if length >= 100:
        for p in panels:
            p.show()
        for b in buttons:
            b.show()
            for ev in events:
                b.click(ev)
        for t in texts:
            t.show()
        for d in dialogues:
            d.show()
            d.update(keys)
    else:
        panels[-1].show()
        if timer <= 2:
            length += 0.5
        elif timer > 2 and timer <= 3:
            length += 0.25
        elif timer > 3:
            length += 1
        pg.draw.rect(screen, (60,60,60), (panload.x - 10, panload.y - 10, 100 * 6 + 20, 70))
        panload.rect.w = length * 6
        panload.show()
        timer += 1/ G.FPS
        if length >= 100:
            panels.pop()
            now_active = True
    return screen