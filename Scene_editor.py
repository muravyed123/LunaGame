import importlib
import sys

import pygame as pg

import globalsc as G

import Scene_class as Sc
object_move = False
now_object = None
now_key = ''
coords = (0, 0)
speed = 10
number = 53
scene = importlib.import_module(f'scenes.scene{number}')
active = True

clock = pg.time.Clock()
text = ''
sc = pg.display.set_mode((0, 0), pg.FULLSCREEN)
scene.start()
pg.font.init()
def find_object(coords):
    global text, now_key
    #if scene.flip:
        #coords = (scene.length - coords[0],- coords[1])
    for i in scene.collisions:
        if i.rect.collidepoint(coords):
            text = 'Collision'
            return i
    for i in scene.areas:
        if i.rect.collidepoint(coords):
            text = 'Area'
            return i
    for i in scene.keys[::-1]:
        if scene.sprites[i].rect.collidepoint(coords):
            text = i
            now_key = i
            return scene.sprites[i]
    return None
def save():
    save_text = 'SPRITES: \n'
    for i in scene.keys:
        r = scene.sprites[i].rect
        if not scene.flip:
            save_text += (i + ':  (' + str(r.x) + ', ' + str(r.y) + '), (' + str(r.width) + ', ' + str(r.height) + ')' + '\n')
        else:
            save_text += (i + ':  (' + str(scene.length - r.x - r.width) + ', ' + str(r.y) + '), (' + str(r.width) + ', ' + str(
                r.height) + ')' + '\n')
    save_text += 'COLLISIONS: \n'
    for i in scene.collisions:
        r = i.rect
        if not scene.flip:
            save_text += str(r.x) + ', ' + str(r.y) + ', (' + str(r.width) +', ' + str(r.height) + ')\n'
        else:
            save_text += str(scene.length - r.x - r.width) + ', ' + str(r.y) + ', (' + str(r.width) + ', ' + str(r.height) + ')\n'
    save_text += 'AREAS: \n'
    for i in scene.areas:
        r = i.rect
        if not scene.flip:
            save_text += str(r.x) + ', ' + str(r.y) + ', (' + str(r.width) + ', ' + str(r.height) + ')\n'
        else:
            save_text += str(scene.length - r.x - r.width) + ', ' + str(r.y) + ', (' + str(r.width) + ', ' + str(
                r.height) + ')\n'
    file = open('Savefile.txt', 'w')
    file.write(save_text)
while active:
    clock.tick(G.FPS)
    events = pg.event.get()

    keys = pg.key.get_pressed()
    vel = [0,0]
    size = [0,0]
    layer = 0
    if keys[pg.K_LEFT]:
        vel[0] += 1
    if keys[pg.K_RIGHT]:
        vel[0] -= 1
    if keys[pg.K_UP]:
        vel[1] += 1
    if keys[pg.K_DOWN]:
        vel[1] -= 1
    if keys[pg.K_w]:
        size[1] += 1
    if keys[pg.K_s]:
        size[1] -= 1
    if keys[pg.K_a]:
        size[0] -= 1
    if keys[pg.K_d]:
        size[0] += 1
    if keys[pg.K_ESCAPE]:
        sys.exit()
    if keys[pg.K_j]:
        save()
    if keys[pg.K_RSHIFT]:
        speed = 50
    else:
        speed = 5
    if keys[pg.K_9]:
        layer += 1
    elif keys[pg.K_0]:
        layer -= 1
    if not object_move:
        coords = (coords[0] + vel[0] * speed, coords[1] + vel[1] * speed)
    else:
        if now_object != None:
            if now_object.x + coords[0] > G.WIDTH - 100:
                coords = (coords[0] - G.WIDTH // 2, coords[1])
            elif now_object.x + coords[0] < -100:
                coords = (coords[0] + G.WIDTH // 2, coords[1])
            now_object.x -= vel[0] * speed
            if type(now_object) == Sc.Sprite:
                index = scene.keys.index(now_key) + layer
                if index >= 0 and index < len(scene.keys):
                    scene.keys[index], scene.keys[index - layer] = scene.keys[index - layer], scene.keys[index]
            now_object.y -= vel[1] * speed
            now_object.change_size([now_object.size[0] + size[0] * 5, now_object.size[1] + size[1] * 5])
            scene.draw_only()
    sc.fill(G.WHITE)
    sc.blit(scene.get_scene(keys)[0], coords)
    for event in events:
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                now_object = find_object((event.pos[0] - coords[0], event.pos[1] - coords[1]))
                if now_object != None:
                    object_move = True
            elif event.button == 3:
                text = ''
                now_object = None
                object_move = False
        if event.type == pg.MOUSEMOTION:
            if not scene.flip:
                pg.draw.circle(sc, G.BLACK, event.pos, 10)
    font = pg.font.SysFont("Arial", 30)
    Text = font.render(text, 1, pg.Color("Black"))
    sc.blit( Text, (0,100))
    pg.display.update()