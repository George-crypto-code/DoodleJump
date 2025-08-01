import pygame as pg


class Spring(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.default_image = pg.image.load("game/images/spring/short.png")
        self.active_image = pg.image.load("game/images/spring/long.png")
        self.default_image_rect = self.default_image.get_rect()
        self.active_image_rect = self.active_image.get_rect()

        self.image = self.default_image
        self.rect = self.default_image_rect

    def setPosition(self, x, y):
        self.rect.midbottom = x, y

    def active(self):
        self.image = self.active_image
        a = self.rect.midbottom
        self.rect = self.active_image_rect
        self.rect.midbottom = a
