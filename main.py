import json
import os

import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from button import Button, ButtonWithoutText, ButtonWithBG
from label import Label
from launch import launch
from make_screen import picture

pygame.init()
pygame.mixer.init()


def load_screen(size=(1280, 720)):
    if fullscreen_flag:
        return pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(size)


def fullscreen():
    global fullscreen_flag
    global cell
    global SCREEN
    fullscreen_flag = not fullscreen_flag
    cell.flag = not cell.flag
    SCREEN = load_screen()


with open('data/info/settings.json') as js_file:
    data = json.load(js_file)

volume, fullscreen_flag = data['volume'], data['fullscreen']

SCREEN = load_screen()

pygame.display.set_caption("MyGame")
clock = pygame.time.Clock()
FPS = 60

BG = pygame.image.load("data/images/rad2.jpg")

pygame.mixer.music.load('data/info/main.ogg')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(volume / 100)

options_buttons = []
cell = ButtonWithBG((880, 200), options_buttons, fullscreen,
                    pygame.image.load(f"data/images/cell.png"), pygame.image.load(f"data/images/cell_with_mark.png"),
                    flag=fullscreen_flag)
slider = Slider(SCREEN, 865, 300, 200, 20, min=0, max=100, step=1)
slider.setValue(volume)


def play(level):
    indicator, time = launch(SCREEN, level)
    if indicator is None:
        choose_level()
    elif indicator is True:
        play(level)
    else:
        win_menu(time, level)


def get_font(size):
    return pygame.font.Font("data/info/font.ttf", size)


def choose_level_left(is_moving):
    is_moving[0] = True
    is_moving[1] = 40
    is_moving[2] = 0


def choose_level_right(is_moving):
    is_moving[0] = True
    is_moving[1] = -20
    is_moving[2] = 0


def win_menu(time, level):
    win_menu_text = []
    Label("you win", (640, 75), win_menu_text, size=60)

    Label(f"your result is {time}", (640, 150), win_menu_text, size=45)
    with open('data/info/records.json') as file:
        data = json.load(file)
    if str(level) in data:
        data[str(level)] = min(data[str(level)], str(time))
    else:
        data[str(level)] = str(time)

    with open('data/info/records.json', 'w') as file:
        json.dump(data, file)

    win_menu_buttons = []
    Button("back", (640, 650), win_menu_buttons, choose_level, size=45)
    Button("retry", (640, 500), win_menu_buttons, lambda: play(level), size=45)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill("#3E64A3")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in win_menu_buttons:
                    button.click(pos=mouse_pos)
        for label in win_menu_text:
            label.blit(screen=SCREEN)

        for button in win_menu_buttons:
            button.update(SCREEN, mouse_pos)

        pygame.display.update()


