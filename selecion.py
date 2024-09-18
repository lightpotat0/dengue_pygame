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

def draw_image_with_border(screen, image, pos, border_color, border_size, border_radius):
	image_rect = image.get_rect(topleft=pos)

	pygame.draw.rect(screen, border_color,
					 (image_rect.x - border_size, image_rect.y - border_size,
					  image_rect.width + border_size*2, image_rect.height + border_size*2), border_radius=border_radius)

	util.smoothscaleblit(screen, 600, image, pos)
	return image_rect

def is_mouse_over(image_rect):
	return image_rect.collidepoint(util.mouse_pos)

class Selecion:
	def __init__(self, casas, jogo):
		self.jogadores = 0
		self.fundo = pygame.image.load("selecion/fundo.png").convert_alpha()
		self.portratos = [
			pygame.transform.scale(pygame.image.load("selecion/ana_leticia.jpg").convert_alpha(), size1),
			pygame.transform.scale(pygame.image.load("selecion/helena_karan.jpg").convert_alpha(), size1),
			pygame.transform.scale(pygame.image.load("selecion/enzo_gabriel.jpg").convert_alpha(), size1),
			pygame.transform.scale(pygame.image.load("selecion/joao_maria.jpg").convert_alpha(), size1)
		]

		self.c_enzo = pygame.transform.scale(pygame.image.load("selecion/enzu.jpg").convert_alpha(), size2)
		self.c_jm = pygame.transform.scale(pygame.image.load("selecion/jm.jpg").convert_alpha(), size2)
		self.c_an = pygame.transform.scale(pygame.image.load("selecion/an.jpg").convert_alpha(), size2)
		self.c_hk = pygame.transform.scale(pygame.image.load("selecion/hk.jpg").convert_alpha(), size2)

		self.number1 = pygame.transform.scale(pygame.image.load("selecion/1.png").convert_alpha(), size3)
		self.number2 = pygame.transform.scale(pygame.image.load("selecion/2.png").convert_alpha(), size3)
		self.number3 = pygame.transform.scale(pygame.image.load("selecion/3.png").convert_alpha(), size3)
		self.number4 = pygame.transform.scale(pygame.image.load("selecion/4.png").convert_alpha(), size3)

	def frame(self, screen, delta, jogo):
		size1 = (200, 300)
		size2 = (100, 100)
		size3 = (50, 50)
		screen.blit(pygame.transform.scale(self.fundo, screen.get_size()), (0, 0))
		draw_image_with_border(screen, self.portratos[jogo.jogadores[0].personagem], (50, 50), border_colors[jogo.jogadores[0].personagem], border_size, border_radius)
		if self.jogadores >= 1:
			draw_image_with_border(screen, self.portratos[jogo.jogadores[1].personagem], (305, 50), border_colors[jogo.jogadores[1].personagem], border_size, border_radius)
		if self.jogadores >= 2:
			draw_image_with_border(screen, self.portratos[jogo.jogadores[2].personagem], (560, 50), border_colors[jogo.jogadores[2].personagem], border_size, border_radius)
		if self.jogadores >= 3:
			draw_image_with_border(screen, self.portratos[jogo.jogadores[3].personagem], (820, 50), border_colors[jogo.jogadores[3].personagem], border_size, border_radius)

		jm_rect = draw_image_with_border(screen, self.c_an, (300, 420), border_color_vermei, border_size1, border_radius)
		hk_rect = draw_image_with_border(screen, self.c_hk, (420, 420), border_color_azuli, border_size1, border_radius)
		enzo_rect = draw_image_with_border(screen, self.c_enzo, (540, 420), border_color_verdi, border_size1, border_radius)
		an_rect = draw_image_with_border(screen, self.c_jm, (660, 420), border_color_amare, border_size1, border_radius)

		screen.blit(self.number1, (52, 55))
		if self.jogadores >= 1:
			screen.blit(self.number2, (308, 55))
		if self.jogadores >= 2:
			screen.blit(self.number3, (563, 55))
		if self.jogadores >= 3:
			screen.blit(self.number4, (823, 55))

		jogador = jogo.jogadores[0]
		if is_mouse_over(jm_rect):
			jogador.personagem = 0
			sprite_to_blit = pygame.transform.scale(jogador.get_andamento("down"), (150, 150))
			screen.blit(sprite_to_blit, (65, 380))
		elif is_mouse_over(hk_rect):
			jogador.personagem = 1
			sprite_to_blit = pygame.transform.scale(jogador.get_andamento("down"), (150, 150))
			screen.blit(sprite_to_blit, (65, 380))
		elif is_mouse_over(enzo_rect):
			jogador.personagem = 2
			sprite_to_blit = pygame.transform.scale(jogador.get_andamento("down"), (150, 150))
			screen.blit(sprite_to_blit, (65, 380))
		elif is_mouse_over(an_rect):
			jogador.personagem = 3
			sprite_to_blit = pygame.transform.scale(jogador.get_andamento("down"), (150, 150))
			screen.blit(sprite_to_blit, (65, 380))