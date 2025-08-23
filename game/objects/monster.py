import pygame as pg


class Monster(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.frames = [pg.image.load("game/images/monster/2.png"),
                       pg.image.load("game/images/monster/3.png"),
                       pg.image.load("game/images/monster/4.png"),
                       pg.image.load("game/images/monster/5.png"),
                       pg.image.load("game/images/monster/1.png")]

        self.image = pg.image.load("game/images/monster/1.png")
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.speed = 2
        self.x = 0
        self.counter = 0

    def update(self):
        self.counter += 1
        self.counter %= 25
        self.image = self.frames[self.counter // 5]
        a = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = a
        self.rect.x += self.speed
        if self.rect.x >= self.x + 100 or self.rect.x <= self.x:
            self.speed *= -1
        self.mask = pg.mask.from_surface(self.image)

    def setPosition(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.x = x