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

flip_scene = 1
flip = True
length = 3000
start_position = (2500,680)
textures = ["materials\kfloor.png", 'materials\ktable.png', 'materials\sofa.png', 'materials\kbox.png',
            'materials\karmchair.png', 'materials\window.png', 'materials\door1.png']

def clear():
    global collisions, objects, areas
    collisions = []
    objects =[]
    areas = []
    draw_only()
def start():
    wall = Sc.Figure('rect', (156, 224, 180), (0, 0, 3000, 525, 300))
    wall2 = Sc.Figure('rect', (156, 224, 161), (0, 0, 200, 700, 140))
    wall3 = Sc.Figure('rect', G.BLACK, (0, -5, 200, 710, 5))
    wall4 = Sc.Figure('rect', (156, 224, 161), (1400, 0, 500, 700, 260))
    wall5 = Sc.Figure('rect', G.BLACK, (1400, -5, 500, 710, 5))
    wall6 = Sc.Figure('polygon', (136, 224, 161), ((1300, 520), (1400, 700), (1400, 0 ), (1300, 0)))
    table2 = Sc.Sprite(textures[1], (2300, 209), (700, 600))
    start_pos = -138
    leng = 611
    floor1 = Sc.Sprite(textures[0], (start_pos, 582), (864, 350))
    floor2 = Sc.Sprite(textures[0], (start_pos + leng * 1, 582), (864, 350))
    floor3 = Sc.Sprite(textures[0], (start_pos + leng * 2, 582), (864, 350))
    floor4 = Sc.Sprite(textures[0], (start_pos + leng * 3, 582), (864, 350))
    floor5 = Sc.Sprite(textures[0], (start_pos + leng * 4, 582), (864, 350))
    floor6 = Sc.Sprite(textures[0], (1000, 518), (800, 200))
    floor7 = Sc.Sprite(textures[0], (600, 518), (800, 200))
    floor8 = Sc.Sprite(textures[0], (200, 518), (800, 200))
    door1 = Sc.Sprite(textures[6], (1450, 50), (500, 700))
    #door2 = Sc.Sprite(textures[6], (1800, 20), (500, 700))
    window = Sc.Sprite(textures[5], (850, 100), (400, 270))
    window2 = Sc.Sprite(textures[5], (370, 100), (400, 270))
    sofa = Sc.Sprite(textures[2], (450, 299), (500, 400))
    table = Sc.Sprite(textures[1], (500, 359), (500, 400))
    box = Sc.Sprite(textures[3], (40, 99), (500, 600))
    armch = Sc.Sprite(textures[4], (950, 419), (300, 270))
    sprites.append(floor1)
    sprites.append(floor2)
    sprites.append(floor3)
    sprites.append(floor4)
    sprites.append(floor5)
    sprites.append(floor6)
    sprites.append(floor7)
    sprites.append(floor8)
    sprites.append(window)
    sprites.append(window2)
    sprites.append(armch)
    sprites.append(sofa)
    sprites.append(table)
    sprites.append(table2)
    sprites.append(door1)
    sprites.append(box)

    objects.append(wall)
    objects.append(wall2)
    objects.append(wall3)
    objects.append(wall4)
    objects.append(wall5)
    objects.append(wall6)
    if flip:
        Sc.flip_all(objects, areas, collisions,sprites, length)
    for i in sprites:
        sprite_group.add(i)
    draw_only()
    wall2.draw()
    wall3.draw()
    wall4.draw()
    wall5.draw()
    wall6.draw()
    door1.draw()
    

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