import pygame as pg
import globalsc as G

screen = pg.Surface((G.WIDTH * 2, G.HEIGHT), G.WHITE)
class CollisionShape():
    def __init__(self, x , y, size):
        self.x = x
        self.y = y
        self.rect = pg.Rect((x, y, size[0], size[1]))
    def is_collide(self, rec):
        return(self.rect.colliderect(rec))
    def push_on(self, rec, vel):
        y1, y2 = self.y - rec.height, self.y + self.rect.height
        if vel > 0 :
            return(y1)
        else:
            return(y2)
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
            x, y, w, h, r = self.parameters
            pg.draw.rect(screen, self.color, (x, y, w, h), r)
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
class AnimatedSprite():
    def __init__(self, images, speed, stop, pos, size = None):
        self.images = images
        self.image = pg.image.load(images[0])
        self.x = pos[0]
        self.y = pos[1]
        self.size = [self.image.get_width(), self.image.get_height()]
        if size!= None:
            self.size = size
        self.n = 0
        self.speed = speed
        self.stop = stop
        self.rect = pg.Rect(self.x, self.y, size[0], size[1])
    def draw(self):
        if self.n != len(self.images ) * self.speed:
            self.image = pg.image.load(self.images[self.n//self.speed])
            self.image = pg.transform.scale(
                self.image, (self.size[0], self.size[1]))   
            self.n += 1
            if self.n == len(self.images) * self.speed and not self.stop:
                self.n = 0
            screen.blit(self.image, self.rect)    
        else:
            self.image = pg.image.load(self.images[-1])
            self.image = pg.transform.scale(
                self.image, (self.size[0], self.size[1]))   
            screen.blit(self.image, self.rect)       
class Dialogue():
    def __init__(self):
        self.r = 10
        self.x = 100
        self.y = 100
        self.color = G.BLACK
        self.r = 5
        self.tx = 300
        self.ty = 100
        self.v = 30
    def draw(self):
        rect = pg.Rect(self.x, self.y, 300, 300)
        pg.draw.rect(self.screen, self.color, rect, border_radius = self.r)
    def interior(self):
        file = open('dialogues\dialogue0.txt', 'r')
        text = list(map(lambda x: x.rstrip("\\"), file.readlines()))
        for i in range(len(text)):
            if i % 2 == 0:
                lab1 = Sc.PlayLabel(text[i], (self.tx, self.ty), G.WHITE, 30)
                objects.append(lab1)
            else:                
                lab2 = Sc.PlayLabel(text[i], (self.tx, self.ty), G.WHITE, 30)
                objects.append(lab2)
            self.ty += self.v
class KinematicBody():
    def __init__(self, obj, typ, parameters):
        self.obj = obj
        self.typ = typ
        self.p = parameters
    def move(self):
        if self.typ == 1:
            self.obj.rect.x += self.p['speed'][0]
            self.obj.rect.y += self.p['speed'][1]
        
def change_scene(obj = None, scene = None, param = None):
    number = 2
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

def give_list_an(file_name):
    anim = [file_name + '/' + str(x) + '.png' for x in range(1, G.howmanyFiles(file_name) + 1)]
    return anim
def go_in_btl(obj = None, scene = None, number = None):
    from draw import go_in_battle as battle
    battle(number)
    