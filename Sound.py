import pygame as pg
music = ['music/firfloorfon.mp3']
def start_play_fon_music(number):
    pg.mixer.music.load(music[number])
    pg.mixer.music.play()