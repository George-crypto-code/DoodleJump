import pygame as pg
from config.settings import WIGHT, GRAVITY, SPEED, STRENGTH_JUMP
from game.objects.platform import BreakingPlatform


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_right = pg.image.load("game/images/player/player_right.png")
        self.player_right_jump = pg.image.load("game/images/player/player_right_jump.png")
        self.player_left = pg.image.load("game/images/player/player_left.png")
        self.player_left_jump = pg.image.load("game/images/player/player_left_jump.png")

        self.jump_sound = pg.mixer.Sound("sounds/jump.wav")
        self.spring_sound = pg.mixer.Sound("sounds/spring.wav")
        self.trump_sound = pg.mixer.Sound("sounds/trampoline.wav")
        self.propeller_sound = pg.mixer.Sound("sounds/propeller.wav")
        self.jetpack_sound = pg.mixer.Sound("sounds/jetpack.wav")
        self.break_sound = pg.mixer.Sound("sounds/break.wav")

        self.image = self.player_right

        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        self.pos = pg.Vector2(100.0, 355.0)
        self.velocityY = pg.Vector2(0.0, STRENGTH_JUMP)
        self.velocityX = pg.Vector2(0.0, 0.0)
        self.gravity = GRAVITY
        self.rect.center = self.getPos()

        self.direction = True
        self.jumping = False
        self.propeller_flag = False
        self.jetpack_flag = False
        self.stan = False

    def movingLeft(self):
        self.velocityX.x = -SPEED

    def stopMoving(self):
        self.velocityX.x = 0

    def movingRight(self):
        self.velocityX.x = SPEED

    def setDirection(self, direction):
        if direction == "left":
            self.image = self.player_left_jump if self.jumping else self.player_left
            self.direction = False
        elif direction == "right":
            self.image = self.player_right_jump if self.jumping else self.player_right
            self.direction = True

    def setVelocityX(self, value):
        self.velocityX.x = value

    def setVelocityY(self, value):
        self.velocityY.y = value

    def jump(self, k=1.0):
        self.velocityY.y = STRENGTH_JUMP * k
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

    def update(self, platforms, springs, trumps, propellers, jetpacks, monsters, gravity=True):
        if self.propeller_flag:
            for propeller in propellers:
                propeller.update()
                propeller.setPosition(self.rect.x + 31 + self.velocityX.x, self.rect.y + 25)
            self.pos += self.velocityX
            self.rect.center = self.getPos()
            self.rect.centerx %= WIGHT
        elif self.jetpack_flag:
            for jetpack in jetpacks:
                jetpack.update()

                if self.direction:
                    jetpack.image = pg.transform.flip(jetpack.image, 1, 0)
                    dx, dy = 11, 80
                else:
                    dx, dy = 50, 80
                jetpack.setPosition(self.rect.x + dx + self.velocityX.x, self.rect.y + dy)
            self.pos += self.velocityX
            self.rect.center = self.getPos()
            self.rect.centerx %= WIGHT
        else:
            if gravity:
                self.velocityY.y += self.gravity

            velocity_y = self.velocityY.y
            if velocity_y > 20:
                self.velocityY.y = 20

            if not self.stan:
                for spring in springs:
                    if (pg.sprite.collide_rect(self, spring)
                            and spring.rect.bottom >= self.rect.bottom and self.velocityY.y >= 0):
                        self.jump(k=1.5)
                        spring.active()
                        self.spring_sound.play()

                for trump in trumps:
                    if (pg.sprite.collide_rect(self, trump)
                            and trump.rect.bottom >= self.rect.bottom and self.velocityY.y >= 0):
                        self.jump(k=2)
                        trump.active()
                        self.trump_sound.play()

                for propeller in propellers:
                    if pg.sprite.collide_rect(self, propeller):
                        self.propeller_flag = True
                        self.velocityY.y = -10
                        self.propeller_sound.play()
                        pg.time.set_timer(pg.USEREVENT + 1, 2700)

                for jetpack in jetpacks:
                    if pg.sprite.collide_rect(self, jetpack):
                        self.jetpack_flag = True
                        self.velocityY.y = -15
                        self.jetpack_sound.play()
                        pg.time.set_timer(pg.USEREVENT + 2, 3200)

                for monster in monsters:
                    if pg.sprite.collide_rect(self, monster):
                        self.stan = True

                for platform in platforms:
                    if (pg.sprite.collide_mask(self, platform)
                            and platform.rect.bottom >= self.rect.bottom and self.velocityY.y >= 0):
                        self.jump()
                        self.jump_sound.play()

                self.pos += self.velocityX
                self.rect.center = self.getPos()
                self.rect.centerx %= WIGHT

    def falling(self):
        self.pos += self.velocityY
        self.rect.center = self.getPos()

    def propellerStop(self, propellers):
        self.propeller_flag = False
        for propeller in propellers:
            propeller.kill()
        pg.time.set_timer(pg.USEREVENT + 1, 0)

    def jetpackStop(self, jetpacks):
        self.jetpack_flag = False
        for jetpack in jetpacks:
            jetpack.kill()
        pg.time.set_timer(pg.USEREVENT + 2, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def getCurrentSpeedX(self):
        return self.velocityX.x

    def getCurrentSpeedY(self):
        return self.velocityY.y

    def getPos(self):
        return int(self.pos.x), int(self.pos.y)
