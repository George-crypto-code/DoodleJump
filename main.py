from camera import Camera
from player import Player  # doodle jump player model
from system import *


def main():
    pg.init()  # pg initialization
    size = WIGHT, HEIGHT  # window size
    screen = pg.display.set_mode(size)  # set siz on window
    clock = pg.time.Clock()  # set time on main cycle

    all_platforms = pg.sprite.Group()
    Platform(all_platforms).setPlatform(70, 450)  # start platform will always place here
    player = Player()  # main player
    camera = Camera()

    background = get_background("data/background/background.png")
    bottom = get_bottom("data/background/bottom.png")

    running = True  # flag for stopping main cycle
    while running:  # main cycle

        screen.blit(background, (0, 0))
        set_platforms(all_platforms)  # set and delete some amount of platforms

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

            if event.type == pg.USEREVENT:
                player.stopJump()  # event for stop jumping animation

        player.update(all_platforms)  # update speed and collision
        all_platforms.draw(screen)  # draw all platforms
        player.draw(screen)  # draw player

        camera.update(player)  # watch for player
        for platform in all_platforms:
            camera.apply(platform)

        screen.blit(bottom, (0, HEIGHT - bottom.get_height()))

        pg.display.flip()  # change display picture
        clock.tick(200)  # set fps

    pg.quit()  # turn off pygame


if __name__ == "__main__":
    main()
