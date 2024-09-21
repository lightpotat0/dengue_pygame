import pygame
import util

#fontes
fonte = pygame.font.Font("Biblioteca de Assets/fontes/tt-milks-casual-pie-base.ttf", 30)
fonte1 = pygame.font.Font("Biblioteca de Assets/fontes/tt-milks-casual-pie-base.ttf", 25)
class Titulo:
	def __init__(self):
		self.logo = pygame.image.load("titulo/logo.svg").convert_alpha()
		self.bg = pygame.image.load("titulo/titulobq.png").convert_alpha()
		self.comecar = False

	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key in [pygame.K_KP_ENTER, pygame.K_RETURN, pygame.K_SPACE, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,  pygame.K_m]:
				self.comecar = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.comecar = True

	def frame(self, screen, delta, jogo):
		#background
		screen.blit(pygame.transform.smoothscale(self.bg, screen.get_size()), (0, 0))

		#escala da logo
		max_logo_width = screen.get_width() * 0.8
		max_logo_height = screen.get_height() * 0.8

		logo_rect = self.logo.get_rect()
		logo_scaled_rect = logo_rect.scale_by(max_logo_height / logo_rect.height)
		if logo_scaled_rect.width > max_logo_width:
			logo_scaled_rect = logo_rect.scale_by(max_logo_width / logo_rect.width)

		logo_scaled = pygame.transform.smoothscale(self.logo, logo_scaled_rect.size)
		logo_rect = logo_scaled.get_rect(center=screen.get_rect().center)
		logo_rect.centery = screen.get_rect().centery - screen.get_height() // 15
		screen.blit(logo_scaled, logo_rect)

		#mensagens
		mensagem = 'Pressione qualquer tecla para iniciar'
		mensagem1 = 'Pressione esc para sair'
		texto_formatado = fonte.render(mensagem, True, (255,255,255))
		texto_formatado1 = fonte1.render(mensagem1, True, (255,255,255))
		util.scaleblit(screen, 600, texto_formatado, (600 / screen.get_height() * screen.get_width() / 2 - texto_formatado.get_width() / 2, 480))
		util.scaleblit(screen, 600, texto_formatado1, (600 / screen.get_height() * screen.get_width() / 2 - texto_formatado1.get_width() / 2, 530))
		util.scaleblit(screen, 600, fonte1.render("1: Pingo, 2: Walk, 3: Space, 4: Pistol, M: Aleatório", True, (0, 0, 0)), (0, 0))

		#verificação de seleção
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
				return "selecion"
