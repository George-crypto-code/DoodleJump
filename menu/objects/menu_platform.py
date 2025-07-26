import pygame as pg


class MenuPlatform(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pg.image.load("menu/images/platform/platform.png")
        self.rect = self.image.get_rect()

    def setPlatform(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def checkCollide(self, platforms):
        if len(pg.sprite.spritecollide(self, platforms, False)) <= 1:
            return True
        return False

