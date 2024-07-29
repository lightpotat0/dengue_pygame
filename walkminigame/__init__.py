#MiniGame David
import pygame
from random import randint, choice
from sys import exit

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		#Sprites
		self.image = pygame.image.load('walkminigame/Sprites/player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom=(120, 320))

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,object, minigame):
		super().__init__()

		self.minigame = minigame
		self.object = object

		if object == 'down':
			self.image = pygame.image.load('walkminigame/Sprites/down.png').convert_alpha()
		elif object == 'up':
			self.image = pygame.image.load('walkminigame/Sprites/up.png').convert_alpha()
		elif object == 'right':
			self.image = pygame.image.load('walkminigame/Sprites/right.png').convert_alpha()

		self.rect = self.image.get_rect(midbottom=(300, 320))

	def update(self):
		keys = pygame.key.get_pressed()
		if self.object == 'down' and keys[pygame.K_DOWN]:
			self.kill()
			self.minigame.kills += 1
			self.minigame.spawn = True
		if self.object == 'up' and keys[pygame.K_UP]:
			self.kill()
			self.minigame.kills += 1
			self.minigame.spawn = True
		if self.object == 'right' and keys[pygame.K_RIGHT]:
			self.kill()
			self.minigame.kills += 1
			self.minigame.spawn = True

class WalkMinigame:
	def __init__(self):
		self.screen = pygame.Surface((1280, 720))
		self.spawn = True
		self.player = pygame.sprite.GroupSingle()
		self.player.add(Player())

		self.obstacles = pygame.sprite.Group()
		self.kills = 0

		self.ground = pygame.image.load('walkminigame/Sprites/ground.png').convert()
		self.groundrect = self.ground.get_rect(bottomleft = (0,720))

	def frame(self, screen, delta, jogo):
		if self.kills >= 10:
			self.spawn = False
		if self.spawn:
			self.obstacles.add(Obstacle(choice(['up', 'down', 'right']), self))
			self.spawn = False

		self.screen.fill('Blue')
		self.screen.blit(self.ground, self.groundrect)

		self.player.draw(self.screen)

		self.obstacles.draw(self.screen)
		self.obstacles.update()
		screen.blit(pygame.transform.scale(self.screen, screen.get_size()), (0, 0))
		if self.kills >= 10:
			return "ganhou"
