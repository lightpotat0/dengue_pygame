from typing import Any
import pygame
from pygame.sprite import Group
import random

MOSQUITO_SPEED = 110

class Mosquito(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = 'spacedengue/graphics/' + color + '.png'
		self.image1 = pygame.image.load(file_path).convert_alpha()
		file_path2 = 'spacedengue/graphics/' + color + '_wing_down.png'
		self.image2 = pygame.image.load(file_path2).convert_alpha()
		self.image = self.image1
		self.rect = self.image.get_rect(topleft = (x,y))
		self.x = x
		self.tempo = random.random()

	def update(self, direction, delta):
		self.x += direction * MOSQUITO_SPEED * delta
		self.rect.x = self.x
		self.tempo += delta
		if self.tempo % 1.0 < 0.5:
			self.image = self.image1
		else:
			self.image = self.image2

class Extra(pygame.sprite.Sprite):
	def __init__(self,side,screen_width):
		super().__init__()
		#self.image = pygame.image.load("spacedengue/graphics/extra.png").convert_alpha()
		self.image = pygame.image.load("spacedengue/graphics/yellow.png").convert_alpha()

		if side == "right":
			x = screen_width + 50
			self.speed = -4
		else:
			x = -50
			self.speed = 4

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.speed