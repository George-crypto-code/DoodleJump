import pygame as pg
from button import Button
from system import get_background
from menu_player import MenuPlayer
from platform import Platform


class MainMenu:
    def __init__(self):
        self.background = get_background("data/background/main_menu_background.png")
        self.play_button = Button()
        self.play_button.setImage("data/buttons/play.png", "data/buttons/play_hover.png")
        self.play_button.setSignal("play")
        self.options_button = Button()
        self.options_button.setImage("data/buttons/options.png", "data/buttons/options_hover.png")
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
        all_platforms = pg.sprite.Group()
        platform = Platform(all_platforms)
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
            pg.display.flip()
            clock.tick(60)

