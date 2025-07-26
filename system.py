from random import randint

import pygame as pg

from platform import Platform
from settings import *
import os
import sys


def load_image(name):  # func which return pg image
    fullname = os.path.join("data", name)  # take full path of file
    if not os.path.isfile(fullname):  # check file
        print(f"File not found")
        sys.exit()
    image = pg.image.load(fullname)  # load image
    return image


def get_background(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (WIGHT, HEIGHT))


def get_bottom(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (WIGHT, image.get_height() * (WIGHT / image.get_width())))


def get_button(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (130, 47))


def set_platforms(all_platforms):
    for platform in all_platforms:
        if platform.rect.centery >= HEIGHT + 50:
            platform.kill()
            all_platforms.remove(platform)

    for i in range(PLATFORM_AMOUNT - len(all_platforms)):
        current_platform = Platform(all_platforms)
        x = randint(3, WIGHT - 60)
        y = HEIGHT // PLATFORM_AMOUNT * i - 10
        current_platform.setPlatform(x, y)
        while not current_platform.checkCollide(all_platforms):
            x = randint(3, WIGHT - 60)
            current_platform.setPlatform(x, y)
