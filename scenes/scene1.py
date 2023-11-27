import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)

textures = ['materials\Luna.jpg', 'materials\door.jpg', 'materials\wall1.jpg']
animations = ['Animations/bl_cat_go', 'Animations/bl_cat_sit']
def start():
    global collisions
    colis1 = Sc.CollisionShape(0, 0, (20, 460))
    colis2 = Sc.CollisionShape(1000, 0, (20, 460))
    colis3 = Sc.CollisionShape(300, 250, (60, 60))
    colis4 = Sc.CollisionShape(500, 60, (80, 60))
    
    spr2 = Sc.Sprite(textures[1], (700, 200), (100, 250))
    spr3 = Sc.Sprite(textures[1], (300, 200), (100, 250))
    wall = Sc.Sprite(textures[2], (20, 0), (980, 450))
    
    objects.append(wall)
    objects.append(spr2)
    objects.append(spr3)
    
    collisions.append(colis1)
    collisions.append(colis2)
    collisions.append(colis3)
    collisions.append(colis4)
    
    obj1 = Sc.Object('rect', G.BLACK, (500, 60, 80, 60))
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
    
    ar1 = Sc.Area(800, 0, (40, 60), Sc.change_scene)
    ar2 = Sc.Area(500, 400, (60, 60), Sc.create_checktext, ('press [E] to change scene', (400, 300), G.BLACK, 30, pg.K_e, Sc.change_scene, None), Sc.delete_obj)
    areas.append(ar1)
    areas.append(ar2)
def get_scene(keys):
    screen = Sc.screen
    screen.fill(G.WHITE)
    for i in collisions:
        i.draw()
    for i in objects:
        i.draw()
        if type(i) == Sc.CheckText:
            i.click(keys)
    for i in areas:
        i.draw()
    return(screen)
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