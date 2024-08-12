import pygame
import util

fonte = pygame.font.SysFont('arial', 40, True, True)
fonte1 = pygame.font.SysFont('arial', 25, True, True)
class Titulo:
	def __init__(self):
		self.bg = pygame.image.load("titulo/titulo.jpeg")
		self.comecar = False

	def event(self, event):
		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			self.comecar = True

	def frame(self, screen, delta, jogo):
		screen.blit(pygame.transform.scale(self.bg, screen.get_size()), (0, 0))
		mensagem = 'Pressione qualquer tecla para iniciar'
		mensagem1 = 'Ou pressione esc para sair'
		texto_formatado = fonte.render(mensagem, True, (000,000,000))
		texto_formatado1 = fonte1.render(mensagem1, True, (000,000,000))
		util.scaleblit(screen, 600, texto_formatado, (200, 480))
		util.scaleblit(screen, 600, texto_formatado1, (370, 530))
		if self.comecar:
			return "novo jogo"
