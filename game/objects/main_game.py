from collections import OrderedDict

import pygame as pg

from config.button import Button
from config.settings import HEIGHT
from config.system import get_background, get_bottom, get_top, set_platforms, show_score, show_mini_score, \
    update_platforms
from game.objects.player import Player
from game.objects.camera import Camera


def main_game(screen):
    clock = pg.time.Clock()
    all_platforms = pg.sprite.Group()
    all_springs = pg.sprite.Group()
    all_trumps = pg.sprite.Group()
    all_propellers = pg.sprite.Group()
    all_jetpacks = pg.sprite.Group()
    all_monsters = pg.sprite.Group()
    set_platforms(all_platforms)
    camera = Camera()
    player = Player()
    current_score, max_score = 0, 0

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

    pause_sound = pg.mixer.Sound("sounds/pause.wav")
    unpause_sound = pg.mixer.Sound("sounds/unpause.wav")
    game_over_sound = pg.mixer.Sound("sounds/fall.wav")
    button_sound = pg.mixer.Sound("sounds/button.wav")

    pressed_keys = OrderedDict()
    with open("config/best_score.txt") as file:
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
                        unpause_sound.play()
                        break
                    if signal := play_again_button.click():
                        button_sound.play()
                        return signal
                    if signal := menu_button.click():
                        button_sound.play()
                        return signal

            screen.blit(bottom, (0, HEIGHT - bottom.get_height()))
            screen.blit(top, (0, 0))
            show_score(screen, max_score)

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

            player.setVelocityX(0)
            player_pos = player.getPos()
            player_velocity_y = player.getCurrentSpeedY()

            while True:
                screen.blit(background, (0, 0))

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return "quit"
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if signal := play_again_button.click():
                            button_sound.play()
                            return signal
                        if signal := menu_button.click():
                            button_sound.play()
                            return signal

                if your_high_score_rect[1] <= player_pos[1]:
                    player.falling()
                else:
                    for obj in all_objects:
                        obj[1] -= player_velocity_y

                player.draw(screen)

                play_again_button.setPosition(*play_again_button_rect)
                menu_button.setPosition(*menu_button_rect)

                if player_pos[1] >= 650:
                    player.kill()

                screen.blit(bottom, (0, HEIGHT - bottom.get_height()))
                screen.blit(top, (0, 0))
                show_score(screen, max_score)

                play_again_button.update()
                menu_button.update()
                pause_button.draw(screen)
                play_again_button.draw(screen)
                menu_button.draw(screen)

                screen.blit(game_over, game_over_rect)
                screen.blit(your_score, your_score_rect)
                screen.blit(your_high_score, your_high_score_rect)

                show_mini_score(screen, max_score, score_rect)
                show_mini_score(screen, BEST_SCORE, best_score_rect)

                pg.display.flip()
                clock.tick(60)
        else:
            screen.blit(background, (0, 0))
            current_score += update_platforms(all_platforms, all_springs, all_trumps, all_propellers, all_jetpacks, all_monsters, current_score)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "quit"

                if event.type == pg.USEREVENT:
                    player.stopJump()

                if event.type == pg.USEREVENT + 1:
                    player.propellerStop(all_propellers)

                if event.type == pg.USEREVENT + 2:
                    player.jetpackStop(all_jetpacks)

                if event.type == pg.USEREVENT + 3:
                    player.stopStan()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if pause_button.click():
                        pause_flag = True
                        pause_sound.play()

            if player.velocityY.y >= 20:
                game_over_flag = True
                game_over_sound.play()

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
                    player.setDirection("right")
                    player.movingRight()
                else:
                    player.setDirection("left")
                    player.movingLeft()
            else:
                player.stopMoving()

            player.update(all_platforms, all_springs, all_trumps, all_propellers, all_jetpacks, all_monsters, screen)
            all_platforms.update()
            all_monsters.update()
            all_platforms.draw(screen)
            all_springs.draw(screen)
            all_trumps.draw(screen)
            all_jetpacks.draw(screen)
            all_monsters.draw(screen)
            player.draw(screen)
            all_propellers.draw(screen)

            camera.update(player)
            for platform in all_platforms:
                camera.apply(platform)

            for spring in all_springs:
                camera.apply(spring)
                if spring.rect.midbottom[1] >= 660:
                    spring.kill()

            for trump in all_trumps:
                camera.apply(trump)
                if trump.rect.midbottom[1] >= 660:
                    trump.kill()

            for propeller in all_propellers:
                camera.apply(propeller)
                if propeller.rect.midbottom[1] >= 660:
                    propeller.kill()

            for jetpack in all_jetpacks:
                camera.apply(jetpack)
                if jetpack.rect.midbottom[1] >= 660:
                    jetpack.kill()

            for monster in all_monsters:
                camera.apply(monster)
                if monster.rect.midbottom[1] >= 660:
                    monster.kill()

            screen.blit(bottom, (0, HEIGHT - bottom.get_height()))
            screen.blit(top, (0, 0))

            if current_score > max_score:
                max_score = current_score
                if max_score > BEST_SCORE:
                    BEST_SCORE = max_score
                    with open("config/best_score.txt", mode="w") as file:
                        file.write(str(max_score))

            show_score(screen, max_score)

            pause_button.update()
            pause_button.draw(screen)

            pg.display.flip()
            clock.tick(60)