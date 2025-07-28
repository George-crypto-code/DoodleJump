import pygame as pg

from system.button import Button
from system.system import get_background


class Options:
    def __init__(self):
        self.background = get_background("options/images/background/options_background.png")
        self.menu_button = Button()
        self.menu_button.setImage("options/images/buttons/menu.png", "options/images/buttons/menu_hover.png")
        self.menu_button.setSignal("menu")
        self.menu_button.setPosition(200, 500)

    def update(self):
        self.menu_button.update()

    def draw(self, screen):
        self.menu_button.draw(screen)

    def running(self, screen):
        clock = pg.time.Clock()
        while True:
            screen.blit(self.background, (0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    return "quit"
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if signal := self.menu_button.click():
                        return signal
            self.menu_button.update()
            self.menu_button.draw(screen)
            pg.display.flip()
            clock.tick(60)

