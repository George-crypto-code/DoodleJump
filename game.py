from player import Player
from main_menu import MainMenu


class Game:
    def __init__(self):
        self.player_running = False
        self.menu_running = True
        self.options_running = False

    def running(self):
