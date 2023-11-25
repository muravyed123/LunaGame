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
    def __init__(self, x , y, size, signal):
        self.x = x
        self.y = y
        self.rect = pg.Rect((x, y, size[0], size[1]))
        self.signal = signal
    def is_collide(self, rec):
        return((self.rect.colliderect(rec), self.signal))
    def draw(self):
        screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
        screen.fill(G.WHITE)
        pg.draw.rect(screen, G.GREEN, self.rect)    
        screen.set_alpha(100)
        return(screen)
def change_scene():
    number = 1
    from draw import change_scene as change
    change(number)
    
