import pygame as pg  # main library
from settings import WIGHT


class Player(pg.sprite.Sprite):  # main player class
    def __init__(self):
        super().__init__()  # inherit methods from sprite
        self.player_right = pg.image.load("data/player/player_right.png")  # save image
        self.player_right_jump = pg.image.load("data/player/player_right_jump.png")
        self.player_left = pg.image.load("data/player/player_left.png")
        self.player_left_jump = pg.image.load("data/player/player_left_jump.png")

        self.image = self.player_right

        self.rect = self.image.get_rect()  # get rect of player image
        self.direction = True # direction for picture
        self.jumping = False # flag for jump
        self.mask = pg.mask.from_surface(self.image)
        self.pos = pg.Vector2(100.0, 355.0)  # extra field for moving on coordinates
        self.velocityY = pg.Vector2(0.0, -3)  # start speed on Oy
        self.velocityX = pg.Vector2(0.0, 0.0)  # start speed on Ox
        self.gravity = 0.03  # force of gravity
        self.rect.center = self.pos  # set player model on start

    def movingLeft(self):  # moving while pressed A
        self.velocityX.x = -2

    def stopMoving(self):  # stop moving on Ox
        self.velocityX.x = 0

    def movingRight(self):  # moving while pressed D
        self.velocityX.x = 2

    def setDirection(self, direction):  # change image depending on moving
        if direction == "left":
            self.image = self.player_left_jump if self.jumping else self.player_left
            self.direction = False
        elif direction == "right":
            self.image = self.player_right_jump if self.jumping else self.player_right
            self.direction = True

    def jump(self):
        self.velocityY.y = -3
        if self.direction:
            self.image = self.player_right_jump
        else:
            self.image = self.player_left_jump

        pg.time.set_timer(pg.USEREVENT, 300)
        self.jumping = True

    def stopJump(self):
        if self.direction:
            self.image = self.player_right
        else:
            self.image = self.player_left

        pg.time.set_timer(pg.USEREVENT, 0)
        self.jumping = False

    def update(self, platforms):
        self.velocityY.y += self.gravity  # calculate speed with gravity
        self.pos += self.velocityX  # calculate pos

        for platform in platforms:
            if (pg.sprite.collide_mask(self, platform) and
                    platform.rect.bottom >= self.rect.bottom and self.velocityY.y >= 0):
                self.jump()

        self.rect.center = self.pos  # set player model on the new place
        self.rect.centerx %= WIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)
