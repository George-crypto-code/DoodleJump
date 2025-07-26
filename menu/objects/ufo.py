import pygame as pg


class UFO(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("menu/images/ufo/ufo.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300, 100)
        self.speed = 1

    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 250 or self.rect.x >= 300:
            self.speed *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
