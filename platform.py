import pygame
import const

pygame.mixer.init()
splash = pygame.mixer.Sound('data/info/slime.ogg')
splash.set_volume(0.1)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color=const.BLACK):
        pygame.sprite.Sprite.__init__(self)
        if color == '#630321':
            self.image = pygame.transform.scale(pygame.image.load('data/images/break.png'),
                                                (const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT))
        else:
            image = pygame.transform.scale(pygame.image.load('data/images/break_lines.png'),
                                           (const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT))
            self.image = pygame.Surface((const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT))
            self.image.fill(pygame.Color(color))
            self.image.blit(image, (0, 0))
        self.rect = pygame.Rect(x, y, const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT)
        self.color = color


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, color=const.BOX_COLOR):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT))
        self.image.fill(color)
        image = pygame.transform.scale(pygame.image.load("data/images/box.png"), (const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT))
        self.image.blit(image, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT)
        self.yvel = 0
        self.xvel = 0
        self.color = color
        self.onGround = False

    def update(self, platforms, Class_player):
        if self.color != const.BACKGROUND_COLOR and self.rect.top <= const.WIN_HEIGHT + const.PLATFORM_HEIGHT:
            if not self.onGround:
                self.yvel += const.GRAVITY
            self.rect.y += int(self.yvel)
            self.collide(platforms, Class_player)
            self.move(platforms, Class_player)
            self.collide(platforms, Class_player)

    def collide(self, platforms, player):
        for p in platforms:
            if p != self and p.color != const.BACKGROUND_COLOR and pygame.sprite.collide_rect(self, p):
                flag = False
                if p.rect.top <= self.rect.bottom <= p.rect.top + const.JUMP_POWER and pygame.sprite.collide_rect(self, p):
                    self.rect.bottom = p.rect.top

                    self.yvel = 0
                    flag = True

                if p.rect.bottom <= self.rect.top <= p.rect.bottom + const.JUMP_POWER and pygame.sprite.collide_rect(self, p):
                    self.rect.top = p.rect.bottom

                    self.yvel = 0
                    flag = True

                if p.rect.left <= self.rect.right <= p.rect.left + const.MOVE_SPEED and pygame.sprite.collide_rect(self, p):
                    self.rect.right = p.rect.left
                    player.rect.right = self.rect.left
                    player.xvel = 0
                    flag = True

                if p.rect.right - const.MOVE_SPEED <= self.rect.left <= p.rect.right and pygame.sprite.collide_rect(self, p):
                    self.rect.left = p.rect.right
                    player.rect.left = self.rect.right
                    player.xvel = 0
                    flag = True
                if flag:
                    break

    def move(self, platforms, Class_player):
        if self.color != const.BACKGROUND_COLOR and pygame.sprite.collide_rect(self, Class_player):
            if self.color != const.BACKGROUND_COLOR:
                if self.rect.top <= Class_player.rect.bottom <= self.rect.top + Class_player.yvel and Class_player.yvel > 0:
                    Class_player.rect.bottom = self.rect.top
                    Class_player.onGround = True
                    if int(Class_player.yvel) > 1:
                        splash.play()
                    Class_player.yvel = 0
                elif Class_player.rect.top <= self.rect.bottom <= Class_player.rect.top + self.yvel or \
                        Class_player.rect.top <= self.rect.bottom <= Class_player.rect.top - Class_player.yvel:
                    self.rect.bottom = Class_player.rect.top
                    self.yvel = Class_player.yvel
                else:
                    if Class_player.xvel < 0:
                        self.rect.right = Class_player.rect.left
                    else:
                        self.rect.left = Class_player.rect.right
                    self.collide(platforms, Class_player)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, color=const.BLUE):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("data/images/door.png"),
                                            (const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT * 2))
        self.rect = pygame.Rect(x, y, const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT * 2)
        self.color = color


class Thorns(pygame.sprite.Sprite):
    def __init__(self, x, y, color=const.BLUE):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT // 2))
        pygame.draw.polygon(self.image, color, [(0, const.PLATFORM_HEIGHT // 2), (const.PLATFORM_WIDTH // 2, const.PLATFORM_HEIGHT // 2),
                                                [const.PLATFORM_WIDTH / 4, 0]])
        pygame.draw.polygon(self.image, color, [(const.PLATFORM_WIDTH // 2, const.PLATFORM_HEIGHT // 2), (const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT // 2),
                                                [const.PLATFORM_WIDTH * 3 / 4, 0]])

        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = pygame.Rect(x, y, const.PLATFORM_WIDTH, const.PLATFORM_HEIGHT // 2)
        self.color = color
