import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
flip_scene = 1
sprites = []
sprite_group = pg.sprite.Group()
flip = True
length = 3000
start_position = (500,680)

textures = []
animations = ['Animations/bl_cat_go', 'Animations/bl_cat_sit']
start_position = (1500,680)
def clear():
    global collisions, objects, areas
    collisions = []
    objects =[]
    areas = []
    draw_only
def start():
    wall = Sc.Figure('rect', (156, 224, 161), (0, 0, 3000, 400, 350))
    objects.append(wall)
    draw_only()

def draw_only():
    Sc.screen.fill((255,255,255))
    for i in objects:
        i.draw()
    sprite_group.draw(Sc.screen)
def get_scene(keys):
    screen = Sc.screen
    change_screen = Sc.change_screen
    change_screen.fill(G.WHITE)
    screen.blit(change_screen, (0,0))
    for i in objects:
        #i.draw()
        if type(i) == Sc.CheckText:
            i.click(keys)
    for i in collisions:
        i.draw()
    for i in areas:
        i.draw()
    #sprite_group.draw(Sc.screen)
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