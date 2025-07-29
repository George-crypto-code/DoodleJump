from random import randint

import pygame as pg

from game.objects.platform import Platform
from game.objects.spring import Spring
from game.objects.trump import Trump
from system.settings import *


def get_background(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (WIGHT, HEIGHT))


def get_bottom(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (WIGHT, image.get_height() * (WIGHT / image.get_width())))


def get_top(path):
    image = pg.image.load(path)
    return pg.transform.scale(image, (WIGHT, image.get_height() * (WIGHT / image.get_width())))


def set_platforms(all_platforms, all_springs, all_trumps, score):
    score = abs(int(score))
    for platform in all_platforms:
        if platform.rect.centery >= HEIGHT + 50:
            platform.kill()
            all_platforms.remove(platform)

    for i in range(PLATFORM_AMOUNT - len(all_platforms)):
        current_platform = Platform(all_platforms)
        x = randint(3, WIGHT - 60)
        y = HEIGHT // PLATFORM_AMOUNT * i - 10

        current_platform.setPlatform(x, y)

        if score > 10 and 0 <= score % 150 <= 2:
            trump = Trump(all_trumps)
            trump.setPosition(x + 27, y + 3)

            while not (current_platform.checkCollide(all_platforms) and trump.checkCollide(all_platforms)):
                x = randint(3, WIGHT - 60)
                current_platform.setPlatform(x, y)
                trump.setPosition(x + 27, y + 3)

        elif score > 10 and 0 <= score % 100 <= 2:
            spring = Spring(all_springs)
            spring.setPosition(x + 28, y + 3)

            while not (current_platform.checkCollide(all_platforms) and spring.checkCollide(all_platforms)):
                x = randint(3, WIGHT - 60)
                current_platform.setPlatform(x, y)
                spring.setPosition(x + 28, y + 3)
        else:
            while not current_platform.checkCollide(all_platforms):
                x = randint(3, WIGHT - 60)
                current_platform.setPlatform(x, y)


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

