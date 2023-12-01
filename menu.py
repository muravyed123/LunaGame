#import main
import pygame as pg
import globalsc as G

panels = []

buttons = []

texts = []
pg.init()

screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)

class Button:
    def __init__(self, text,  pos, font, bg, screen):
        # Я не знаю как передавать в инит команду, которую будет выполнять кнопка при нажатии, пока пусть будет типом задаваться.
        self.x, self.y = pos
        self.font = pg.font.SysFont('arial', font)
        self.screen = screen
        self.n = 0
        self.sost = False
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
def start():
    but = Button("Start", (600, 400), 30, "navy", screen)
    but.command = but.exit
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
    return(screen)