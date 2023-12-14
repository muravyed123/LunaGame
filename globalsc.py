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

WIDTH, HEIGHT = pg.display.set_mode((0,0), pg.FULLSCREEN).get_size()
name = 'Kitty'
password = 457
level = 1


def crop_image(file, count_x, count_y, need, path):
    '''
    Функция для разрезания изображения на несколько изображений.
    file - путь к нужному файлу из директории
    count_x - число нужных фрагментов по горизонтали
    count_y - число нужных фрагментов по вертикали
    need - массив "нужных для записи фрагментов, обычно задается с помощью генератора"
    path - путь для записи полученных файлов
    '''
    im = Image.open(file)
    width, height = im.size
    for j in range(count_y):
        for i in range(count_x):
            im_crop = im.crop((width//count_x * i, height// count_y * j, width//count_x * (i + 1), height// count_y * (j + 1)))
            number = 1 + j * count_x + i 
            if number in need:
                n_path = path + str(number - need[0] + 1) + '.png'
                im_crop.save(n_path)

# Образец для разрезки изображения
# crop_image('materials/fire.png', 5, 3, [x + 1 for x in range(15)], 'Animations/fire/')


def howmanyFiles(path):
    # Функция получения количества файлов директории по пути
    dirs = os.listdir(path)
    return(len(dirs))


def give_name(nam):
    # Функция для записи имени персонажа
    global name
    name = nam


def menu_text(obj, scene, par):
    number, text = par
    from draw import checkpoints as ch
    if not ch[number]:
        from menu import create_text
        create_text(text, 2)
        remove_checkpoint(number)
        from draw import now_scene as n
        n.me.clear()
        n.me.start()


def end_game(p):
    from Sound import start_play_fon_music as start
    start(5, -1)
    from menu import create_end_menu as cr
    cr()


def create_dialog(par):
    number, signal, sig_par = par
    from menu import create_dialog
    create_dialog(number, signal, sig_par)


def remove_checkpoint(number):
    from draw import remove_checkpoints as remove
    remove(int(number))

