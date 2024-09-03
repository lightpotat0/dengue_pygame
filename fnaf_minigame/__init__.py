import pygame
import util
import random
import time

#coisas
mosquito_image = pygame.image.load('fnaf_minigame/sprites/voando.png')
bg = pygame.image.load('fnaf_minigame/sprites/cenario.png')
cisterna = pygame.image.load('fnaf_minigame/sprites/cisterna.png')
bain = pygame.image.load('fnaf_minigame/sprites/bain.png')
tiro = pygame.image.load('fnaf_minigame/sprites/tiro.png')
mira = pygame.image.load('fnaf_minigame/sprites/mira.png')
screen_width = 1066
screen_height = 600
font = pygame.font.Font(None, 74)

class Mosquito:
	def __init__(self):
		self.active = True
		self.atirou = None
		self.fire_duration = 0.2
		self.size = mosquito_image.get_width()
		self.x = random.randint(0, screen_width - self.size)
		self.y = random.randint(0, screen_height - self.size)
		self.mosquito_rect = pygame.Rect(self.x, self.y, self.size, self.size)
		self.speed_x = random.choice([-3, 3])
		self.speed_y = random.choice([-3, 3])

	def move(self):
		if not self.active:
			return

		self.x += self.speed_x
		self.y += self.speed_y

		self.mosquito_rect.topleft = (self.x, self.y)

		#inverte a direção bla bla bla
		if self.x <= 0 or self.x >= screen_width - mosquito_image.get_width():
			self.speed_x = -self.speed_x

		if self.y <= 0 or self.y >= screen_height - mosquito_image.get_height():
			self.speed_y = -self.speed_y

	def draw(self, screen):
		if self.active:
			screen.blit(mosquito_image, (self.x, self.y))

		if self.atirou and (time.time() - self.atirou < self.fire_duration):
			screen.blit(tiro, (self.x, self.y))

	def deactivate(self):
		self.active = False
		self.atirou = time.time()

class PistolMosquito:
	tamanho = (screen_width, screen_height)
	def __init__(self):
		# quantidade de mosquito
		self.mosquitos = [Mosquito() for _ in range(15)]
		# timer
		self.start_time = time.time()
		self.timer_duration = 10
		self.clock = pygame.time.Clock()

	def event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			for mosquito in self.mosquitos:
				if mosquito.active and mosquito.mosquito_rect.collidepoint(mouse_pos):
					mosquito.deactivate()

	def frame(self, screen, delta, jogo):
		elapsed_time = time.time() - self.start_time
		screen.blit(pygame.transform.scale(bg, (screen_width, screen_height)), (0, 0))
		screen.blit(pygame.transform.scale_by(cisterna, 4), (82, 30))
		if elapsed_time < self.timer_duration:
			for mosquito in self.mosquitos:
				mosquito.move()
				mosquito.draw(screen)
			for mosquito in self.mosquitos:
				if mosquito.active:
					break
			else:
				return "ganhou"
		else:
			for mosquito in self.mosquitos:
				mosquito.deactivate()
			text = font.render("Você perdeu", True, (255, 0, 0))
			screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 1))
			if elapsed_time >= self.timer_duration + 2:
				return "perdeu"