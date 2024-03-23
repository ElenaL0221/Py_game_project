import pygame


pygame.mixer.init()
click = pygame.mixer.Sound('data/info/click.ogg')
click.set_volume(0.05)


class Button:
	def __init__(self, text, pos, but_list, func, size=75, base_color='#FFFFFF', hovering_color='green'):
		self.x_pos, self.y_pos = pos
		self.font = pygame.font.Font("data/info/font.ttf", size)
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text
		self.text = self.font.render(self.text_input, True, self.base_color)
		self.image = self.text
		self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		but_list.append(self)
		self.func = func

	def update(self, screen, pos):
		self.hover(pos)
		screen.blit(self.text, self.rect)

	def is_cursor_on_button(self, pos):
		return pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom)

	def hover(self, pos):
		if self.is_cursor_on_button(pos):
			color = self.hovering_color

		else:
			color = self.base_color
		self.text = self.font.render(self.text_input, True, color)

	def click(self, **kwargs):
		if self.is_cursor_on_button(kwargs['pos']):
			click.play()
			return self.func()


class ButtonWithoutText(pygame.sprite.Sprite):
	def __init__(self, pos, but_list, func, image_stand, image_hold):
		pygame.sprite.Sprite.__init__(self)
		self.x_pos, self.y_pos = pos
		self.image_stand = image_stand
		self.image_hold = image_hold
		self.image = self.image_stand
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		but_list.append(self)
		self.func = func

	def update(self, screen, pos):
		self.hover(pos)
		screen.blit(self.image, self.rect)

	def hover(self, pos):
		if self.is_cursor_on_button(pos):
			self.image = self.image_hold
		else:
			self.image = self.image_stand
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

	def is_cursor_on_button(self, pos):
		cursor = Cursor(pos)
		return pygame.sprite.collide_mask(self, cursor)

	def click(self, **kwargs):
		if self.is_cursor_on_button(kwargs['pos']):
			click.play()
			if 'is_moving' in kwargs and not kwargs['is_moving'][0]:
				self.func(kwargs['is_moving'])
			elif 'is_moving' not in kwargs:
				return self.func()


class ButtonWithBG(ButtonWithoutText):
	def __init__(self, pos, but_list, func, image_stand, image_hold, flag=False):
		super().__init__(pos, but_list, func, image_stand, image_hold)
		self.flag = flag

	def is_cursor_on_button(self, pos):
		ans = (pos[0] - self.x_pos + self.image.get_rect()[2] / 2 in range(self.image.get_rect()[2]) and
				pos[1] - self.y_pos + self.image.get_rect()[3] / 2 in range(self.image.get_rect()[3]))
		return ans

	def update(self, screen, pos):
		if self.flag:
			self.image = self.image_hold
		else:
			self.image = self.image_stand
		screen.blit(self.image, self.rect)


class Cursor(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((1, 1))
		self.rect = self.image.get_rect(center=pos)
