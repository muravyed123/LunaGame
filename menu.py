#import main
import pygame as pg
import globalsc as G

panels = []

buttons = []

texts = []
pg.init()

dialogues = []

screen = pg.Surface((1280, 720), G.WHITE)

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
class Dialogue():
    def __init__(self, screen, text, person, name):
        self.r = 10
        self.x = G.WIDTH // 2 - 400
        self.y = G.HEIGHT // 2 - 350
        self.color = G.BLACK
        self.r = 5
        self.tx = G.WIDTH // 2
        self.ty = G.HEIGHT - 10
        self.v = 0.5
        self.index = 0
        self.font = pg.font.SysFont("Arial", 30)
        self.label = [person, name]
        self.text = [self.label[i % 2] + ": " + text[i] for i in range(len(text))]
        self.screen = screen
        self.now_text = text[self.index]

    def show(self):
        self.ty -= self.v

        rect = pg.Rect(self.x, self.y, 800, 700)
        pg.draw.rect(self.screen, self.color, rect, border_radius=self.r)

        if self.now_text == "":
            if self.index < len(self.text):
                self.now_text = self.text[self.index]
                self.index += 1
        else:
            text = self.font.render(self.label[self.index % 2] + ': ' + self.now_text, True, G.WHITE)
            text_rect = text.get_rect()
            text_rect.centerx = G.WIDTH // 2
            text_rect.bottom = self.ty
            self.screen.blit(text, text_rect)

def separate(file):
    with open(file, 'r') as file_text:
        text = file_text.read()
        phrases = text.split('@')
        return [phrase.strip() for phrase in phrases if phrase.strip()]
def start():
    #Add function "Enter your name"
    text = separate('dialogues\dialogue0.txt')
    but = Button("Start", (600, 400), 30, "navy", screen)
    but.command = but.exit
    #dialogues.append(Dialogue(screen, text, 'Luna', 'Kitty'))
    #buttons.append(but)
    text = Text("Start", (800, 600), "navy", 30, screen)
    #texts.append(text)
    pan = Panel((800, 450), (30, 40), G.GREEN, screen)
    #panels.append(pan)
def update(events):
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
    return screen
