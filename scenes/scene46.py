import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
flip_scene = 45
sprites = {}
sprite_group = pg.sprite.Group()
keys = []
flip = True
length = 3000

textures = ["materials/floor.png", 'materials/door2.png', 'materials/door3.png', 'materials/door5.png',
            'materials/door6.png', 'materials/door7.png', 'materials/door8.png']

animations = ['Animations/bl_cat_go', 'Animations/bl_cat_sit']
start_position = [(200, 680), (length -200, 680)]
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
    wall = Sc.Figure('rect', (156, 224, 161), (0, 0, 3000, 600, 350))
    bord = Sc.Figure('rect', (102, 84, 63), (0, 350, 3000, 70, 35))
    start_pos = -170
    leng = 611
    objects.append(wall)
    objects.append(bord)
    floor1 = Sc.Sprite(textures[0], (start_pos, 582), (864, 350))
    floor2 = Sc.Sprite(textures[0], (start_pos + leng * 1, 582), (864, 350))
    floor3 = Sc.Sprite(textures[0], (start_pos + leng * 2, 582), (864, 350))
    floor4 = Sc.Sprite(textures[0], (start_pos + leng * 3, 582), (864, 350))
    floor5 = Sc.Sprite(textures[0], (start_pos + leng * 4, 582), (864, 350))
    ar2 = Sc.Area(15, 65, (40, 625), Sc.change_scene, (42, 0))
    colis1 = Sc.CollisionShape(2970, 180, (100, 510))
    door1 = Sc.Sprite(textures[4], (2445, 55), (280, 550))
    door2 = Sc.Sprite(textures[1], (110, -35), (560, 690))
    door3 = Sc.Sprite(textures[6], (1710, 50), (305, 560))
    door4 = Sc.Sprite(textures[3], (980, 40), (345, 565))
    sprites['floor1'] = floor1
    sprites['floor2'] = floor2
    sprites['floor3'] = floor3
    sprites['floor4'] = floor4
    sprites['floor5'] = floor5
    sprites['door1'] = door1
    sprites['door2'] = door2
    sprites['door3'] = door3
    sprites['door4'] = door4
    areas.append(ar2)
    collisions.append(colis1)
    keys = list(sprites.keys())
    if flip:
        Sc.flip_all(objects, areas, collisions,sprites, length)
    draw_only()
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