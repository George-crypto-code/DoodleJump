from random import randint

import pygame as pg

from game.objects.platform import Platform
from game.objects.spring import Spring
from game.objects.trump import Trump
from game.objects.propeller import Propeller
from config.settings import *


def get_background(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (WIGHT, HEIGHT))


def get_bottom(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (WIGHT, image.get_height() * (WIGHT / image.get_width())))


def get_top(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (WIGHT, image.get_height() * (WIGHT / image.get_width())))


def set_platforms(all_platforms):
    for i in range(PLATFORM_AMOUNT - len(all_platforms)):
        current_platform = Platform(all_platforms)
        x = randint(3, WIGHT - 60)
        y = PLATFORM_HEIGHT[i]
        current_platform.setPlatform(x, y)


def update_platforms(all_platforms, all_springs, all_trumps, all_propellers, score):
    lowest_platform = highest_platform = None
    for platform in all_platforms:
        if lowest_platform is None or platform.rect.y > lowest_platform.rect.y:
            lowest_platform = platform
        if highest_platform is None or platform.rect.y < highest_platform.rect.y:
            highest_platform = platform

    if lowest_platform.rect.y >= HEIGHT + 60:
        all_platforms.remove(lowest_platform)
        current_platform = Platform(all_platforms)
        x = randint(3, WIGHT - 60)
        y = highest_platform.rect.y - 60

        if score % 13 == 0:
            spring = Spring(all_springs)
            spring.setPosition(x + 28, y + 2)

        if score and score % 31 == 0:
            trump = Trump(all_trumps)
            trump.setPosition(x + 28, y + 2)

        if score and score % 97 == 0:
            propeller = Propeller(all_propellers)
            propeller.setPosition(x + 28, y + 2)

        current_platform.setPlatform(x, y)
        return 1
    return 0



def show_score(screen, score):
    wight = 10
    for digit in str(int(abs(score))):
        image = pg.image.load(f"game/images/numbers/default/{digit}.png")
        screen.blit(image, (wight, 5))
        wight += image.get_width()


def show_mini_score(screen, score, pos):
    wight = 0
    x, y = pos
    for digit in str(int(abs(score))):
        image = pg.image.load(f"game/images/numbers/mini/{digit}.png")
        screen.blit(image, (x + wight, y))
        wight += image.get_width()
