import pygame as pg
import os
import sys


def load_image(name):  # func which return pg image
    fullname = os.path.join("data", name)  # take full path of file
    if not os.path.isfile(fullname):  # check file
        print(f"File not found")
        sys.exit()
    image = pg.image.load(fullname)  # load image
    return image
