import json
import os
import sys
import pygame
import const
import label

width = const.WIN_WIDTH + 100
height = const.WIN_HEIGHT + 100
but = {0: 'DELETE', 1: 'BOX', 2: 'PLATFORM', 3: 'EXIT', 4: 'THORNS', 5: 'PLAYER'}
objects = set()


def draw_menu(screen):
    global width, height
    pygame.draw.rect(screen, const.WHITE, (0, height - 100, width, 100))
    pygame.draw.rect(screen, const.WHITE, (width - 100, 0, width, height))
    [pygame.draw.rect(screen, eval(f'const.COL{x + 1}'), (25 + 100 * x, height - 75, 50, 50)) for x in range(7)]
    [pygame.draw.rect(screen, const.BLUE, (width - 75, 25 + 100 * x, 50, 50)) for x in range(6)]

    if color is not None:
        pygame.draw.rect(screen, color, (825, height - 75, 50, 50))
    if ob_type is not None:
        pygame.draw.rect(screen, const.BLUE, (width - 75, 725, 50, 50))


def exit(d, player_position, exit_position):
    pygame.quit()
    lvl = []
    for it in d:
        for predmet in d[it]:
            name_x = it[0]
            pos_x, pos_y, color_ob = predmet
            lvl.append((name_x, pos_x, pos_y, color_ob))
    dictionary = {"LEVEL": lvl, "PLATFORM_SIZE": pl_size,
                  "PLAYER_POSITION": player_position, "EXIT_POSITION": exit_position}
    with open(f'''data/levels/{len([f for f in os.listdir("data/levels/") 
        if os.path.isfile(os.path.join("data/levels/", f))]) + 1}.json''', 'w') as js_file:
        json.dump(dictionary, js_file)

    sys.exit()


pygame.init()
screen = pygame.display.set_mode((width, height))  # , pygame.FULLSCREEN)

bg = pygame.Surface((width, height))
bg.fill(pygame.Color(const.BLACK))
color = None
ob_type = None

pl_size = int(input())
# pl_size = 32

d = {'platforms': set(), 'boxes': set(), 'thorns': set()}
ex = None
player = None

texst = []
[label.Label(but[x].lower(), (width - 50, 50 + 100 * x), texst, 10, const.BLACK) for x in range(6)]
lab = label.Label('', (width - 50, 750), texst, 10, const.BLACK)
p = label.Label('p', (pl_size / 2, pl_size / 2), [], 10)
b = label.Label('b', (pl_size / 2, pl_size / 2), [], 10)
e = label.Label('e', (pl_size / 2, pl_size), [], 10)
t = label.Label('t', (pl_size / 2, pl_size / 4), [], 10)

now_x = 0
mbd = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(d, player, ex)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or mbd:
            mbd = True
            x, y = pygame.mouse.get_pos()
            for i in range(7):
                if 25 + 100 * i <= x <= 75 + 100 * i and height - 75 <= y <= height - 25:
                    color = eval(f'const.COL{i + 1}')
                if width - 75 <= x <= width - 25 and 25 + 100 * i <= y <= 75 + 100 * y:
                    if i < 6:
                        ob_type = but[i]
            if x <= width - 100 and y <= height - 100 and color is not None and ob_type is not None:
                pl_x, pl_y = (now_x + x) // pl_size, y // pl_size
                if ob_type == 'BOX' and (pl_x, pl_y) not in objects:
                    d['boxes'].add((pl_x, pl_y, color))
                    objects.add((pl_x, pl_y))
                if ob_type == 'PLATFORM' and (pl_x, pl_y) not in objects:
                    d['platforms'].add((pl_x, pl_y, color))
                    objects.add((pl_x, pl_y))
                if ob_type == 'THORNS' and (pl_x, pl_y) not in objects:
                    d['thorns'].add((pl_x, pl_y, color))
                    objects.add((pl_x, pl_y))

            if x <= width - 100 and pl_size <= y <= height - 100 and ob_type == 'EXIT':
                pl_x, pl_y = (now_x + x) // pl_size, y // pl_size
                if (pl_x, pl_y) not in objects:
                    if ex is not None:
                        px, py = ex
                        objects.remove((px, py))
                        objects.remove((px, py - 1))
                    ex = (pl_x, pl_y)
                    objects.add((pl_x, pl_y))
                    objects.add((pl_x, pl_y - 1))
            if x <= width - 100 and y <= height - 100:
                if ob_type == 'PLAYER':
                    player = (x + now_x, y)
                if ob_type == 'DELETE':
                    flag = True
                    mx, my = (now_x + x) // pl_size, y // pl_size
                    for i in d['platforms']:
                        pl_x, pl_y, _ = i
                        if mx == pl_x and my == pl_y:
                            d['platforms'].remove(i)
                            objects.remove((pl_x, pl_y))
                            flag = False
                            break
                    if flag:
                        for i in d['boxes']:
                            pl_x, pl_y, _ = i
                            if mx == pl_x and my == pl_y:
                                d['boxes'].remove(i)
                                objects.remove((pl_x, pl_y))
                                flag = False
                                break
                        if flag:
                            for i in d['thorns']:
                                pl_x, pl_y, _ = i
                                if mx == pl_x and my == pl_y:
                                    d['thorns'].remove(i)
                                    objects.remove((pl_x, pl_y))
                                    flag = False
                                    break
                                if flag:
                                    if ex is not None:
                                        pl_x, pl_y = ex
                                        if pl_x == mx and pl_y == my:
                                            ex = None
                                            objects.remove((pl_x, pl_y))
                                            flag = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mbd = False
        if event.type == pygame.MOUSEWHEEL:
            now_x = max(0, now_x - 10 * event.y)

    screen.blit(bg, (0, 0))
    for item in d:
        for ob in d[item]:
            pl_x, pl_y, color_pl = ob
            if item == 'thorns':
                tile_obj = pygame.Surface((pl_size, pl_size // 2))
            else:
                tile_obj = pygame.Surface((pl_size, pl_size))
            tile_obj.fill(color_pl)
            name = item[0]
            eval(name).blit(tile_obj)
            if item == 'thorns':
                screen.blit(tile_obj, (pl_x * pl_size - now_x, pl_y * pl_size + pl_size // 2))
            else:
                screen.blit(tile_obj, (pl_x * pl_size - now_x, pl_y * pl_size))
    if ex is not None:
        pl_x, pl_y = ex
        tile_ex = pygame.Surface((pl_size, pl_size * 2))
        tile_ex.fill(const.BLUE)
        e.blit(tile_ex)
        screen.blit(tile_ex, (pl_x * pl_size - now_x, (pl_y - 1) * pl_size))
    if player is not None:
        player_x, player_y = player
        tile_ex = pygame.Surface((const.WIDTH, const.HEIGHT))
        tile_ex.fill(const.WHITE)
        p.blit(tile_ex)
        screen.blit(tile_ex, (player_x - now_x, player_y - 1))

    draw_menu(screen)
    if ob_type is not None:
        lab.change_text(ob_type)
    for text in texst:
        text.blit(screen)
    pygame.display.flip()
