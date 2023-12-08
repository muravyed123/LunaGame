import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
flip_scene = 8
sprites = {}
sprite_group = pg.sprite.Group()
keys = []
flip = False
length = 1700

textures = ["materials/floor.png", "materials/washma.png"]

animations = ['Animations/bl_cat_go', 'materials/ghost.png']
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
    wall = Sc.Figure('rect', (217, 218, 185), (0, 0, 1800, 600, 350))
    start_pos = -138
    leng = 611
    objects.append(wall)
    floor1 = Sc.Sprite(textures[0], (start_pos, 582), (864, 350))
    floor2 = Sc.Sprite(textures[0], (start_pos + leng * 1, 582), (864, 350))
    floor3 = Sc.Sprite(textures[0], (start_pos + leng * 2, 582), (864, 350))
    floor4 = Sc.Sprite(textures[0], (start_pos + leng * 3, 582), (864, 350))
    colis1 = Sc.CollisionShape(1420, 160, (85, 625))
    ar1 = Sc.Area(0, 65, (40, 625), Sc.change_scene, (7, 2))
    ar3 = Sc.Area(560, 630, (40, 100), Sc.create_animated_object, (
    [animations[1]], 5, False, (180, 180), (1700, 580), [animations[1]], 10, True, (150, 150),
    (600, 580), 15, Sc.go_in_btl, (2), False))
    areas.append(ar1)
    ar4 = Sc.Area(200, 630, (40, 100),Sc.create_dialog,(1, G.remove_checkpoint, (2, 'nothing'), True))
    from draw import checkpoints as ch
    if not ch[1] and ch[0]:
        areas.append(ar3)
    if not ch[2] and ch[1]:
        areas.append(ar4)
    areas.append(ar4)
    wash1 = Sc.Sprite(textures[1], (965, 165), (565, 555))
    wash2 = Sc.Sprite(textures[1], (480, 165), (550, 560))
    wash3 = Sc.Sprite(textures[1], (15, 165), (550, 545))
    sprites['floor1'] = floor1
    sprites['floor2'] = floor2
    sprites['floor3'] = floor3
    #sprites['floor4'] = floor4
    sprites['wash1'] = wash1
    sprites['wash2'] = wash2
    sprites['wash3'] = wash3
    collisions.append(colis1)
    keys = list(sprites.keys())
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
        if type(i) == Sc.CheckText:
            i.click(keys)
            i.draw()
        if type(i) == Sc.KinematicBody:
            i.move()
            i.draw()
            if i.die:
                del objects[objects.index(i)]
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
        if signal != None and signal != True:
            if signal == G.create_dialog:
                signal(param)
            else:
                signal(i, objects, param)
    return vel