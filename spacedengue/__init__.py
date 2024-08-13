import pygame, sys
from spacedengue.player import Player
import spacedengue.obstacle

screen_width = 1280
screen_height = 720

class SpaceMinigame:
	def __init__(self):
		# Player Setup
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		# Obstacle Setup
		self.shape = obstacle.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obstacle_amount = 4
		self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 480)

		self.tela = pygame.Surface((screen_width, screen_height))

	def create_obstacle(self, x_start, y_start, offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index,col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstacle.Block(self.block_size,(241,79,80),x,y)
					self.blocks.add(block)

	def create_multiple_obstacles(self, x_start, y_start, *offset):
		for offset_x in offset:
			self.create_obstacle(x_start, y_start, offset_x)

	def frame(self, screen, delta, jogo):
		self.player.update()

		# render
		self.tela.fill("black")
		self.player.sprite.lasers.draw(self.tela)
		self.player.draw(self.tela)

		self.blocks.draw(self.tela)

		screen.blit(pygame.transform.scale(self.tela, screen.get_size()), (0, 0))
