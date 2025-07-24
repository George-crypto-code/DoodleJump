import pygame as pg  # main library
from settings import WIGHT


class Player(pg.sprite.Sprite):  # main player class
    def __init__(self):
        super().__init__()  # inherit methods from sprite
        self.image = pg.image.load("data/player/player_right.png")  # save image
        self.rect = self.image.get_rect()  # get rect of player image
        self.direction = "right" # direction for picture
        self.flag_timer = False # flag for jump
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
            path = "data/player/player_left_jump.png" if self.flag_timer else "data/player/player_left.png"
            self.image = pg.image.load(path)  # take base picture and mirroring
            self.direction = "left"
        elif direction == "right":
            path = "data/player/player_right_jump.png" if self.flag_timer else "data/player/player_right.png"
            self.image = pg.image.load(path)  # base picture
            self.direction = "right"
        else:
            raise Exception("This direct does not exist")

    def jump(self):
        self.velocityY.y = -3
        if self.direction == "right":
            self.image = pg.image.load("data/player/player_right_jump.png")
        else:
            self.image = pg.image.load("data/player/player_left_jump.png")

        pg.time.set_timer(pg.USEREVENT, 300)
        self.flag_timer = True

    def stopJump(self):
        if self.direction == "right":
            self.image = pg.image.load("data/player/player_right.png")
        else:
            self.image = pg.image.load("data/player/player_left.png")

        pg.time.set_timer(pg.USEREVENT, 0)
        self.flag_timer = False

    def update(self, platforms):
        self.velocityY.y += self.gravity  # calculate speed with gravity
        self.pos += self.velocityX  # calculate pos

        for platform in platforms:
            if (pg.sprite.collide_mask(self, platform) and
                    platform.rect.bottom >= self.rect.bottom and self.velocityY.y >= 0):
                self.jump()

        self.rect.center = self.pos  # set player model on the new place
        self.rect.centerx %= WIGHT
