from game.objects.player import Player  # doodle jump player model
from menu.objects.main_menu import MainMenu
from system.system import *


def main():
    pg.init()  # pg initialization
    size = WIGHT, HEIGHT  # window size
    screen = pg.display.set_mode(size)  # set siz on window
    player = Player()  # main player
    menu = MainMenu()

    player_running = False
    menu_running = True
    options_running = False

    while True:  # main cycle

        if menu_running:
            res = menu.run(screen)
            if res == "play":
                player_running = True
                menu_running = False
                options_running = False
            elif res == "options":
                player_running = False
                menu_running = False
                options_running = True
            else:
                break

        if player_running:
            res = player.running(screen)
            if res == "play":
                player_running = True
                menu_running = False
                options_running = False
            elif res == "menu":
                player_running = False
                menu_running = True
                options_running = False
            else:
                break


    pg.quit()  # turn off pygame


if __name__ == "__main__":
    main()
