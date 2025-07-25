import pygame as pg


class MenuPlayer(pg.sprite.Sprite):  # main player class
    def __init__(self):
        super().__init__()  # inherit methods from sprite
        self.player_right = pg.image.load("data/player/player_right.png")  # save image
        self.player_right_jump = pg.image.load("data/player/player_right_jump.png")

        self.image = self.player_right

        self.rect = self.image.get_rect()  # get rect of player image
        self.jumping = False # flag for jump
        self.mask = pg.mask.from_surface(self.image)
        self.pos = pg.Vector2(100.0, 355.0)  # extra field for moving on coordinates
        self.velocityY = pg.Vector2(0.0, -3)  # start speed on Oy
        self.gravity = 0.3  # force of gravity
        self.rect.center = self.pos  # set player model on start

    def jump(self):
        self.velocityY.y = -8
        self.image = self.player_right_jump
        pg.time.set_timer(pg.USEREVENT, 300)
        self.jumping = True

    def stopJump(self):
        self.image = self.player_right
        pg.time.set_timer(pg.USEREVENT, 0)
        self.jumping = False

    def update(self, platforms):
        self.velocityY.y += self.gravity  # calculate speed with gravity
        self.pos += self.velocityY

        for platform in platforms:
            if (pg.sprite.collide_mask(self, platform) and
                    platform.rect.bottom >= self.rect.bottom and self.velocityY.y >= 0):
                self.jump()

        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)
