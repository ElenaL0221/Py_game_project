import pygame
import const

import pygame


pygame.mixer.init()
splash = pygame.mixer.Sound('data/info/slime.ogg')
splash.set_volume(0.1)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((const.WIDTH, const.HEIGHT))
        self.image.blit(pygame.transform.scale(pygame.image.load('data/images/player.png'),
                                               (const.WIDTH, const.HEIGHT)), (0, 0))

        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.yvel = 0
        self.onGround = False

    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:
                self.yvel = -const.JUMP_POWER
        if left:
            self.xvel = max(self.xvel - const.ACCELERATION, -const.MOVE_SPEED)

        if right:
            self.xvel = min(self.xvel + const.ACCELERATION, const.MOVE_SPEED)

        if not (left or right):
            if self.xvel > 0:
                self.xvel = max(0, self.xvel - const.SLOW_DOWN)
            else:
                self.xvel = min(0, self.xvel + const.SLOW_DOWN)
        if not self.onGround:
            self.yvel += const.GRAVITY

        self.onGround = False
        self.rect.y += int(self.yvel)
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p) and p.color != const.BACKGROUND_COLOR:

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    if int(self.yvel) > 1:
                        splash.play()
                    self.yvel = 0


                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0