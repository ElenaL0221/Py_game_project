import json
import pygame
import const
import platform


def picture(k):
    screen = pygame.Surface((const.WIN_WIDTH, const.WIN_HEIGHT))

    with open(f'data/levels/{k}.json', 'r') as file:
        file = json.load(file)
        platform_size = file['PLATFORM_SIZE']
        level = file["LEVEL"]
        exit_position = file["EXIT_POSITION"]
    objects = []

    bg = pygame.Surface((const.WIN_WIDTH, const.WIN_HEIGHT))
    bg.fill(pygame.Color(const.BLACK))
    const.PLATFORM_WIDTH = const.PLATFORM_HEIGHT = platform_size
    for row in level:
        name, pl_x, pl_y, color_platform = row
        x, y = pl_x * const.PLATFORM_WIDTH, pl_y * const.PLATFORM_HEIGHT
        if name == 'p':
            objects.append(platform.Platform(x, y, color_platform))
        if name == 'b':
            objects.append(platform.Box(x, y, color_platform))
        if name == 't':
            objects.append(platform.Thorns(x, y + const.PLATFORM_HEIGHT // 2, color_platform))

    exit_x, exit_y = exit_position
    ex = platform.Exit(exit_x * const.PLATFORM_WIDTH, (exit_y - 1) * const.PLATFORM_HEIGHT)  # один выход на уровень
    objects.append(ex)
    screen.blit(bg, (0, 0))
    for ob in objects:
        if ob.rect.right >= 0 and ob.rect.left <= const.WIN_WIDTH:
            screen.blit(ob.image, (ob.rect.x, ob.rect.y))
    return screen
