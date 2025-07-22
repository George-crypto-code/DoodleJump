import pygame as pg  # main library

from player import Player  # doodle jump player model


def main():
    pg.init()  # pg initialization
    size = width, height = 800, 600  # window size
    screen = pg.display.set_mode(size)  # set siz on window
    clock = pg.time.Clock()  # set time on main cycle

    all_sprites = pg.sprite.Group()  # player, platforms, monsters(maybe) sprites
    player = Player(all_sprites)  # main player

    running = True  # flag for stopping main cycle
    while running:  # main cycle

        for event in pg.event.get():  # get all events at the moment

            if event.type == pg.QUIT:  # if user click on close button
                running = False  # cycle stop
                break

            if event.type == pg.KEYDOWN:  # get all pressed keys
                if event.key == pg.K_d:
                    player.setDirection("right")  # flip right player model
                    player.movingRight()  # moving right while button will not be press
                if event.key == pg.K_a:
                    player.setDirection("left")  # flip left player model
                    player.movingLeft()  # moving left while button will not be press

            if event.type == pg.KEYUP:  # get all released keys
                if event.key == pg.K_d or event.key == pg.K_a:
                    player.stopMoving()  # stop moving if any key released

        screen.fill((255, 255, 255))  # fill the screen white

        all_sprites.update()  # update all sprites
        all_sprites.draw(screen)  # draw all sprites

        pg.display.flip()  # change display picture
        clock.tick(60)  # set fps

    pg.quit()  # turn off pygame


if __name__ == "__main__":
    main()
