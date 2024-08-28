import pygame
import util

fonte = pygame.font.SysFont('arial', 40, True, True)
fonte1 = pygame.font.SysFont('arial', 25, True, True)
class Titulo:
	def __init__(self):
		self.logo = pygame.image.load("titulo/logo.svg")
		self.bg = pygame.image.load("titulo/titulobq.png")
		self.comecar = False

	def event(self, event):
		if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
			self.comecar = True

	def frame(self, screen, delta, jogo):
		screen.blit(pygame.transform.scale(self.bg, screen.get_size()), (0, 0))
		screen.blit(pygame.transform.scale(self.logo, screen.get_size()), (640, 0))
		mensagem = 'Pressione qualquer tecla para iniciar'
		mensagem1 = 'Ou pressione esc para sair'
		texto_formatado = fonte.render(mensagem, True, (000,000,000))
		texto_formatado1 = fonte1.render(mensagem1, True, (000,000,000))
		util.scaleblit(screen, 600, texto_formatado, (200, 480))
		util.scaleblit(screen, 600, texto_formatado1, (370, 530))
		util.scaleblit(screen, 600, fonte1.render("1: Pingo, 2: Walk, 3: Space, 4: Pistol, M: Aleatório", True, (0, 0, 0)), (0, 0))
		if self.comecar:
			if util.pressionado_agora[pygame.K_1]:
				return "minigame0"
			elif util.pressionado_agora[pygame.K_2]:
				return "minigame1"
			elif util.pressionado_agora[pygame.K_3]:
				return "minigame2"
			elif util.pressionado_agora[pygame.K_4]:
				return "minigame3"
			elif util.pressionado_agora[pygame.K_m]:
				return "minigame"
			else:
				return "novo jogo"
