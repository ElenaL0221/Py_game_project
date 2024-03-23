import pygame

class Label:
    def __init__(self, text, pos, text_list, size=100, color='#FFFFFF', flag=False):
        self.pos = pos
        self.font = pygame.font.Font("data/info/font.ttf", size)
        self.text = text
        self.color = color
        self.out = self.font.render(text, True, color)
        if flag:
            self.rect = pos
        else:
            self.rect = self.out.get_rect(center=pos)
        text_list.append(self)

    def blit(self, screen):
        screen.blit(self.out, self.rect)

    def change_text(self, text):
        self.text = text
        self.out = self.font.render(text, True, self.color)
        self.rect = self.out.get_rect(center=self.pos)

    def move(self, pos):
        self.rect = self.out.get_rect(center=pos)