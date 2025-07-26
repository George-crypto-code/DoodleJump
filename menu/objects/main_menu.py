import pygame as pg
from system.button import Button
from system.system import get_background
from menu.objects.menu_player import MenuPlayer
from menu.objects.menu_platform import MenuPlatform
from menu.objects.ufo import UFO


class MainMenu:
    def __init__(self):
        self.background = get_background("menu/images/background/main_menu_background.png")
        self.play_button = Button()
        self.play_button.setImage("menu/images/button/play.png", "menu/images/button/play_hover.png")
        self.play_button.setSignal("play")
        self.options_button = Button()
        self.options_button.setImage("menu/images/button/options.png", "menu/images/button/options_hover.png")
        self.options_button.setSignal("options")

    def update(self):
        self.play_button.update()
        self.options_button.update()

    def draw(self, screen):
        self.play_button.draw(screen)
        self.options_button.draw(screen)

    def run(self, screen):
        self.play_button.setPosition(140, 200)
        self.options_button.setPosition(140, 270)

        clock = pg.time.Clock()
        player = MenuPlayer()
        ufo = UFO()
        all_platforms = pg.sprite.Group()
        platform = MenuPlatform(all_platforms)
        platform.setPlatform(80, 450)

        while True:

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    return "quit"
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if signal := self.play_button.click():
                        return signal
                    if signal := self.options_button.click():
                        return signal
                if event.type == pg.USEREVENT:
                    player.stopJump()

            screen.blit(self.background, (0, 0))
            self.update()
            self.draw(screen)
            player.update(all_platforms)
            player.draw(screen)
            all_platforms.draw(screen)
            ufo.update()
            ufo.draw(screen)
            pg.display.flip()
            clock.tick(60)

