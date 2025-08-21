from game.objects.main_game import main_game
from menu.objects.main_menu import main_menu
from options.objects.options import options
from config.system import *


def main():
    pg.init()
    pg.mixer.init()
    size = WIGHT, HEIGHT
    screen = pg.display.set_mode(size)
    player_running = False
    menu_running = True
    options_running = False

    while True:

        if menu_running:
            res = main_menu(screen)
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
            res = main_game(screen)
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

        if options_running:
            res = options(screen)
            if res == "menu":
                player_running = False
                menu_running = True
                options_running = False
            else:
                break

    pg.quit()


if __name__ == "__main__":
    main()
