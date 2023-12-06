#import main
import pygame as pg
import globalsc as G

panels = []

buttons = []

texts = []
pg.init()

dialogs =[['materials/Lunaface.png', (100, 100), 'dialogues\dialogue0.txt', 'Luna']]
dialogues = []
index = 0

signal = True

screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)

class Button:
    def __init__(self, text,  pos, font, bg, screen):
        self.font = pg.font.SysFont('arial', font)
        self.screen = screen
        self.n = 0
        self.sost = False
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pg.Rect(self.x, self.y, 5, 5)
        self.text = text
        self.bg = bg
        self.Text = self.font.render(text, 1, pg.Color("White"))
        #self.command()
        self.change_colour()
        self.command = int
    def exit(self):
        #main.exit()
        self.text = str(self.n)
        self.n += 1
        self.Text = self.font.render(self.text, 1, pg.Color("White"))
    def change_colour(self):
        self.size = self.Text.get_size()
        self.rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
        if self.sost:
            fg = 'red'
        else:
            fg = self.bg
        self.surface = pg.Surface(self.size)
        self.surface.fill(fg)
        self.surface.blit(self.Text, (0, 0))
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
        self.h, self.w = size
        self.color = color
        self.screen = screen
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
    def show(self):
        pan = pg.Surface((self.w, self.h))
        screen.blit(pan, (self.x - self.w//2, self.y - self.h//2))
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
                    print(self.sig_par)

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
                self.active_k = False
        else:
            self.active_k = True
def separate(file):
    with open(file, 'r', encoding = 'utf-8') as file_text:
        text = file_text.read()
        phrases = text.split('@')
        return [phrase.strip() for phrase in phrases if phrase.strip()]

def start():
    global signal, index
    #Add function "Enter your name"
    d = Dialogue(screen)
    #d.restart(index, tuple(persons[0]))
    dialogues.append(d)
    but = Button("Start", (600, 400), 30, "navy", screen)
    but.command = but.exit
    #buttons.append(but)
    text = Text("Start", (800, 600), "navy", 30, screen)
    #texts.append(text)
    pan = Panel((800, 450), (30, 40), G.GREEN, screen)
    #panels.append(pan)
def create_dialog(number, signal, sig_par):
    dialogues[0].restart(index, tuple(dialogs[number]), signal, sig_par)
    from draw import change_activity as ch
    ch(False)
def update(events, keys):
    screen.fill(G.WHITE)
    #Background(screen).show()
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
    return screen