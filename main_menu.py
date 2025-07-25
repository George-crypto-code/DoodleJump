import pygame as pg
from button import Button


class MainMenu:
    def __init__(self):
        self.background = pg.image.load("data/background/main_menu_background.png")
        self.play_button = Button()
        self.play_button.setImage("data/buttons/play.png", "data/buttons/play_hover.png")
        self.options_button = Button()
        self.options_button.setImage("data/buttons/options.png", "data/buttons/options_hover.png")

    def update(self):
        self.play_button.update()
        self.options_button.update()

    def draw(self, screen):
        self.play_button.draw(screen)
        self.options_button.draw(screen)
