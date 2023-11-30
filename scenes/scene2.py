import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
textures = []

screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
def clear():
    pass
def start():    
    colis1 = Sc.CollisionShape(700, 300, (80, 60))
    collisions.append(colis1)
    
    spr1 = Sc.Sprite('materials\cucaracha.png', (100, 300), (200, 150))
    objects.append(spr1)
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