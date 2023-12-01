import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
sprites = []
sprite_group = pg.sprite.Group()

flip_scene = 2
flip = False
length = 3000
start_position = (1500,680)

textures = ["materials\kfloor.png", 'materials\ktable.png', 'materials\kboard.png', 'materials\kfirebox.png', 'materials\door1.png', 'materials\door2.png']
animations = ['Animations/bl_cat_go', 'Animations/bl_cat_sit']
def clear():
    global collisions, objects, areas
    collisions = []
    objects =[]
    areas = []
    draw_only()
def start():
    wall = Sc.Figure('rect', (156, 224, 161) , (0, 0, 3000, 600, 350))
    bord = Sc.Figure('rect', (102, 84, 63), (0,350, 3000, 70, 35))
    start_pos = -138
    leng = 611
    floor1 = Sc.Sprite(textures[0], (start_pos, 582),(864, 350))
    floor2 = Sc.Sprite(textures[0], (start_pos + leng * 1, 582),(864, 350))
    floor3 = Sc.Sprite(textures[0], (start_pos + leng * 2, 582),(864, 350))
    floor4 = Sc.Sprite(textures[0], (start_pos + leng * 3, 582), (864, 350))
    floor5 = Sc.Sprite(textures[0], (start_pos + leng * 4, 582), (864, 350))
    board = Sc.Sprite(textures[2], (1500, 100), (900, 300))
    colis1 = Sc.CollisionShape(1680, 455, (520, 20))
    table = Sc.Sprite(textures[1], (1600, 219), (700, 600))
    firebox = Sc.Sprite(textures[3], (1200, 200), (200, 200))
    door1 = Sc.Sprite(textures[4], (400, -50), (500, 700))
    door2 = Sc.Sprite(textures[5], (200, -50), (500, 700))
    door3 = Sc.Sprite(textures[5], (2600, -50), (500, 700))
    objects.append(wall)
    sprites.append(floor1)
    sprites.append(floor2)
    sprites.append(floor3)
    sprites.append(floor4)
    sprites.append(floor5)
    objects.append(bord)
    sprites.append(table)
    sprites.append(board)
    sprites.append(firebox)
    sprites.append(door1)
    sprites.append(door2)
    sprites.append(door3)
    for i in sprites:
        sprite_group.add(i)
    collisions.append(colis1)
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