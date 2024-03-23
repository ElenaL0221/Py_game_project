import datetime
import sys
import pygame
import const
import player
import platform
import menu
import camera

from label import Label
from button import Button, ButtonWithBG


running = True


def game_menu(screen):
    global running
    running = True
    surface = pygame.Surface((1280, 720))
    surface.blit(pygame.image.load("data/images/rad2.jpg"), (0, 0))
    surface = pygame.transform.scale(surface, (960, 540))
    w = 8
    pygame.draw.rect(surface, const.BLACK, (0, 0, 960, 540), w)
    pos = (160, 90)

    labels = []
    Label('pause', (640, 150), labels, size=75)
    buttons = []
    Button('continue', (640, 350), buttons, cont, size=50)
    Button('retry', (640, 450), buttons, retry, size=50)
    Button('menu', (640, 550), buttons, level_choose, size=50)

    while type(running) != type(1):
        mouse_pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for button in buttons:
                    button.click(pos=mouse_pos)
        screen.blit(surface, pos)
        for label in labels:
            label.blit(screen)
        for button in buttons:
            button.update(screen, mouse_pos)
        pygame.display.flip()

    return running


def cont():
    global running
    running = 1


def retry():
    global running
    running = 2


def level_choose():
    global running
    running = 3


def main(screen, player_pos, platform_size, level, exit_position):
    pygame.init()
    start = datetime.datetime.now()
    timer = pygame.time.Clock()

    left = right = up = False
    colors = {1: '#ff3a3a', 2: '#8a8d91', 3: '#dbff43', 4: '#ec46ff', 5: '#52fff8', 6: '#41ff4f'}

    objects = []
    platforms = []
    boxes = []
    thorns = []
    maxx = 0
    hero = player.Player(*player_pos)
    bg = pygame.Surface((const.WIN_WIDTH, const.WIN_HEIGHT))
    bg.fill(pygame.Color(const.BACKGROUND_COLOR))
    const.PLATFORM_WIDTH = const.PLATFORM_HEIGHT = platform_size
    for row in level:
        name, pl_x, pl_y, color_platform = row
        x, y = pl_x * const.PLATFORM_WIDTH, pl_y * const.PLATFORM_HEIGHT
        if name == 'p':
            pf = platform.Platform(x, y, color_platform)
            objects.append(pf)
            platforms.append(pf)
        if name == 'b':
            b = platform.Box(x, y, color_platform)
            objects.append(b)
            boxes.append(b)
        if name == 't':
            t = platform.Thorns(x, y + const.PLATFORM_HEIGHT // 2, color_platform)
            objects.append(t)
            thorns.append(t)

        maxx = max(maxx, x)

    exit_x, exit_y = exit_position
    ex = platform.Exit(exit_x * const.PLATFORM_WIDTH, (exit_y - 1) * const.PLATFORM_HEIGHT)  # один выход на уровень
    objects.append(ex)

    mx = my = 0
    change_color = False
    cam = camera.Camera(maxx, const.WIN_WIDTH, const.WIN_HEIGHT)

    buttons = []
    ButtonWithBG((1245, 50), buttons, lambda: game_menu(screen),
                 pygame.image.load("data/images/pause.png"), pygame.image.load("data/images/pause.png"))

    while True:
        timer.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.KEYDOWN and (e.key == pygame.K_a or e.key == pygame.K_LEFT):
                left = True
            if e.type == pygame.KEYDOWN and (e.key == pygame.K_d or e.key == pygame.K_RIGHT):
                right = True
            if e.type == pygame.KEYDOWN and (e.key == pygame.K_w or e.key == pygame.K_UP):
                up = True

            if e.type == pygame.KEYUP and (e.key == pygame.K_d or e.key == pygame.K_RIGHT):
                right = False
            if e.type == pygame.KEYUP and (e.key == pygame.K_a or e.key == pygame.K_LEFT):
                left = False
            if e.type == pygame.KEYUP and (e.key == pygame.K_w or e.key == pygame.K_UP):
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                m_s = datetime.datetime.now()
                f = game_menu(screen)
                if f == 3:
                    return None, None
                elif f == 2:
                    return True, None

                m_e = datetime.datetime.now()
                start += (m_e - m_s)

            if e.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    m_s = datetime.datetime.now()
                    f = button.click(pos=mouse_pos)
                    if f == 3:
                        return None, None
                    elif f == 2:
                        return True, None
                    elif f == 1:
                        m_e = datetime.datetime.now()
                        start += (m_e - m_s)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                mx, my = pygame.mouse.get_pos()
                change_color = (mx, my)
            if e.type == pygame.MOUSEBUTTONUP and e.button == 3:
                x, y = pygame.mouse.get_pos()
                dx, dy = x - mx, my - y
                change = 0
                if 0 <= dy < dx * 3 ** 0.5:
                    change = 1
                if dy > -dx * 3 ** 0.5 and dy >= dx * 3 ** 0.5:
                    change = 2
                if 0 < dy <= -dx * 3 ** 0.5:
                    change = 3
                if dx * 3 ** 0.5 < dy <= 0:
                    change = 4
                if dy <= dx * 3 ** 0.5 and dy < -dx * 3 ** 0.5:
                    change = 5
                if -dx * 3 ** 0.5 <= dy < 0:
                    change = 6
                if change in colors and not pygame.sprite.spritecollide(hero, objects, False):
                    const.BACKGROUND_COLOR = colors[change]
                bg.fill(pygame.Color(const.BACKGROUND_COLOR))
                change_color = False

        screen.blit(bg, (0, 0))

        # entities.draw(screen)
        hero.update(left, right, up, platforms)
        [box.update(objects, hero) for box in boxes]
        if pygame.sprite.collide_rect(hero, ex):
            end = datetime.datetime.now()
            return False, end - start
        for t in thorns:
            if pygame.sprite.collide_rect(t, hero) and t.color != const.BACKGROUND_COLOR:
                return True, None

        cam.draw(screen, hero, objects)
        if change_color:
            menu.change_color_draw(screen, change_color)

        for button in buttons:
            button.update(screen, mouse_pos)

        pygame.display.flip()
