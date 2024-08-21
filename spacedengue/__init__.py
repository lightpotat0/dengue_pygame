import pygame, sys
from spacedengue.player import Player
import spacedengue.obstacle
from spacedengue.mosquitalien import Mosquito, Extra
from random import choice
from laser import Laser
from random import randint
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
		self.create_multiple_obstacles(x_start = screen_width / 15, y_start = 480, *self.obstacle_x_positions)

		self.tela = pygame.Surface((screen_width, screen_height))

		#Mosquito setup
		self.mosquitos = pygame.sprite.Group()
		self.mosquito_lasers = pygame.sprite.Group()
		self.mosquito_setup(rows = 6, cols = 8)
		self.mosquito_direction = 1

		#Extra Setup
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(400,800)

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

	def mosquito_setup(self,rows,cols,x_distance = 60,y_distance = 48, x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset

				if row_index == 0: mosquito_sprite = Mosquito("yellow",x,y)
				elif 1 <= row_index <= 2: mosquito_sprite = Mosquito("green",x,y)
				else: mosquito_sprite = Mosquito("red",x,y)
				self.mosquitalien.add(mosquito_sprite)

	def mosquito_position_checker(self):
		all_mosquitos = self.mosquitos.sprites()
		for mosquito in all_mosquitos:
			if mosquito.rect.right >= screen_height:
				self.alien_direction = -1
				self.mosquito_move_down(2)
			elif mosquito.rect.left <= 0:
				self.mosquito_direction = 1
				self.mosquito_move_down(2)

	def mosquito_move_down(self,distance):
		if self.mosquitos:
			for mosquito in self.mosquitos.sprites():
				mosquito.rect.y += distance


	def mosquito_shoot(self):
		if self.mosquitos.sprites():
			random_mosquito = choice(self.mosquitos.sprites())
			laser_sprite = Laser(random_mosquito.rect.center,6,screen_height)
			self.mosquito_lasers.add(laser_sprite)

	def extra_mosquito_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Extra(choice(['right','left']),screen_width))
	
	def run(self, screen, delta, jogo):
		self.player.update()
		self.mosquitos.update(self.mosquito_direction)
		self.mosquito_position_checker()
		self.mosquito_lasers.update()
		self.extra_mosquito_timer()
		self.extra.update()
		# render
		self.tela.fill("black")
		self.player.sprite.lasers.draw(self.tela)
		self.player.draw(self.tela)

		self.blocks.draw(self.tela)
		self.mosquitos.draw(screen)
		self.mosquito_lasers.draw(screen)
		screen.blit(pygame.transform.scale(self.tela, screen.get_size()), (0, 0))
		self.extra.draw(screen)

if __name__ == '__main__':
	pygame.init()
	screen_width = 1280
	screen_height = 720
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = SpaceMinigame()
	

	MOSQUITOLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(MOSQUITOLASER,800)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOSQUITOLASER:
				game.mosquito_shoot()

		screen.fill((30,30,30))
		game.run()
		#crt.draw()
			
		pygame.display.flip()
		clock.tick(60)