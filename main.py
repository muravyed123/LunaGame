import pygame as pg
import sys
import menu
import draw
import json
import Sound as sound

import globalsc as G

can_pause = False
pause = False
active = True
 
clock = pg.time.Clock()
sc = pg.display.set_mode((0,0), pg.FULLSCREEN)


menu.start()
draw.change_scene(1, 1)
pg.display.set_caption('Game')
sound.start_play_fon_music(1, -1)


def save():
    savefile = {'checkpoints': draw.checkpoints, 'position': (draw.player.x, draw.player.y), 'name': G.name, 'now_scene': draw.now_scene.number}

    with open('save.json', 'w') as file:
        json.dump(savefile, file)


def load():
    with open('save.json', 'r') as json_file:
        data = json.load(json_file)
        G.give_name(data['name'])
        draw.change_checkpoints(data['checkpoints'])
        print(data['checkpoints'], data['position'])
        draw.change_scene(data['now_scene'], -1,  data['position'])
        menu.pause(False)
        menu.loading()


def clear():
    G.give_name('')
    draw.change_checkpoints([False]*8)
    # draw.change_scene(1, 2)
    menu.pause(False)
    menu.loading()


menu.start_menu()


def unpause():
    global pause
    pause = False
    menu.pause(pause)


while active:
    clock.tick(G.FPS)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            sys.exit()
            
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        if can_pause and menu.can_return and not draw.in_battle:
            pause = not pause
            can_pause = False
            menu.pause(pause)
    else:
        can_pause = True
    sc.fill(G.WHITE)
    if not pause and menu.now_active:
        sc.blit(draw.update(events, keys), (0, 0))
    sc.blit(menu.update(events, keys), (0, 0))
    pg.display.update()


def exit_pr():
    # active = False
    sys.exit()