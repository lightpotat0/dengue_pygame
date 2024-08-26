from typing import Any
import pygame
from pygame.sprite import Group

class Mosquito(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = 'spacedengue/graphics/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,direction):
		self.rect.x += direction


class Extra(pygame.sprite.Sprite):
	def __init__(self,side,screen_width):
		super().__init__()
		#self.image = pygame.image.load("spacedengue/graphics/extra.png").convert_alpha()
		self.image = pygame.image.load("spacedengue/graphics/yellow.png").convert_alpha()

		if side == "right":
			x = screen_width + 50
			self.speed = -5
		else:
			x = -50
			self.speed = 5

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.speed