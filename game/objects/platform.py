import pygame as pg

from config.settings import WIGHT


class Platform(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pg.image.load("game/images/platforms/platform.png")
        self.rect = self.image.get_rect()
        self.x, self.y = 0, 0

    def setPlatform(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.x, self.y = x, y


class MovingPlatform(Platform):
    def __init__(self, speed, event, *group):
        super().__init__(*group)
        self.image = pg.image.load("game/images/platforms/moving_platform.png")
        self.rect = self.image.get_rect()
        self.speed = speed
        self.event = event if event else None

    def update(self):
        self.rect.x += self.speed
        if self.event:
            self.event.rect.x += self.speed
        if self.rect.x >= WIGHT - 60 or self.rect.x <= 3:
            self.speed *= -1

# ----------------------------doesn't work------------------------------

class BreakingPlatform(Platform):
    def __init__(self, *group):
        super().__init__(*group)

        self.frames = [pg.image.load("game/images/platforms/breaking_platform/2.png"),
                       pg.image.load("game/images/platforms/breaking_platform/3.png"),
                       pg.image.load("game/images/platforms/breaking_platform/4.png")]

        self.image = pg.image.load("game/images/platforms/breaking_platform/1.png")
        self.rect = self.image.get_rect()
        self.counter = 0
        self.break_flag = False

    def update(self):
        if self.break_flag:
            if self.counter < 14:
                self.counter += 1
                self.image = self.frames[self.counter // 5]
                x, y = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = (x, y)
            else:
                self.image = pg.image.load("game/images/platforms/breaking_platform/1.png")
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
                self.image = pg.Surface((0, 0))

    # def breaking(self):
    #     break_sound = pg.mixer.Sound("sounds/break.wav")
    #     break_sound.play()
    #     self.break_flag = True
