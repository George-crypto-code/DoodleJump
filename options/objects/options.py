import pygame as pg

from config.button import Button
from config.system import get_background


def options(screen):
    background = get_background("options/images/background/options_background.png")
    menu_button = Button()
    menu_button.setImage("options/images/buttons/menu.png", "options/images/buttons/menu_hover.png")
    menu_button.setSignal("menu")
    menu_button.setPosition(200, 500)

    clock = pg.time.Clock()
    sound = pg.mixer.Sound("sounds/button.wav")

    while True:
        screen.blit(background, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return "quit"
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if signal := menu_button.click():
                    sound.play()
                    return signal
        menu_button.update()
        menu_button.draw(screen)
        pg.display.flip()
        clock.tick(60)

