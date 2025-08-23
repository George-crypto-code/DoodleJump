from random import randint, choice

import pygame as pg

from game.objects.jetpack import Jetpack
from game.objects.monster import Monster
from game.objects.platform import Platform, MovingPlatform, BreakingPlatform
from game.objects.spring import Spring
from game.objects.trump import Trump
from game.objects.propeller import Propeller
from config.settings import *
from config.settings import OBJECTS_INTERVALS, SPRING_INTERVAL, TRUMP_INTERVAL, PROPELLER_INTERVAL, JETPACK_INTERVAL


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


def update_platforms(all_platforms, all_springs, all_trumps, all_propellers, all_jetpacks, all_monsters, score):
    lowest_platform = highest_platform = None

    for platform in all_platforms:
        if lowest_platform is None or platform.rect.y > lowest_platform.rect.y:
            lowest_platform = platform
        if highest_platform is None or platform.rect.y < highest_platform.rect.y:
            highest_platform = platform

    if lowest_platform.rect.y >= HEIGHT + 60:

        all_platforms.remove(lowest_platform)
        event = None

        if score and score % 233 == 0:
            x = 250
            y = highest_platform.rect.y - 60
            monster = Monster(all_monsters)
            monster.setPosition(10, y)
            monster_sound = pg.mixer.Sound("sounds/monster.wav")
            monster_sound.play()
        # elif score >= 200 and randint(1, 5) == 3:
        #     current_platform = MovingPlatform(1, all_platforms)
        #     x = randint(3, WIGHT - 60)
        #     y = highest_platform.rect.y - 60
        # elif score % 10 == 0:
        #     current_platform = BreakingPlatform(all_platforms)
        #     x = randint(3, WIGHT - 60)
        #     y = highest_platform.rect.y - 60
        else:
            x = randint(3, WIGHT - 60)
            y = highest_platform.rect.y - 60

            if score and score % OBJECTS_INTERVALS["spring_interval"] == 0:
                event = Spring(all_springs)
                OBJECTS_INTERVALS["spring_interval"] += choice(SPRING_INTERVAL)

            elif score and score % OBJECTS_INTERVALS["trump_interval"] == 0:
                event = Trump(all_trumps)
                OBJECTS_INTERVALS["trump_interval"] += choice(TRUMP_INTERVAL)

            elif score and score % OBJECTS_INTERVALS["propeller_interval"] == 0:
                event = Propeller(all_propellers)
                OBJECTS_INTERVALS["propeller_interval"] += choice(PROPELLER_INTERVAL)

            elif score and score % OBJECTS_INTERVALS["jetpack_interval"] == 0:
                event = Jetpack(all_jetpacks)
                OBJECTS_INTERVALS["jetpack_interval"] += choice(JETPACK_INTERVAL)

        if score >= 200 and randint(1, 5) == 3:
            current_platform = MovingPlatform(1, event, all_platforms)
        else:
            current_platform = Platform(all_platforms)

        current_platform.setPlatform(x, y)
        if event:
            event.setPosition(x + 28, y + 2)

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
