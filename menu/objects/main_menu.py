import pygame as pg
from config.button import Button
from config.system import get_background
from menu.objects.menu_player import MenuPlayer
from menu.objects.menu_platform import MenuPlatform
from menu.objects.ufo import UFO


def main_menu(screen):
    background = get_background("menu/images/background/main_menu_background.png")
    play_button = Button()
    play_button.setImage("menu/images/button/play.png", "menu/images/button/play_hover.png")
    play_button.setSignal("play")
    options_button = Button()
    options_button.setImage("menu/images/button/options.png", "menu/images/button/options_hover.png")
    options_button.setSignal("options")

    play_button.setPosition(140, 200)
    options_button.setPosition(140, 270)

    clock = pg.time.Clock()
    player = MenuPlayer()
    ufo = UFO()
    all_platforms = pg.sprite.Group()
    platform = MenuPlatform(all_platforms)
    platform.setPlatform(80, 450)
    sound = pg.mixer.Sound("sounds/button.wav")

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return "quit"
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if signal := play_button.click():
                    sound.play()
                    return signal
                if signal := options_button.click():
                    sound.play()
                    return signal
            if event.type == pg.USEREVENT:
                player.stopJump()

        screen.blit(background, (0, 0))
        play_button.update()
        options_button.update()
        play_button.draw(screen)
        options_button.draw(screen)
        player.update(all_platforms)
        player.draw(screen)
        all_platforms.draw(screen)
        ufo.update()
        ufo.draw(screen)
        pg.display.flip()
        clock.tick(60)
