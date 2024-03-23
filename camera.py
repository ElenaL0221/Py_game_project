import const


class Camera:
    def __init__(self, maxx, w, h):
        self.x = maxx
        self.width = w
        self.height = h

    def draw(self, screen, hero, objects):
        hero_x, hero_y = hero.rect.center
        left = 0
        if self.x > const.WIN_WIDTH:
            if self.width / 2 <= hero_x <= self.x - self.width / 2:
                left = hero_x - self.width / 2
            if 0 <= hero_x < self.width / 2:
                left = 0
            if self.x - self.width / 2 < hero_x <= self.x:
                left = self.x - self.width

        for ob in objects:
            if ob.rect.right >= left and ob.rect.left <= left + self.width and ob.rect.top <= const.WIN_HEIGHT \
                    and ob.color != const.BACKGROUND_COLOR:
                screen.blit(ob.image, (ob.rect.x - left, ob.rect.y))
        screen.blit(hero.image, (hero.rect.x - left, hero.rect.y))
