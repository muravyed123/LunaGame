import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
sprites = {}
keys = []
sprite_group = pg.sprite.Group()

flip_scene = 1
flip = True
length = 3000
start_position = [(100,680), (length -200, 680)]
textures = ["materials/floor.png", 'materials/table.png', 'materials/sofa.png', 'materials/box.png',
            'materials/armchair.png', 'materials/window.png', 'materials/door1.png', 'materials/flower.png',
            'materials/flower2.png', 'materials/tree.png', 'materials/turnstile.png', 'materials/exit.png',
            'materials/board_pl.png', 'materials/plakat3.png', 'materials/mirror.png']

def clear():
    global collisions, objects, areas, sprites, keys
    collisions = []
    objects =[]
    areas = []
    sprites = {}
    keys = []
    draw_only()
def start():
    global keys
    wall = Sc.Figure('rect', (156, 224, 180), (0, 0, 3000, 600, 300))
    wall2 = Sc.Figure('rect', (156, 224, 161), (0, 0, 200, 700, 140))
    wall3 = Sc.Figure('rect', G.BLACK, (0, -5, 200, 710, 5))
    wall4 = Sc.Figure('rect', (156, 224, 161), (1250, 0, 500, 640, 260))
    wall5 = Sc.Figure('rect', G.BLACK, (1250, -5, 500, 650, 5))
    wall6 = Sc.Figure('polygon', (136, 224, 161), ((1180, 460), (1250, 640), (1250, 0 ), (1180, 0)))
    shelf = Sc.Figure('rect', (94, 81, 60), (500, 370, 400, 320, 100))
    table2 = Sc.Sprite(textures[1], (2245, 279), (500, 500))
    start_pos = -170
    leng = 611
    floor1 = Sc.Sprite(textures[0], (start_pos, 582), (864, 350))
    floor2 = Sc.Sprite(textures[0], (start_pos + leng * 1, 582), (864, 350))
    floor3 = Sc.Sprite(textures[0], (start_pos + leng * 2, 582), (864, 350))
    floor4 = Sc.Sprite(textures[0], (start_pos + leng * 3, 582), (864, 350))
    floor5 = Sc.Sprite(textures[0], (start_pos + leng * 4, 582), (864, 350))
    floor6 = Sc.Sprite(textures[0], (1000, 518), (800, 200))
    floor7 = Sc.Sprite(textures[0], (600, 518), (800, 200))
    floor8 = Sc.Sprite(textures[0], (200, 518), (800, 200))
    door1 = Sc.Sprite(textures[6], (1200, -20), (500, 700))
    door2 = Sc.Sprite(textures[6], (2605, -40), (540, 700))
    door3 = Sc.Sprite(textures[6], (1710, -45), (595, 700))
    #door2 = Sc.Sprite(textures[6], (1800, 20), (500, 700))
    window = Sc.Sprite(textures[5], (900, 100), (300, 270))
    window2 = Sc.Sprite(textures[5], (470, 100), (300, 270))
    window3 = Sc.Sprite(textures[5], (340, 100), (300, 270))
    sofa = Sc.Sprite(textures[2], (450, 299), (500, 400))
    table = Sc.Sprite(textures[1], (540, 344), (395, 400))
    box = Sc.Sprite(textures[3], (70, 134), (385, 645))
    armch = Sc.Sprite(textures[4], (900, 399), (350, 330))
    flower1 = Sc.Sprite(textures[7], (350, 199), (200, 170))
    flower2 = Sc.Sprite(textures[8], (750, 229), (200, 170))
    flower3 = Sc.Sprite(textures[9], (490, 0), (300, 470))
    trn = Sc.Sprite(textures[10], (1500, 335), (500, 425))
    exit = Sc.Sprite(textures[11], (1955, 365), (285, 325))
    plakat = Sc.Sprite(textures[12], (2265, 175), (300, 215))
    plakat2 = Sc.Sprite(textures[13], (2565, 200), (125, 100))
    mirror = Sc.Sprite(textures[14], (1590, 115), (125, 425))
    ar1 = Sc.Area(5, 215, (40, 410), Sc.change_scene, (6, 0))
    ar2 = Sc.Area(2955, 10, (40, 625), Sc.change_scene, (4, 1))
    sprites['floor1'] = floor1
    sprites['floor2'] = floor2
    sprites['floor3'] = floor3
    sprites['floor4'] = floor4
    sprites['floor5'] = floor5
    sprites['floor6'] = floor6
    sprites['floor7'] = floor7
    sprites['floor8'] = floor8
    sprites['window'] = window
    sprites['window2'] = window2
    sprites['window3'] = window3
    sprites['armch'] = armch
    sprites['sofa'] = sofa
    sprites['table'] = table
    sprites['table2'] = table2
    sprites['door1'] = door1
    sprites['door2'] = door2
    sprites['door3'] = door3
    sprites['flower1'] = flower1
    sprites['flower2'] = flower2
    sprites['flower3'] = flower3
    sprites['box'] = box
    sprites['trn'] = trn
    sprites['exit'] = exit
    sprites['plakat'] = plakat
    sprites['plakat2'] = plakat2
    sprites['mirror'] = mirror

    objects.append(wall)
    objects.append(wall2)
    objects.append(wall3)
    objects.append(wall4)
    objects.append(wall5)
    objects.append(wall6)
    objects.append(shelf)
    areas.append(ar1)
    areas.append(ar2)
    if flip:
        Sc.flip_all(objects, areas, collisions,sprites, length)
    for i in sprites.values():
        sprite_group.add(i)
    keys = list(sprites.keys())
    draw_only()
    wall2.draw()
    wall3.draw()
    wall4.draw()
    wall5.draw()
    wall6.draw()
    door1.draw()
    armch.draw()
    mirror.draw()


def draw_only():
    Sc.screen.fill((255,255,255))
    for i in objects:
        i.draw()
    sprite_group = pg.sprite.Group()
    for i in keys:
        sprite_group.add(sprites[i])
    for i in collisions:
        i.draw()
    sprite_group.draw(Sc.screen)
def get_scene(keys):
    screen = Sc.screen
    change_screen = Sc.change_screen
    change_screen.fill(G.WHITE)
    for i in objects:
        #i.draw()
        if type(i) == Sc.CheckText:
            i.click(keys)
    for i in collisions:
        i.draw()
    for i in areas:
        i.draw()
    #sprite_group.draw(Sc.screen)
    return(screen, change_screen)
def update(player, pl, vel):
    pl.is_on_floor = player.is_on_floor
    r1, r2 = pl.move_x(vel[0]), pl.move((-vel[0], vel[1]))
    r3 = pl.move((vel[0] ,0))
    for i in collisions:
        if i.is_collide(r1): 
            vel[0] = 0
        if i.is_collide(r2):
            player.push(i.push_on(r3, player.v_y))
            vel[1] = 0
    for i in areas:
        res, signal, param = i.is_collide(r3)
        if signal != None:
            signal(i, objects, param)
    return vel