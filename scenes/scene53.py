import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
flip_scene = None
sprites = {}
sprite_group = pg.sprite.Group()
keys = []
flip = False
length = 1700

textures = ["materials/floor.png", "materials/stairpr.png"]

animations = ['Animations/luna_sit', 'materials/ghost.png']
start_position = [(200, 680), (length -200, 680), (800, 680)]
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
    wall = Sc.Figure('rect', (249, 166, 236), (0, 0, 1800, 600, 350))
    floor  = Sc.Figure('rect', (249, 230, 236), (0, 0, 1800, 600, 350))
    objects.append(floor)
    objects.append(wall)
    Luna = Sc.AnimatedSprite(Sc.give_list_an(animations[0]), 5, True,
                        (180, 180), (905, 167), (160, 160))

    wash1 = Sc.Sprite(textures[1], (505, 30), (740, 555))
    objects.append(Luna)
    #sprites['floor4'] = floor4
    sprites['wash1'] = wash1
    keys = list(sprites.keys())
    Sc.create_dialog(None,None, (2, G.end_game, ((0,0)), False))
    Luna.draw()
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
        from draw import change_activity as ch
        ch(False)
        if type(i) == Sc.AnimatedSprite:
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
        if signal != None and signal != True:
            if signal == G.create_dialog:
                signal(param)
            else:
                signal(i, objects, param)
    return vel