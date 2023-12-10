import pygame as pg
music = ['music/firfloorfon.mp3', 'music/menu.mp3', 'music/Кухня.mp3', 'music/ghost.mp3', 'music/eva.mp3', 'music/Lastbye.mp3']
now_music = -1
def start_play_fon_music(number, count):
    global now_music
    if str(number) == 'nothing':
        pg.mixer.music.stop()
        now_music = -1
        return None
    if now_music != number:
        pg.mixer.music.load(music[number])
        pg.mixer.music.play(count)
        now_music = number
def pause(pause):
    if pause:
        pg.mixer.music.pause()
    else:
        pg.mixer.music.unpause()
def set_volume(c):
    pg.mixer.music.set_volume(c/100)
pg.mixer.music.set_volume(0)