import pygame as pg


class Stars(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.frames = [
            pg.image.load("game/images/stars/1.png"),
            pg.image.load("game/images/stars/2.png"),
            pg.image.load("game/images/stars/3.png")
        ]

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.counter = 0

    def update(self):
        self.counter += 1
        self.counter %= 15
        self.image = self.frames[self.counter // 5]
        a = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = a

    def draw(self, screen, pos):
        screen.blit(self.image, pos)

    def setPosition(self, x, y):
        self.rect.midbottom = x, y
