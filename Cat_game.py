import pygame as pg
import sys

from sprites import *
screen = pg.display.set_mode((1000, 600))
game = True

dimension_num = 0
clock = pg.time.Clock()
player = pg.image.load('cat_right1.png')
walk_right = [pg.transform.scale(pg.image.load('cat_right1.png'), (100, 80)), pg.transform.scale(pg.image.load('cat_right2.png'), (100, 80)), pg.transform.scale(pg.image.load('cat_right3.png'), (100, 80)), pg.transform.scale(pg.image.load('cat_right4.png'), (100, 80))]
walk_left = [pg.transform.scale(pg.image.load('cat_left1.png'), (100, 80)), pg.transform.scale(pg.image.load('cat_left2.png'), (100, 80)), pg.transform.scale(pg.image.load('cat_left3.png'), (100, 80)), pg.transform.scale(pg.image.load('cat_left4.png'), (100, 80))]
player = pg.transform.scale(player, (100, 80))
running = True


dimensions = [void(screen), forest(screen), sun(screen)]
while game:
    dimension = dimensions[dimension_num]
    screen.fill('black')
    screen.blit(dimension.bg, (0, 0))
    dimension_num = dimension.update()
    pg.display.update()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            sys.exit()
    clock.tick(10)