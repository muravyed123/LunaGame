import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
def start():
    colis1 = Sc.CollisionShape(700, 300, (80, 60))
    collisions.append(colis1)
def get_scene():
    for i in collisions:
        screen.blit(i.draw(),(0,0))
    for i in objects:
        screen.blit(i.draw(),(0,0))
    for i in areas:
        screen.blit(i.draw(),(0,0))
    return(screen)
def update(player, pl, vel):
    r1, r2 = pl.move_x(vel[0]), pl.move((-vel[0], vel[1]))
    r3 = pl.move((vel[0] ,0))
    for i in collisions:
        if i.is_collide(r1): 
            vel[0] = 0
        if i.is_collide(r2):
            player.push(i.push_on(r3))
            vel[1] = 0
    for i in areas:
        res, signal = i.is_collide(r3)
        if res:
            signal()
    return vel