#MiniGame David
import pygame
from random import randint, choice

#Player Class
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		#Sprites
		self.image = pygame.image.load('walkminigame/Sprites/player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom=(120, 320))

#Obstacle Class
class Obstacle(pygame.sprite.Sprite):
	def __init__(self, object, minigame):
		super().__init__()

		self.minigame = minigame
		self.object = object

		object_images = {
			'down': 'walkminigame/Sprites/bucketdown.png',
			'up': 'walkminigame/Sprites/trashup.png',
			'right': 'walkminigame/Sprites/tireright.png'
		}

		self.image = pygame.image.load(object_images[object]).convert_alpha()
		self.rect = self.image.get_rect(midbottom=(300, 320))

	def update(self): #Update Obstacles
		keys = pygame.key.get_pressed()

		#Obstacles Directions Dictionary
		directions = {
			'down': pygame.K_DOWN,
			'up': pygame.K_UP,
			'right': pygame.K_RIGHT
		}

		#Obstacle Delet
		if self.object in directions and keys[directions[self.object]]:
			self.kill()
			self.minigame.kills += 1
			self.minigame.spawn = True

class WalkMinigame:
	def __init__(self):
		self.screen = pygame.Surface((1280, 720))
		self.spawn = True

		#Player
		self.player = pygame.sprite.GroupSingle()
		self.player.add(Player())

		#Obstacles
		self.obstacles = pygame.sprite.Group()
		self.kills = 0

		#Scenario
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
