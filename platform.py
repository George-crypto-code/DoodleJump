import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pg.image.load("data/platforms/platform.png")
        self.rect = self.image.get_rect()

    def setPlatform(self, x, y):
        self.rect.x = x
        self.rect.y = y
