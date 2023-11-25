import pygame as pg
import globalsc as G

screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
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
        pg.draw.rect(screen, G.BLUE, self.rect)    
        return(screen)
class Object():
    def __init__(self, fig, color, parameters,x = 0, y = 0):
        self.fig = fig
        self.x = x
        self.y = y
        self.color = color
        self.parameters = parameters
    def draw(self):
        if self.fig == 'rect':
            pg.draw.rect(screen, self.color, self.parameters)
        elif fig == 'çircle':
            pg.draw.circle(screen, self.color, self.parameters)
        elif fig == 'polygon':
            pg.draw.polygon(screen, self.color, self.parameters)
class Area():
    def __init__(self, x , y, size, signal, p1 = None, signal_ex = None, p2 = None):
        self.x = x
        self.y = y
        self.rect = pg.Rect((x, y, size[0], size[1]))
        self.signal = signal
        self.signal_ex = signal_ex
        self.p1 = p1
        self.p2 = p2
        
        self.info = 0
        self.is_collid = False
    def is_collide(self, rec):
        t = self.rect.colliderect(rec)
        if t:
            if not self.is_collid:
                self.is_collid = True
                return((t, self.signal, self.p1))
            else:
                return((t, None, None))
        else:
            #print(self.is_collid)
            if self.is_collid:
                self.is_collid = False  
                return((t, self.signal_ex, self.p2))
            else: return((t, None, None))
    def draw(self):
        pg.draw.rect(screen, G.GREEN, self.rect)    
class PlayLabel():
    def __init__(self, text,  pos, color, font):
        self.x, self.y = pos
        self.font = pg.font.SysFont("Arial", font)
        self.color = color
        self.text = text
    def draw(self):
        text = self.font.render(self.text, True, self.color)        
        screen.blit(text, (self.x, self.y))    
class CheckText(PlayLabel):
    def __init__(self, text,  pos, color, font, key, command, param):
        self.x, self.y = pos
        self.font = pg.font.SysFont("Arial", font)
        self.color = color
        self.text = text
        self.key = key
        self.command = command
        self.param = param
    def click(self, keys):
        if keys[self.key]:
            self.command(self.param)  
class Sprite():
    def __init__(self, texture, pos, size = None):
        self.image = pg.image.load(texture)
        self.x = pos[0]
        self.y = pos[1]
        self.size = [self.image.get_width(), self.image.get_height()]
        if size!= None:
            self.size = size
        self.rect = pg.Rect(self.x, self.y, size[0], size[1])
        self.image = pg.transform.scale(
            self.image, (self.size[0], self.size[1]))        
    def draw(self):
        screen.blit(self.image, self.rect)
        
def change_scene(obj = None, scene = None, param = None):
    number = 1
    from draw import change_scene as change
    change(number)
def create_label(obj, scene, param):
    text, pos, color, font = param
    lab_n = PlayLabel(text, pos, color, font)
    obj.info = len(scene)
    scene.append(lab_n)
def delete_obj(obj, scene, param):
    del scene[obj.info]
def create_checktext(obj, scene, param):
    text, pos, color, font, key, command, par = param
    cht_n = CheckText(text, pos, color, font, key, command, par)
    cht_n.command = command
    obj.info = len(scene)
    scene.append(cht_n)