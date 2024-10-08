import pygame
import util
from jogador import Jogador

#bordas das imagens
border_color_nenhum = (63, 63, 63)
border_colors = [
    (255, 0, 0),
	(0, 162, 255),
	(24, 196, 26),
	(255, 196, 0)
]

#escala das bordas
border_size = 10
border_size1 = 5
border_radius = 10
font = pygame.font.Font(None, 24)

#escalas
size1 = (200, 300)
size2 = (100, 100)
size3 = (50, 50)

#desenho das imagens com borda
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

#função do evento de hover
def is_mouse_over(screen, image_rect):
	return image_rect.collidepoint(util.mouse_pos_para(screen, 600))

class Selecion:
	def __init__(self, casas, jogo):
		#variaveis da classe
		jogo.jogadores = [Jogador(), Jogador(), Jogador(), Jogador()]
		for i in range(4):
			jogo.jogadores[i].numero = i
		self.jogadores = 0
		self.fundo = pygame.image.load("selecion/fundo.png").convert_alpha()
		self.portratos = [
			pygame.image.load("Biblioteca de Assets/Players/2 Full Art.png").convert_alpha(),
			pygame.image.load("Biblioteca de Assets/Players/4 Full Art.png").convert_alpha(),
			pygame.image.load("Biblioteca de Assets/Players/1 Full Art.png").convert_alpha(),
			pygame.image.load("Biblioteca de Assets/Players/3 Full Art.png").convert_alpha()
		]
		self.ninguem = pygame.Surface((200, 300))
		self.start = pygame.image.load("selecion/start.png").convert_alpha()

		self.number1 = pygame.image.load("selecion/1.png").convert_alpha()
		self.number2 = pygame.image.load("selecion/2.png").convert_alpha()
		self.number3 = pygame.image.load("selecion/3.png").convert_alpha()
		self.number4 = pygame.image.load("selecion/4.png").convert_alpha()

		self.pressed = True

	def frame(self, screen, delta, jogo):
		screen.blit(pygame.transform.scale(self.fundo, screen.get_size()), (0, 0)) #background
		#personagens para seleção editados
		draw_image_with_border(screen, self.portratos[jogo.jogadores[0].personagem] if jogo.jogadores[0].personagem != None else self.ninguem, (50, 50), 200, border_colors[0], border_size, border_radius)
		draw_image_with_border(screen, self.portratos[jogo.jogadores[1].personagem] if jogo.jogadores[1].personagem != None else self.ninguem, (305, 50), 200, border_colors[1], border_size, border_radius)
		draw_image_with_border(screen, self.portratos[jogo.jogadores[2].personagem] if jogo.jogadores[2].personagem != None else self.ninguem, (560, 50), 200, border_colors[2], border_size, border_radius)
		draw_image_with_border(screen, self.portratos[jogo.jogadores[3].personagem] if jogo.jogadores[3].personagem != None else self.ninguem, (820, 50), 200, border_colors[3], border_size, border_radius)

		#evento da seleção do jogador
		jogador_que_escolheu = [None, None, None, None]
		for jogador in jogo.jogadores:
			if jogador.personagem != None:
				jogador_que_escolheu[jogador.personagem] = jogador.numero
		cor_do_jogador_que_escolheu = [border_color_nenhum, border_color_nenhum, border_color_nenhum, border_color_nenhum]
		for jogador in jogo.jogadores:
			if jogador.personagem != None:
				cor_do_jogador_que_escolheu[jogador.personagem] = border_colors[jogador.numero]
		jm_rect = draw_image_with_border(screen, util.icones[0], (300, 420), 100, cor_do_jogador_que_escolheu[0], border_size1, border_radius)
		hk_rect = draw_image_with_border(screen, util.icones[1], (420, 420), 100, cor_do_jogador_que_escolheu[1], border_size1, border_radius)
		enzo_rect = draw_image_with_border(screen, util.icones[2], (540, 420), 100, cor_do_jogador_que_escolheu[2], border_size1, border_radius)
		an_rect = draw_image_with_border(screen, util.icones[3], (660, 420), 100, cor_do_jogador_que_escolheu[3], border_size1, border_radius)
		iniciar_rect = None

		#impressão da figura dos números
		util.scaleblit(screen, 600, self.number1, (52, 55), None, 4)
		util.scaleblit(screen, 600, self.number2, (308, 55), None, 4)
		util.scaleblit(screen, 600, self.number3, (563, 55), None, 4)
		util.scaleblit(screen, 600, self.number4, (823, 55), None, 4)

		#condição que a partir seleção
		if self.jogadores >= 2:
			iniciar_rect = draw_image_with_border(screen, self.start, (780, 420), 100, (91, 191, 91), border_size1, border_radius)
			iniciar_texto_rect = iniciar_rect.copy()
			iniciar_texto_rect.midtop = iniciar_rect.midbottom
			if is_mouse_over(screen, iniciar_rect):
				iniciar_rect = draw_image_with_border(screen, self.start, (780, 420), 100, (127, 255, 127), border_size1, border_radius)
				if pygame.mouse.get_pressed()[0]:
					jogo.jogadores = jogo.jogadores[:self.jogadores]
					return "iniciar jogo"

		if self.jogadores < 4:
			jogador = jogo.jogadores[self.jogadores]
			aceitaveis = [None, jogador.numero]
			if is_mouse_over(screen, jm_rect) and jogador_que_escolheu[0] in aceitaveis:
				jogador.personagem = 0
			elif is_mouse_over(screen, hk_rect) and jogador_que_escolheu[1] in aceitaveis:
				jogador.personagem = 1
			elif is_mouse_over(screen, enzo_rect) and jogador_que_escolheu[2] in aceitaveis:
				jogador.personagem = 2
			elif is_mouse_over(screen, an_rect) and jogador_que_escolheu[3] in aceitaveis:
				jogador.personagem = 3
			else:
				jogador.personagem = None
			if jogador.personagem != None:
				util.scaleblit(screen, 400, jogador.get_andamento("down"), (50, 270), None, 4)
				if pygame.mouse.get_pressed()[0]:
					if not self.pressed:
						self.jogadores += 1
						self.pressed = True
				else:
					self.pressed = False
