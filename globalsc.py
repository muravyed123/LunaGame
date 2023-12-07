from PIL import Image
import os
import pygame as pg
FPS = 60
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = 0xFFC91F
GREEN = (0, 255, 0)
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH , HEIGHT = pg.display.set_mode((0,0), pg.FULLSCREEN).get_size()
name = 'Kitty'
level = 1
def crop_image(file, count_x, count_y, need, path):
    im = Image.open(file)    
    width, height = im.size
    for j in range(count_y):
        for i in range(count_x):
            im_crop = im.crop((width//count_x * i, height// count_y * j, width//count_x * (i + 1), height// count_y * (j + 1)))
            number = 1 + j * count_x + i 
            if number in need:
                n_path = path + str(number - need[0] + 1) + '.png'
                im_crop.save(n_path)
#crop_image('materials/Lunago2.png', 3, 3, [x + 1 for x in range(8)], 'Animations/luna_go/')
def howmanyFiles(path):
    dirs = os.listdir(path)
    return(len(dirs))
def give_name(nam):
    global name
    name = nam
def create_dialog(par):
    number, signal, sig_par = par
    from menu import create_dialog
    create_dialog(number, signal, sig_par)
def remove_checkpoint(number):
    from draw import remove_checkpoints as remove
    remove(int(number))
#print(howmanyFiles('Animations/bl_cat_go'))