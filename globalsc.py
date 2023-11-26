from PIL import Image
import os
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

WIDTH = 1280
HEIGHT = 720
def crop_image(file, count_x, count_y, need, path):
    im = Image.open(file)    
    width, height = im.size
    for i in range(count_x):
        for j in range(count_y):
            im_crop = im.crop((width//count_x * i, height// count_y * j, width//count_x * (i + 1), height// count_y * (j + 1)))
            number = 1 + i * count_y + j 
            if number in need:
                n_path = path + str(number - need[0] + 1) + '.png'
                im_crop.save(n_path)
#crop_image('materials/cat_Anim.png', 4, 13, [14,15,16,17,18,19], 'Animations/bl_cat_sit/')
def howmanyFiles(path):
    dirs = os.listdir(path)
    return(len(dirs))
#print(howmanyFiles('Animations/bl_cat_go'))