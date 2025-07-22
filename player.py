import pygame as pg  # main library
from system import load_image  # func for upload picture player model


class Player(pg.sprite.Sprite):  # main player class
    image = load_image("player.png")  # loading player model

    def __init__(self, *group):
        super().__init__(*group)  # inherit methods from sprite
        self.image = Player.image  # save image
        self.rect = self.image.get_rect()  # get rect of player image
        self.pos = pg.Vector2(300.0, 555.0)  # extra field for moving on coordinates
        self.velocityY = pg.Vector2(0.0, -15.0)  # start speed on Oy
        self.velocityX = pg.Vector2(0.0, 0.0)  # start speed on Ox
        self.gravity = 0.6  # force of gravity
        self.rect.center = self.pos  # set player model on start

    def movingLeft(self):  # moving while pressed A
        self.velocityX.x = -3

    def stopMoving(self):  # stop moving on Ox
        self.velocityX.x = 0

    def movingRight(self):  # moving while pressed D
        self.velocityX.x = 3

    def setDirection(self, direction):  # change image depending on moving
        if direction == "left":
            self.image = pg.transform.flip(Player.image, 1, 0)  # take base picture and mirroring
        elif direction == "right":
            self.image = Player.image  # base picture
        else:
            raise Exception("This direct does not exist")

    def update(self, *args):
        self.velocityY.y += self.gravity  # calculate speed with gravity
        self.pos += self.velocityY + self.velocityX  # calculate pos

        if self.pos.y >= 555:  # when player reach end of map
            self.pos.y = 555
            self.velocityY.y = -15  # all lope are the same

        self.rect.center = self.pos  # set player model on the new place
