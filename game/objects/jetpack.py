import pygame as pg


class Jetpack(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

        self.frames = [pg.image.load("game/images/jetpack/2.png"),
                       pg.image.load("game/images/jetpack/3.png"),
                       pg.image.load("game/images/jetpack/4.png")]

        self.image = pg.image.load("game/images/jetpack/1.png")
        self.rect = self.image.get_rect()
        self.counter = 0

    def update(self):
        self.counter += 1
        self.counter %= 15
        self.image = self.frames[self.counter // 5]
        a = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = a

    def setPosition(self, x, y):
        self.rect.midbottom = x, y