def choose_level():
    choose_level_text = []
    Label("choose level", (640, 50), choose_level_text, size=45)

    choose_level_buttons = []
    Button("back", (640, 650), choose_level_buttons, main_menu, size=45)
    ButtonWithoutText((1030, 360), choose_level_buttons, choose_level_right,
                      pygame.image.load("data/images/white_right_arrow.png"),
                      pygame.image.load("data/images/gray_right_arrow.png"))
    ButtonWithoutText((250, 360), choose_level_buttons, choose_level_left,
                      pygame.image.load("data/images/white_left_arrow.png"),
                      pygame.image.load("data/images/gray_left_arrow.png"))
    with open('data/info/records.json') as file:
        data = json.load(file)
    unlock = len(data)

    levels_images = []
    p = len([f for f in os.listdir("data/levels/")
                        if os.path.isfile(os.path.join("data/levels/", f))])
    for i in range(p):
        # image = pygame.transform.scale(pygame.image.load(f"data/levels/level{i + 1}.png"), (640, 360))
        image = pygame.transform.scale(picture(i + 1), (640, 360))
        if i == 0:
            image_rect = image.get_rect(center=(640, 360))
        else:
            image_rect = image.get_rect(center=(1920, 360))
        levels_images.append([image, image_rect])

    now = 0
    is_moving = [False, 0, 0]
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("#3E64A3")
        for label in choose_level_text:
            label.blit(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in choose_level_buttons:
                    button.click(pos=mouse_pos, is_moving=is_moving)
                if not is_moving[0] and mouse_pos[0] - 320 in range(640) and mouse_pos[1] - 180 in range(360):
                    play(now + 1)

        if is_moving[1] > 0 and now == 0 or is_moving[1] < 0 and (unlock == now or now == p - 1):
            is_moving = [False, 0, 0]

        if not is_moving[0]:
            SCREEN.blit(levels_images[now][0], levels_images[now][1])
        else:
            levels_images[now][1][0] += is_moving[1] / 60
            SCREEN.blit(levels_images[now][0], levels_images[now][1])

            if is_moving[1] > 0:
                levels_images[now - 1][1][0] += (is_moving[1]) / 60
                SCREEN.blit(levels_images[now - 1][0], levels_images[now - 1][1])
            else:
                levels_images[now + 1][1][0] += is_moving[1] / 60
                SCREEN.blit(levels_images[now + 1][0], levels_images[now + 1][1])

            is_moving[2] += 1
            if is_moving[2] == 59:
                if is_moving[1] > 0:
                    levels_images[now][1] = levels_images[now][0].get_rect(center=(1920, 360))
                    now -= 1
                else:
                    levels_images[now][1] = levels_images[now][0].get_rect(center=(-640, 360))
                    now += 1
                levels_images[now][1] = levels_images[now][0].get_rect(center=(640, 360))
                is_moving = [False, 0, 0]
            elif is_moving[2] < 30:
                is_moving[1] += (is_moving[1] // abs(is_moving[1])) * 88
            else:
                is_moving[1] -= (is_moving[1] // abs(is_moving[1])) * 88

        for button in choose_level_buttons:
            button.update(SCREEN, mouse_pos)

        clock.tick(FPS)
        pygame.display.update()


def options():
    global options_buttons
    global volume
    options_text = []
    Label("options", (640, 50), options_text, size=45)
    Label("fullscreen", (580, 200), options_text, size=45)
    Label("volume", (580, 300), options_text, size=45)

    Button("back", (640, 650), options_buttons, main_menu, size=45)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("#3E64A3")

        for label in options_text:
            label.blit(SCREEN)

        for button in options_buttons:
            button.update(SCREEN, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('data/info/settings.json', 'w') as file:
                    json.dump({"volume": volume, "fullscreen": fullscreen_flag}, file)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in options_buttons:
                    button.click(pos=mouse_pos)

        pygame_widgets.update(pygame.event.get())
        volume = slider.getValue()

        pygame.mixer.music.set_volume(volume / 100)
        pygame.display.update()


def records():
    records_text = []
    Label("records", (640, 50), records_text, size=45)
    with open('data/info/records.json') as file:
        data = json.load(file)

    record_list = []
    start_pos = 60
    for key in data:
        Label(f'{key} level - {data[key]}', (490, start_pos + 50 * int(key)), record_list, size=30, flag=True)

    records_buttons = []
    Button("back", (640, 650), records_buttons, main_menu, size=45)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill("#3E64A3")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in records_buttons:
                    button.click(pos=mouse_pos)
            if event.type == pygame.MOUSEWHEEL:
                last = start_pos
                if start_pos - 10 * event.y <= 60:
                    start_pos -= 10 * event.y
                    for label in record_list:
                        label.move((label.rect.centerx, label.rect.centery + start_pos - last))

        for label in record_list:
            label.blit(screen=SCREEN)

        pygame.draw.rect(SCREEN, "#3E64A3", (0, 0, 1280, 90))
        pygame.draw.rect(SCREEN, "#3E64A3", (0, 620, 1280, 120))

        for label in records_text:
            label.blit(screen=SCREEN)

        for button in records_buttons:
            button.update(SCREEN, mouse_pos)

        pygame.display.update()


def main_menu():
    with open('data/info/settings.json', 'w') as file:
        json.dump({"volume": volume, "fullscreen": fullscreen_flag}, file)

    menu_text = []
    Label("main menu", (640, 100), menu_text)

    main_buttons = []
    Button("play", (640, 250), main_buttons,
           choose_level, hovering_color="#f3dfb2", size=60)
    Button("options", (640, 375), main_buttons,
           options, hovering_color="#f3dfb2", size=60)
    Button("records", (640, 500), main_buttons,
           records, hovering_color="#f3dfb2", size=60)
    Button("quit", (640, 625), main_buttons,
           sys.exit, hovering_color="#f3dfb2", size=60)
    while True:
        SCREEN.blit(BG, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        for label in menu_text:
            label.blit(screen=SCREEN)

        for button in main_buttons:
            button.update(SCREEN, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in main_buttons:
                    button.click(pos=mouse_pos)
        pygame.display.update()


if __name__ == "__main__":
    main_menu()
