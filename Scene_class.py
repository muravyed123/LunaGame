import pygame as pg
import globalsc as G

screen = pg.Surface((G.WIDTH * 2, G.HEIGHT), G.WHITE)
change_screen = pg.Surface((G.WIDTH * 2, G.HEIGHT), G.WHITE)
""""global collisions, objects, areas
    colis1 = Sc.CollisionShape(0, 0, (20, 460))
    colis2 = Sc.CollisionShape(1000, 0, (20, 460))
    colis3 = Sc.CollisionShape(300, 250, (60, 60))
    colis4 = Sc.CollisionShape(500, 60, (80, 60))
    
    spr2 = Sc.Sprite(textures[1], (700, 200), (100, 250))
    spr3 = Sc.Sprite(textures[1], (300, 200), (100, 250))
    wall = Sc.Sprite(textures[2], (20, 0), (980, 450))
    
    #objects.append(wall)
    objects.append(spr2)
    objects.append(spr3)
    
    collisions.append(colis1)
    collisions.append(colis2)
    collisions.append(colis3)
    collisions.append(colis4)
    
    obj1 = Sc.Figure('rect', G.BLACK, (500, 60, 80, 60, 30))
    lab1 = Sc.PlayLabel('you can escape ->', (200, 400), G.BLACK, 30)
    lab2 = Sc.PlayLabel('you can go here ->', (200, 10), G.BLACK, 30)
    lab3 = Sc.PlayLabel('OMG Luna', (790, 200), G.BLACK, 30)
    spr1 = Sc.Sprite(textures[0], (800, 350), (100,100))
    anspr1 = Sc.AnimatedSprite(Sc.give_list_an(animations[0]), 4, False, (700, 385), (140,70))
    anspr2 = Sc.AnimatedSprite(Sc.give_list_an(animations[1]), 4, True, (600, 385), (140,70))
    objects.append(obj1)
    objects.append(lab1)
    objects.append(lab2)
    objects.append(lab3)
    objects.append(spr1)
    objects.append(anspr1)
    objects.append(anspr2)
    
    ar1 = Sc.Area(800, 400, (40, 60), Sc.go_in_btl, (1))
    ar2 = Sc.Area(500, 400, (60, 60), Sc.create_checktext, ('press [E] to change scene', (400, 300), G.BLACK, 30, pg.K_e, Sc.change_scene, None), Sc.delete_obj)
    areas.append(ar1)
    areas.append(ar2)
    if flip:
        objects, areas, collisions = Sc.flip_all(objects, areas, collisions, length)
    """
class CollisionShape():
    def __init__(self, x , y, size):
        self.x = x
        self.y = y
        self.rect = pg.Rect((x, y, size[0], size[1]))
        self.size = size
    def is_collide(self, rec):
        return(self.rect.colliderect(rec))
    def change_size(self, size):
        self.size = tuple(size)
        self.rect = pg.Rect((self.x, self.y, size[0], size[1]))
    def push_on(self, rec, vel):
        y1, y2 = self.y - rec.height, self.y + self.rect.height
        if vel > 0 :
            return(y1)
        else:
            return(y2)
    def draw(self):
        pg.draw.rect(screen, G.BLUE, self.rect)    
        return(screen)
class Figure():
    def __init__(self, fig, color, parameters,x = 0, y = 0):
        self.fig = fig
        self.x = parameters[0]
        self.y = parameters[1]
        self.color = color
        self.parameters = parameters
    def draw(self):
        if self.fig == 'rect':
            a, b, w, h, r = self.parameters
            pg.draw.rect(screen, self.color, (self.x, self.y, w, h), r)
        elif self.fig == 'circle':
            pg.draw.circle(screen, self.color, self.parameters)
        elif self.fig == 'polygon':
            pg.draw.polygon(screen, self.color, self.parameters)
class Area():
    def __init__(self, x , y, size, signal, p1 = None, signal_ex = None, p2 = None):
        self.x = x
        self.y = y
        self.size = tuple(size)
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
    def change_size(self, size):
        self.size = tuple(size)
        self.rect = pg.Rect((self.x, self.y, self.size[0], self.size[1]))
    def draw(self):
        pg.draw.rect(screen, G.GREEN, self.rect)    
class PlayLabel():
    def __init__(self, text,  pos, color, font):
        self.x, self.y = pos
        self.font = pg.font.SysFont("Arial", font)
        self.color = color
        self.text = text
        Text = self.font.render(text, 1, pg.Color("White"))
        self.size = Text.get_size()
    def draw(self):
        text = self.font.render(self.text, True, self.color)        
        change_screen.blit(text, (self.x, self.y))
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
class Sprite(pg.sprite.DirtySprite):
    def __init__(self, texture, pos, size = None):
        pg.sprite.Sprite.__init__(self)
        self.texture = texture
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
        pass
    def change_size(self, size):
        self.size = tuple(size)
        self.image = pg.image.load(self.texture)
        self.image = pg.transform.scale(
            self.image, (self.size[0], self.size[1]))
        self.rect = pg.Rect(self.x, self.y, size[0], size[1])
        pg.sprite.Sprite.__init__(self)
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
            change_screen.blit(self.image, self.rect)
        else:
            self.image = pg.image.load(self.images[-1])
            self.image = pg.transform.scale(
                self.image, (self.size[0], self.size[1]))   
            change_screen.blit(self.image, self.rect)
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
    number, way = param
    from draw import change_scene as change
    change(number, way)
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
def flip_all(obj, ar, col, sprites, length):
    for i in obj:
        if type(i) == PlayLabel:
            i.x = length - i.x - i.size[0]
        elif type(i) == Figure :
            if i.fig == 'rect':
                i.x = length - i.x - i.parameters[2]
            elif i.fig == 'polygon':
                new_param = []
                for j in range(len(i.parameters)):
                    new_param.append((length -i.parameters[j][0],  i.parameters[j][1]))
                i.parameters = tuple(new_param)
    for i in ar:
        i.x = length - i.x  - i.rect.width
        i.change_size(i.size)
    for i in col:
        i.x = length - i.x  - i.rect.width
        i.change_size(i.size)
    for i in sprites.values():
        i.x = length - i.x - i.rect.width
        i.change_size(i.size)
        i.change_size(i.size)
    return(obj, ar, col, sprites)