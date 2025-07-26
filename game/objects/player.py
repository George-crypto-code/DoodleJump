import pygame as pg  # main library
from collections import OrderedDict

from .camera import Camera
from system.settings import WIGHT, HEIGHT, GRAVITY, SPEED, STRENGTH_JUMP
from game.objects.platform import Platform
from system.system import get_background, get_bottom, get_top, set_platforms, show_score


class Player(pg.sprite.Sprite):  # main player class
    def __init__(self):
        super().__init__()  # inherit methods from sprite
        self.player_right = pg.image.load("game/images/player/player_right.png")  # save image
        self.player_right_jump = pg.image.load("game/images/player/player_right_jump.png")
        self.player_left = pg.image.load("game/images/player/player_left.png")
        self.player_left_jump = pg.image.load("game/images/player/player_left_jump.png")

        self.image = self.player_right

        self.rect = self.image.get_rect()  # get rect of player image
        self.mask = pg.mask.from_surface(self.image)

        self.pos = pg.Vector2(100.0, 355.0)  # extra field for moving on coordinates
        self.velocityY = pg.Vector2(0.0, STRENGTH_JUMP)  # start speed on Oy
        self.velocityX = pg.Vector2(0.0, 0.0)  # start speed on Ox
        self.gravity = GRAVITY  # force of gravity
        self.rect.center = self.pos  # set player model on start

        self.direction = True  # direction for picture
        self.jumping = False  # flag for jump
        self.current_score, self.max_score = 0, 0

    def movingLeft(self):  # moving while pressed A
        self.velocityX.x = -SPEED

    def stopMoving(self):  # stop moving on Ox
        self.velocityX.x = 0

    def movingRight(self):  # moving while pressed D
        self.velocityX.x = SPEED

    def setDirection(self, direction):  # change image depending on moving
        if direction == "left":
            self.image = self.player_left_jump if self.jumping else self.player_left
            self.direction = False
        elif direction == "right":
            self.image = self.player_right_jump if self.jumping else self.player_right
            self.direction = True

    def jump(self):
        self.velocityY.y = STRENGTH_JUMP
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

    def running(self, screen):
        clock = pg.time.Clock()  # set time on main cycle
        all_platforms = pg.sprite.Group()
        Platform(all_platforms).setPlatform(70, 450)  # start platform will always place here
        camera = Camera()
        background = get_background("game/images/background/background.png")
        bottom = get_bottom("game/images/background/bottom.png")
        top = get_top("game/images/background/top.png")

        pressed_keys = OrderedDict()

        while True:

            screen.blit(background, (0, 0))
            set_platforms(all_platforms)  # set and delete some amount of platforms

            for event in pg.event.get():  # get all events at the moment
                if event.type == pg.QUIT:  # if user click on close button
                    return "quit"
                if event.type == pg.USEREVENT:
                    self.stopJump()  # event for stop jumping animation

            keys = pg.key.get_pressed()
            if keys[pg.K_d]:
                pressed_keys["d"] = True
            else:
                pressed_keys.pop("d", None)

            if keys[pg.K_a]:
                pressed_keys["a"] = True
            else:
                pressed_keys.pop("a", None)

            if pressed_keys:
                current_key = next(reversed(pressed_keys))
                if current_key == "d":
                    self.setDirection("right")
                    self.movingRight()
                else:
                    self.setDirection("left")
                    self.movingLeft()
            else:
                self.stopMoving()

            self.update(all_platforms)  # update speed and collision
            all_platforms.draw(screen)  # draw all platforms
            self.draw(screen)  # draw player

            camera.update(self)  # watch for player
            for platform in all_platforms:
                camera.apply(platform)

            screen.blit(bottom, (0, HEIGHT - bottom.get_height()))
            screen.blit(top, (0, 0))

            self.current_score += self.velocityY.y / 20
            # if
            self.max_score = min(self.current_score, self.max_score)
            show_score(screen, self.max_score)

            pg.display.flip()  # change display picture
            clock.tick(60)  # set fps
