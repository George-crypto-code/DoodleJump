import pygame as pg


class Propeller(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.frames = [pg.image.load("game/images/propeller/2.png"),
                       pg.image.load("game/images/propeller/3.png"),
                       pg.image.load("game/images/propeller/4.png")]
        self.image = pg.image.load("game/images/propeller/1.png")
        self.rect = self.image.get_rect()
        self.counter = 0

    def update(self):
        self.counter += 1
        self.counter %= 31
        self.image = self.frames[self.counter // 10]
        a = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = a

    def drawFly(self, screen, pos):
        screen.blit(screen, pos)

    def setPosition(self, x, y):
        self.rect.midbottom = x, y

    def checkCollide(self, platforms):
        if len(pg.sprite.spritecollide(self, platforms, False)) <= 1:
            return True
        return False