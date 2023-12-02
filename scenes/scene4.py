import pygame as pg
import sys

sys.path.append('..')
import globalsc as G
import Scene_class as Sc

collisions = []
objects = []
areas = []
screen = pg.Surface((G.WIDTH, G.HEIGHT), G.WHITE)
flip_scene = 3
sprites = {}
sprite_group = pg.sprite.Group()
keys = []
flip = True
length = 3000

textures = ["materials/floor.png", 'materials/kitchen.png', 'materials/door3.png', 'materials/firebox.png',
            'materials/box2.png', 'materials/evacuation.png', 'materials/window.png']
animations = ['Animations/bl_cat_go', 'Animations/bl_cat_sit']
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
    wall = Sc.Figure('rect', (156, 224, 161), (0, 0, 3000, 600, 350))
    bord = Sc.Figure('rect', (102, 84, 63), (0, 350, 3000, 70, 35))
    objects.append(wall)
    objects.append(bord)
    start_pos = -138
    leng = 611
    floor1 = Sc.Sprite(textures[0], (start_pos, 582), (864, 350))
    floor2 = Sc.Sprite(textures[0], (start_pos + leng * 1, 582), (864, 350))
    floor3 = Sc.Sprite(textures[0], (start_pos + leng * 2, 582), (864, 350))
    floor4 = Sc.Sprite(textures[0], (start_pos + leng * 3, 582), (864, 350))
    floor5 = Sc.Sprite(textures[0], (start_pos + leng * 4, 582), (864, 350))
    door1 = Sc.Sprite(textures[2], (475, 0), (340, 630))
    kitchen = Sc.Sprite(textures[1], (1540, -145), (835, 775))
    evac = Sc.Sprite(textures[5], (1055, 170), (210, 145))
    window = Sc.Sprite(textures[6], (1730, 35), (425, 235))
    colis1 = Sc.CollisionShape(2800, 160, (85, 625))
    box = Sc.Sprite(textures[3], (835, 215), (200, 185))
    box2 = Sc.Sprite(textures[4], (2745, 55), (310, 750))
    ar2 = Sc.Area(55, 65, (40, 625), Sc.change_scene, (2, 0))
    sprites['floor1'] = floor1
    sprites['floor2'] = floor2
    sprites['floor3'] = floor3
    sprites['floor4'] = floor4
    sprites['floor5'] = floor5
    sprites['door1'] = door1
    sprites['evac'] = evac
    sprites['box'] = box
    sprites['box2'] = box2
    sprites['kitchen'] = kitchen
    sprites['window'] = window
    collisions.append(colis1)
    #areas.append(ar1)
    areas.append(ar2)
    if flip:
        Sc.flip_all(objects, areas, collisions,sprites, length)
    for i in sprites.values():
        sprite_group.add(i)
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