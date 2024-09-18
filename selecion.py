import pygame
import util

border_colors = [
    (255, 0, 0),
	(0, 162, 255),
	(255, 196, 0),
	(24, 196, 26)
]

border_color_vermei = (255, 0, 0)
border_color_azuli = (0, 162, 255)
border_color_amare = (255, 196, 0)
border_color_verdi = (24, 196, 26)
border_size = 10
border_size1 = 5
border_radius = 10
font = pygame.font.Font(None, 24)

size1 = (200, 300)
size2 = (100, 100)
size3 = (50, 50)

def draw_image_with_border(screen, image, pos, width, border_color, border_size, border_radius):
	image_rect = image.get_rect(topleft=pos)
	image_rect.height *= width / image_rect.width
	image_rect.width = width

	util.scaledrawrect(screen, 600, border_color, (
		image_rect.x - border_size,
		image_rect.y - border_size,
		image_rect.width + border_size * 2,
		image_rect.height + border_size * 2
	), border_radius=border_radius)

	util.smoothscaleblit(screen, 600, image, pos, None, width / image.get_width())
	return image_rect

def is_mouse_over(image_rect):
	return image_rect.collidepoint(util.mouse_pos)

class Selecion:
	def __init__(self, casas, jogo):
		self.jogadores = 0
		self.fundo = pygame.image.load("selecion/fundo.png").convert_alpha()
		self.portratos = [
			pygame.image.load("selecion/ana_leticia.jpg").convert_alpha(),
			pygame.image.load("selecion/helena_karan.jpg").convert_alpha(),
			pygame.image.load("selecion/enzo_gabriel.jpg").convert_alpha(),
			pygame.image.load("selecion/joao_maria.jpg").convert_alpha()
		]

		self.number1 = pygame.image.load("selecion/1.png").convert_alpha()
		self.number2 = pygame.image.load("selecion/2.png").convert_alpha()
		self.number3 = pygame.image.load("selecion/3.png").convert_alpha()
		self.number4 = pygame.image.load("selecion/4.png").convert_alpha()

	def frame(self, screen, delta, jogo):
		size1 = (200, 300)
		size2 = (100, 100)
		size3 = (50, 50)
		screen.blit(pygame.transform.scale(self.fundo, screen.get_size()), (0, 0))
		draw_image_with_border(screen, self.portratos[jogo.jogadores[0].personagem], (50, 50), 200, border_colors[jogo.jogadores[0].personagem], border_size, border_radius)
		if self.jogadores >= 1:
			draw_image_with_border(screen, self.portratos[jogo.jogadores[1].personagem], (305, 50), 200, border_colors[jogo.jogadores[1].personagem], border_size, border_radius)
		if self.jogadores >= 2:
			draw_image_with_border(screen, self.portratos[jogo.jogadores[2].personagem], (560, 50), 200, border_colors[jogo.jogadores[2].personagem], border_size, border_radius)
		if self.jogadores >= 3:
			draw_image_with_border(screen, self.portratos[jogo.jogadores[3].personagem], (820, 50), 200, border_colors[jogo.jogadores[3].personagem], border_size, border_radius)

		jm_rect = draw_image_with_border(screen, util.icones[0], (300, 420), 100, border_color_vermei, border_size1, border_radius)
		hk_rect = draw_image_with_border(screen, util.icones[1], (420, 420), 100, border_color_azuli, border_size1, border_radius)
		enzo_rect = draw_image_with_border(screen, util.icones[2], (540, 420), 100, border_color_verdi, border_size1, border_radius)
		an_rect = draw_image_with_border(screen, util.icones[3], (660, 420), 100, border_color_amare, border_size1, border_radius)

		util.scaleblit(screen, 600, self.number1, (52, 55), None, 4)
		if self.jogadores >= 1:
			util.scaleblit(screen, 600, self.number2, (308, 55), None, 4)
		if self.jogadores >= 2:
			util.scaleblit(screen, 600, self.number3, (563, 55), None, 4)
		if self.jogadores >= 3:
			util.scaleblit(screen, 600, self.number4, (823, 55), None, 4)

		jogador = jogo.jogadores[0]
		if is_mouse_over(jm_rect):
			jogador.personagem = 0
			util.scaleblit(screen, 600, jogador.get_andamento("down"), (65, 380), None, 4)
		elif is_mouse_over(hk_rect):
			jogador.personagem = 1
			util.scaleblit(screen, 600, jogador.get_andamento("down"), (65, 380), None, 4)
		elif is_mouse_over(enzo_rect):
			jogador.personagem = 2
			util.scaleblit(screen, 600, jogador.get_andamento("down"), (65, 380), None, 4)
		elif is_mouse_over(an_rect):
			jogador.personagem = 3
			util.scaleblit(screen, 600, jogador.get_andamento("down"), (65, 380), None, 4)