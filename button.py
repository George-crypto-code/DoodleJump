import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hover_image, self.default_image = None, None
        self.image,self.rect, self.mask  = None, None,None
        self.is_hover = False
        self.signal = None

    def checkHover(self):
        mouse_pos = pg.mouse.get_pos()
        return self.mask.get_at((mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y))

    def update(self):
        self.is_hover = self.checkHover()
        if self.is_hover:
            self.image = self.hover_image
        else:
            self.image = self.default_image
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def setImage(self, default_image, hover_image):
        self.default_image = default_image
        self.hover_image = hover_image
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def setSignal(self, signal):
        self.signal = signal

    def setPosition(self, x, y):
        self.rect.centre = x, y

    def click(self):
        if self.checkHover():
            return self.signal
        return None

    def draw(self, screen):
        screen.blit(self.image, self.rect)
