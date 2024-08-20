import pygame
from random import choice
from random import randint

# Player Class
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('walkminigame/Sprites/player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom=(120, 474))

# Obstacle Class
class Obstacle(pygame.sprite.Sprite):
	directions = {
		'down': pygame.K_DOWN,
		'up': pygame.K_UP,
		'right': pygame.K_RIGHT
	}

	def __init__(self, object, minigame, index, posicao_anterior):
		super().__init__()
		self.minigame = minigame
		self.object = object
		self.index = index

		object_images = {
			'down': 'walkminigame/Sprites/bucketdown.png',
			'up': 'walkminigame/Sprites/trashup.png',
			'right': 'walkminigame/Sprites/tireright.png'
		}

		self.image = pygame.image.load(object_images[object]).convert_alpha()
		self.posicao_base = posicao_anterior + randint(200, 400)
		self.rect = self.image.get_rect(midbottom=(self.posicao_base, 474))

	def update(self):
		if not self.minigame.trigger:
			return

		keys = pygame.key.get_pressed()
		direction_key = self.directions[self.object]

		if keys[direction_key] and self.index == self.minigame.kills and self.rect.x <= 500:
			self.kill()
			self.minigame.kills += 1
			self.minigame.trigger = False

def parallax_blit(screen, obj, camera, factor, width):
	screen.blit(obj, (-camera * factor % width, 0))
	screen.blit(obj, (-camera * factor % width - width, 0))

# Main Game Class
class WalkMinigame:
	def __init__(self):
		self.screen = pygame.Surface((1280, 720))
		self.spawn = True
		self.trigger = False
		self.posicao = 0.0
		self.fonte = pygame.font.Font(None, 64)

		self.player = pygame.sprite.GroupSingle(Player())
		self.obstacles = pygame.sprite.Group()
		self.kills = 0

		self.clouds = pygame.image.load('walkminigame/Sprites/cloudsbackground.png').convert_alpha()
		self.clouds_rect = self.clouds.get_rect(topleft=(0, 0))

		self.background = pygame.image.load('walkminigame/Sprites/background.png').convert_alpha()
		self.background_rect = self.background.get_rect(topleft=(0, 0))

		self.ground = pygame.image.load('walkminigame/Sprites/ground.png').convert_alpha()
		self.ground_rect = self.ground.get_rect(bottomleft=(0, 720))
		self.velocidade = 320

	def event(self, event):
		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			self.trigger = True

	def frame(self, screen, delta, jogo):
		if self.spawn:
			posicao_anterior = 600
			for i in range(20):
				obstacle = Obstacle(choice(['up', 'down', 'right']), self, i, posicao_anterior)
				self.obstacles.add(obstacle)
				posicao_anterior = obstacle.posicao_base
			self.spawn = False
		self.velocidade = self.velocidade + 40 * delta
		if self.velocidade > 540:
			self.velocidade = 540
		self.posicao += self.velocidade * delta
		object = "none"
		for sprite in self.obstacles.sprites():
			sprite.rect = sprite.image.get_rect(midbottom=(sprite.posicao_base - self.posicao, 474))
			if object == "none":
				if sprite.rect.x <= 160:
					return "perdeu"
				elif sprite.rect.x <= 500:
					object = sprite.object

		self.screen.fill('#87CEEB')
		width = self.screen.get_width()
		parallax_blit(self.screen, self.clouds, self.posicao, 0.5, width)
		parallax_blit(self.screen, self.background, self.posicao, 0.75, width)
		parallax_blit(self.screen, self.ground, self.posicao, 1.0, width)

		self.player.draw(self.screen)
		self.obstacles.update()
		self.obstacles.draw(self.screen)
		match object:
			case "up":
				self.screen.blit(self.fonte.render(f"^", True, "black"), (120, 320))
			case "down":
				self.screen.blit(self.fonte.render(f"\\/", True, "black"), (120, 320))
			case "right":
				self.screen.blit(self.fonte.render(f"->", True, "black"), (120, 320))

		screen.blit(pygame.transform.scale(self.screen, screen.get_size()), (0, 0))

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