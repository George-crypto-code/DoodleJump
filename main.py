from game.objects.main_game import main_game
from menu.objects.main_menu import MainMenu
from options.objects.options import Options
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
            menu = MainMenu()
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
            options = Options()
            res = options.running(screen)
            if res == "menu":
                player_running = False
                menu_running = True
                options_running = False
            else:
                break

    pg.quit()


if __name__ == "__main__":
    main()
