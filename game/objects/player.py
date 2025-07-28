import pygame as pg  # main library
from collections import OrderedDict

from .camera import Camera
from system.settings import WIGHT, HEIGHT, GRAVITY, SPEED, STRENGTH_JUMP
from game.objects.platform import Platform
from system.system import get_background, get_bottom, get_top, set_platforms, show_score, show_mini_score
from system.button import Button


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

    def update(self, platforms, gravity=True):
        if gravity:
            self.velocityY.y += self.gravity  # calculate speed with gravity

        if self.velocityY.y >= 20:
            self.velocityY.y = 20
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

        pause_flag = False
        game_over_flag = False
        pause_button = Button()
        pause_button.setImage("game/images/buttons/pause.png", "game/images/buttons/pause_hover.png")
        pause_button.setPosition(350, 17)
        pause_button.setSignal("pause")

        menu_button = Button()
        menu_button.setImage("game/images/buttons/menu.png", "game/images/buttons/menu_hover.png")
        menu_button.setPosition(300, 460)
        menu_button.setSignal("menu")

        play_again_button = Button()
        play_again_button.setImage("game/images/buttons/play_again.png", "game/images/buttons/play_again_hover.png")
        play_again_button.setPosition(120, 400)
        play_again_button.setSignal("play")

        background = get_background("game/images/background/background.png")
        bottom = get_bottom("game/images/background/bottom.png")
        top = get_top("game/images/background/top.png")
        pause_background = get_background("game/images/background/pause_background.png")

        pressed_keys = OrderedDict()
        with open("system/best_score.txt") as file:
            line = file.readline()
        BEST_SCORE = int(line) if line else 0

        while True:

            if pause_flag:
                screen.blit(pause_background, (0, 0))
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return "quit"
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if pause_button.click():
                            pause_flag = False
                            continue
                        if signal := play_again_button.click():
                            return signal
                        if signal := menu_button.click():
                            return signal

                screen.blit(bottom, (0, HEIGHT - bottom.get_height()))
                screen.blit(top, (0, 0))
                show_score(screen, self.max_score)

                pause_button.update()
                pause_button.draw(screen)

                menu_button.update()
                menu_button.draw(screen)

                play_again_button.update()
                play_again_button.draw(screen)

                pg.display.flip()
                clock.tick(60)

            elif game_over_flag:
                menu_button_rect = [270, 500 + 600]
                play_again_button_rect = [120, 500 + 600]

                game_over = pg.image.load("game/images/background/game_over.png")
                game_over_rect = [50, 200 + 600]

                your_score = pg.image.load("game/images/background/your_score.png")
                your_score_rect = [75, 350 + 600]

                your_high_score = pg.image.load("game/images/background/your_high_score.png")
                your_high_score_rect = [40, 400 + 600]

                score_rect = [225, 350 + 600]
                best_score_rect = [230, 410 + 600]

                all_objects = [game_over_rect, your_score_rect, your_high_score_rect, menu_button_rect,
                               play_again_button_rect, score_rect, best_score_rect]

                self.velocityX.x = 0

                while True:
                    screen.blit(background, (0, 0))

                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            return "quit"
                        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                            if signal := play_again_button.click():
                                return signal
                            if signal := menu_button.click():
                                return signal

                    if your_high_score_rect[1] <= self.rect.y:
                        self.pos += self.velocityY
                    else:
                        for obj in all_objects:
                            obj[1] -= self.velocityY.y

                    play_again_button.setPosition(*play_again_button_rect)
                    menu_button.setPosition(*menu_button_rect)
                    if self.rect.y <= 610:
                        self.update(all_platforms, gravity=False)
                        self.draw(screen)

                    screen.blit(bottom, (0, HEIGHT - bottom.get_height()))
                    screen.blit(top, (0, 0))
                    show_score(screen, self.max_score)

                    play_again_button.update()
                    menu_button.update()
                    pause_button.draw(screen)
                    play_again_button.draw(screen)
                    menu_button.draw(screen)

                    screen.blit(game_over, game_over_rect)
                    screen.blit(your_score, your_score_rect)
                    screen.blit(your_high_score, your_high_score_rect)

                    show_mini_score(screen, self.max_score, score_rect)
                    show_mini_score(screen, BEST_SCORE, best_score_rect)

                    pg.display.flip()
                    clock.tick(60)

            else:
                screen.blit(background, (0, 0))
                set_platforms(all_platforms)  # set and delete some amount of platforms

                for event in pg.event.get():  # get all events at the moment
                    if event.type == pg.QUIT:  # if user click on close button
                        return "quit"
                    if event.type == pg.USEREVENT:
                        self.stopJump()  # event for stop jumping animation
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if pause_button.click():
                            pause_flag = True

                if self.velocityY.y >= 20:
                    game_over_flag = True

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

                self.current_score += self.velocityY.y / 10
                if self.current_score < self.max_score:
                    self.max_score = self.current_score
                    if (a := int(abs(self.max_score))) > BEST_SCORE:
                        with open("system/best_score.txt", mode="w") as file:
                            file.write(str(a))
                show_score(screen, self.max_score)

                pause_button.update()
                pause_button.draw(screen)

                pg.display.flip()  # change display picture
                clock.tick(60)  # set fps
