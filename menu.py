import pygame


def change_color_draw(screen, xy):
    x, y = xy
    n = 300
    screen.blit(pygame.image.load('data/images/круг.png'), (x - n / 2, y - n / 2))