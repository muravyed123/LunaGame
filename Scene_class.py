import pygame as pg
import globalsc as G

class CollisionShape():
    def __init__(self, x , y, size):
        self.x = x
        self.y = y
        self.rect = pg.Rect((x, y, size[0], size[1]))
    def is_collide(self, rec):
        return(self.rect.colliderect(rec))
    def push_on(self, rec):
        y1, y2 = self.y - rec.height, self.y + self.rect.height
        if abs(rec.y - y1) > abs(rec.y - y2):
            return(y2)
        else:
            return(y1)
    def draw(self):
        screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
        screen.fill(G.WHITE)
        pg.draw.rect(screen, G.BLUE, self.rect)    
        screen.set_alpha(100)
        return(screen)
class Object():
    def __init__(self, fig, color, parameters,x = 0, y = 0):
        self.screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
        if fig == 'rect':
            pg.draw.rect(self.screen, color, parameters)
        elif fig == 'çircle':
            pg.draw.circle(self.screen, color, parameters)
        elif fig == 'polygon':
            pg.draw.polygon(self.screen, color, parameters)
    def draw(self):
        return(self.screen)
class Area():
    def __init__(self, x , y, size, signal, p1 = None, signal_ex = None, p2 = None):
        self.x = x
        self.y = y
        self.rect = pg.Rect((x, y, size[0], size[1]))
        self.signal = signal
        self.signal_ex = signal_ex
        self.p1 = p1
        self.p2 = p2
        self.screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
        self.is_collide = False
    def is_collide(self, rec):
        t = self.rect.colliderect(rec)
        if t:
            self.is_collide = True
            return((t, self.signal, self.p1))
        else:
            if self.is_collide:
                return((t, self.signal_ex, self.p2))
            else: return((t, None, None))
    def draw(self):
        pg.draw.rect(self.screen, G.GREEN, self.rect)    
        self.screen.set_alpha(100)
        return(self.screen)
class Playlabel():
    def __init__(self, text,  pos, color, font):
        self.x, self.y = pos
        self.font = pg.font.SysFont("Arial", font)
        self.color = color
        self.text = text
        self.screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
    def draw(self):
        text = self.font.render(self.text, True, self.color)        
        self.screen.blit(text, (self.x, self.y))    
        return self.screen
class PlayButton():
    def __init__(self, text,  pos, font, bg):
        self.x, self.y = pos
        self.font = pg.font.SysFont('arial', font)
        self.screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
        self.n = 0
        self.sost = False
        self.rect = pg.Rect(self.x, self.y, 5, 5)
        self.text = text
        self.bg = bg
        self.Text = self.font.render(text, 1, pg.Color("White"))
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
def change_scene(obj, scene, param):
    number = 1
    from draw import change_scene as change
    change(number)
def create_label(obj, scene, param):
    lab_n = PlayLabel(param)
def delete_label(obj, scene, param):
    pass
    
