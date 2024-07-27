import pygame

class Titulo:
	def __init__(self):
		self.bg = pygame.image.load("titulo/titulo.jpeg")
		self.comecar = False

	def event(self, event):
		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			self.comecar = True

	def frame(self, screen, delta, jogo):
		screen.blit(pygame.transform.scale(self.bg, screen.get_size()), (0, 0))
		if self.comecar:
			return "novo jogo"
