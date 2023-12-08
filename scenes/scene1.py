import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
sprites = {}
sprite_group = pg.sprite.Group()
keys = []

flip_scene = 2
flip = False
length = 3000
start_position = [(100,680), (length - 200, 680), (1500, 680)]

textures = ["materials/floor.png", 'materials/table3.png', 'materials/board.png', 'materials/firebox.png',
            'materials/door1.png', 'materials/door2.png', 'materials/table2.png', 'materials/plakat.png', 'materials/plak2.png']
animations = ['Animations/luna_go', 'Animations/luna_sit']
def clear():
    global collisions, objects, areas, sprites,keys
    collisions = []
    objects =[]
    areas = []
    sprites = {}
    keys = []
    draw_only()
def start():
    global keys
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
    colis1 = Sc.CollisionShape(1575, 410, (855, 75))
    #colis2 = Sc.CollisionShape(2030, 410, (405, 75))
    table = Sc.Sprite(textures[1], (1490, 219), (695, 605))
    table2 = Sc.Sprite(textures[1], (1940, 219), (690, 610))
    firebox = Sc.Sprite(textures[3], (270, 200), (200, 200))
    door1 = Sc.Sprite(textures[4], (595, -50), (500, 700))
    door2 = Sc.Sprite(textures[5], (390, -50), (500, 700))
    door3 = Sc.Sprite(textures[5], (2640, -50), (500, 700))
    plak1 = Sc.Sprite(textures[7], (1290, 195), (325, 205))
    plak2 = Sc.Sprite(textures[8], (1130, 175), (160, 200))
    ar1 = Sc.Area(5, 215, (40, 410), Sc.change_scene, (5, 1))
    ar2 = Sc.Area(2955, 10, (40, 625), Sc.change_scene, (3, 0))
    ar3 = Sc.Area(1400, 630, (40, 100), Sc.create_animated_object, (Sc.give_list_an(animations[0]), 5, True,
                        (180, 180), (0, 570), Sc.give_list_an(animations[1]), 10, True, (150, 150), (1100, 580), 4,
                        G.create_dialog, (0, G.remove_checkpoint, (0, 'delete_last')), True))
    areas.append(ar1)
    areas.append(ar2)
    from draw import checkpoints as ch
    if not ch[0]:
        areas.append(ar3)
    objects.append(wall)
    sprites['floor1'] = floor1
    sprites['floor2'] = floor2
    sprites['floor3'] = floor3
    sprites['floor4'] = floor4
    sprites['floor5'] = floor5
    objects.append(bord)
    sprites['table'] = table
    sprites['table2'] = table2
    sprites['board'] = board
    sprites['firebox'] = firebox
    sprites['door1'] = door1
    sprites['door2'] = door2
    sprites['door3'] = door3
    sprites['plak1'] = plak1
    sprites['plak2'] = plak2
    collisions.append(colis1)
    #collisions.append(colis2)
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
    for i in areas:
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
        if signal != None:
            signal(i, objects, param)
    return vel