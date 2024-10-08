import pygame
from random import choice
from random import randint
import util
import math

ANIMATION_SPEED = 0.05

# Player Class
class Player(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()
		self.images = [
			pygame.image.load('walkminigame/Sprites/runboy1.png').convert_alpha(),
			pygame.image.load('walkminigame/Sprites/runboy2.png').convert_alpha(),
			pygame.image.load('walkminigame/Sprites/runboy3.png').convert_alpha(),
			pygame.image.load('walkminigame/Sprites/runboy4.png').convert_alpha()
		]
		self.speed = 1.0
		self.image_index = 0
		self.image = self.images[self.image_index]
		self.rect = self.image.get_rect(midbottom=(120, 474))

	def update(self):
		self.image_index += self.speed * ANIMATION_SPEED

		if self.image_index >= len(self.images):
			self.image_index = 0

		self.image = self.images[int(self.image_index)]

object_images = {
	'down': pygame.image.load('walkminigame/Sprites/bucketdown.png').convert_alpha(),
	'up': pygame.image.load('walkminigame/Sprites/trashup.png').convert_alpha(),
	'right': pygame.image.load('walkminigame/Sprites/tireright.png').convert_alpha()
}

# Obstacle Class
class Obstacle(pygame.sprite.Sprite):
	directions = {
		'down': [pygame.K_DOWN, pygame.K_s],
		'up': [pygame.K_UP, pygame.K_w],
		'right': [pygame.K_RIGHT, pygame.K_d]
	}

	def __init__(self, object, minigame, index, posicao_anterior):
		super().__init__()
		self.minigame = minigame
		self.object = object
		self.index = index

		self.image = object_images[object]
		self.posicao_base = posicao_anterior + randint(200, 400) + index * 8
		self.rect = self.image.get_rect(midbottom=(self.posicao_base, 474))

	def update(self):
		if not self.minigame.trigger:
			return
		keys = pygame.key.get_pressed()

		if self.index == self.minigame.kills and self.rect.x <= 720 and self.minigame.stun_timer == 0.0:
			direction_pressed = "none"
			if keys[self.directions["up"][0]] or keys[self.directions["up"][1]]:
				direction_pressed = "up"
			elif keys[self.directions["right"][0]] or keys[self.directions["right"][1]]:
				direction_pressed = "right"
			elif keys[self.directions["down"][0]] or keys[self.directions["down"][1]]:
				direction_pressed = "down"
			if direction_pressed == self.object:
				self.kill()
				self.minigame.kills += 1
				self.minigame.trigger = False
			elif direction_pressed != "none":
				self.minigame.stun_timer = 1.0

# Object Move
def parallax_blit(screen, obj, camera, factor, width):
	screen.blit(obj, (-camera * factor % width, 0))
	screen.blit(obj, (-camera * factor % width - width, 0))

# Main Game Class
class WalkMinigame:
	tamanho = (1280, 720)
	def __init__(self):
		self.fonte = pygame.font.Font(None, 64)

		# Variaveis
		self.spawn = True
		self.trigger = False
		self.posicao = 0.0
		self.velocidade = 320
		self.stun_timer = 0.0
		self.kills = 0

		# Jogador
		self.player = Player()
		self.obstacles = pygame.sprite.Group()

		# Sprites do Cenário
		self.clouds = pygame.image.load('walkminigame/Sprites/cloudsbackground.png').convert_alpha()
		self.clouds_rect = self.clouds.get_rect(topleft=(0, 0))

		self.background = pygame.image.load('walkminigame/Sprites/background.png').convert_alpha()
		self.background_rect = self.background.get_rect(topleft=(0, 0))

		self.ground = pygame.image.load('walkminigame/Sprites/ground.png').convert_alpha()
		self.ground_rect = self.ground.get_rect(bottomleft=(0, 720))

		# Sprites das Setas
		self.upkey = pygame.image.load("walkminigame/Sprites/upkey.png").convert_alpha()
		self.downkey = pygame.image.load("walkminigame/Sprites/downkey.png").convert_alpha()
		self.rightkey = pygame.image.load("walkminigame/Sprites/rightkey.png").convert_alpha()

	def get_tempo_da_perdicao(self, tempo_inicio):
		if len(self.obstacles) == 0:
			return 0
		distancia = self.obstacles.sprites()[-1].rect.x - 160
		# equação de torricelli
		velocidade_final = math.sqrt(self.velocidade * self.velocidade + 2 * 42 * distancia)
		return pygame.time.get_ticks() + distancia / ((velocidade_final + self.velocidade) / 2) * 1000

	def event(self, event):
		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			self.trigger = True

	def frame(self, screen, delta, jogo):
		self.player.update()

		red_tint = 0.0

		if self.stun_timer > 0.0:
			red_tint = min((1 - abs(self.stun_timer * 2 - 1)) * 2, 1)
			self.stun_timer -= delta * 4

			if self.stun_timer < 0.0:
				self.stun_timer = 0.0

		if self.spawn:
			posicao_anterior = 600
			for i in range(20):
				obstacle = Obstacle(choice(['up', 'down', 'right']), self, i, posicao_anterior)
				self.obstacles.add(obstacle)
				posicao_anterior = obstacle.posicao_base
			self.spawn = False

		self.velocidade = self.velocidade + 42 * delta
		self.posicao += self.velocidade * delta
		self.player.speed = self.velocidade / 500.0

		screen.fill('#87CEEB')
		width = screen.get_width()

		parallax_blit(screen, self.clouds, self.posicao, 0.5, width)
		parallax_blit(screen, self.background, self.posicao, 0.75, width)
		parallax_blit(screen, self.ground, self.posicao, 1.0, width)

		screen.blit(self.player.image, self.player.rect)

		self.obstacles.update()
		self.obstacles.draw(screen)
		object = "none"

		for sprite in self.obstacles.sprites():
			sprite.rect = sprite.image.get_rect(midbottom=(sprite.posicao_base - self.posicao, 474))
			if object == "none":
				if sprite.rect.x <= 160:
					return "perdeu"
				elif sprite.rect.x <= 720:
					object = sprite.object

		match object:
			case "up":
				screen.blit(self.upkey, self.upkey.get_rect(midbottom=self.obstacles.sprites()[0].rect.midtop))
			case "down":
				screen.blit(self.downkey, self.downkey.get_rect(midbottom=self.obstacles.sprites()[0].rect.midtop))
			case "right":
				screen.blit(self.rightkey, self.rightkey.get_rect(midbottom=self.obstacles.sprites()[0].rect.midtop))

		if self.kills >= 20:
			return "ganhou"

'''
def main():
	pygame.init()
	screen = pygame.display.set_mode((1280, 720))
	pygame.display.set_caption('Walk Minigame')
	clock = pygame.time.Clock()
	jogo = WalkMinigame()
	running = True

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		delta = clock.tick(60) / 1000
		result = jogo.frame(screen, delta)

		if result == "ganhou":
			print("Você ganhou!")
			running = False

		pygame.display.flip()

	pygame.quit()

if __name__ == "__main__":
	main()
'''