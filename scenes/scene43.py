import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
flip_scene = 44
sprites = {}
sprite_group = pg.sprite.Group()
keys = []
flip = False
length = 3000

textures = ["materials/floor.png", 'materials/door2.png', 'materials/door3.png', 'materials/door5.png',
            'materials/door6.png', 'materials/stairs.png', 'materials/door10.png']

animations = ['Animations/bl_cat_go', 'Animations/bl_cat_sit']
start_position = [(200, 680), (length -200, 680), (1000, 680)]
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
    wall2 = Sc.Figure('rect', (255, 255, 255), (778, 0, 254, 320, 350))
    bord = Sc.Figure('rect', (102, 84, 63), (0, 350, 3000, 70, 35))
    start_pos = -138
    leng = 611
    objects.append(wall)
    objects.append(bord)
    objects.append(wall2)
    label = Sc.PlayLabel('5 ЭТАЖ', (500, 50), (100, 0, 0), 50)
    objects.append(label)
    floor1 = Sc.Sprite(textures[0], (start_pos, 582), (864, 350))
    floor2 = Sc.Sprite(textures[0], (start_pos + leng * 1, 582), (864, 350))
    floor3 = Sc.Sprite(textures[0], (start_pos + leng * 2, 582), (864, 350))
    floor4 = Sc.Sprite(textures[0], (start_pos + leng * 3, 582), (864, 350))
    floor5 = Sc.Sprite(textures[0], (start_pos + leng * 4, 582), (864, 350))
    stairs = Sc.Sprite(textures[5], (770, -20), (535, 630))
    ar1 = Sc.Area(830, 335, (170, 410), Sc.create_checktext,
                  ('Нажмите Т чтобы спуститься по ступеням', (1055, 400), G.BLACK, 50, pg.K_t, Sc.change_scene, (33, 2)),
                  Sc.delete_obj)
    ar2 = Sc.Area(10, 65, (40, 625), Sc.change_scene, (47, 1))
    ar3 = Sc.Area(2930, 65, (40, 625), Sc.change_scene, (39, 0))
    door1 = Sc.Sprite(textures[2], (95, 15), (345, 620))
    door2 = Sc.Sprite(textures[4], (2415, 50), (290, 550))
    door3 = Sc.Sprite(textures[6], (1660, 45), (275, 560))
    door4 = Sc.Sprite(textures[6], (1030, -15), (270, 625))
    sprites['floor1'] = floor1
    sprites['floor2'] = floor2
    sprites['floor3'] = floor3
    sprites['floor4'] = floor4
    sprites['floor5'] = floor5
    sprites['door1'] = door1
    sprites['door2'] = door2
    sprites['door3'] = door3
    sprites['stairs'] = stairs
    sprites['door4'] = door4
    areas.append(ar2)
    areas.append(ar3)
    areas.append(ar1)
    keys = list(sprites.keys())
    draw_only()
    wall2.draw()
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
        if type(i) == Sc.CheckText:
            i.click(keys)
            i.draw()
        elif type(i) == Sc.PlayLabel:
            i.draw()
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