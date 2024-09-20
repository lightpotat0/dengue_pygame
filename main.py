import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1066, 600), pygame.RESIZABLE | pygame.DOUBLEBUF)
screen.set_alpha(None)
pygame.display.set_caption("Alerta Mosquito")
clock = pygame.time.Clock()
if True:
    loading = pygame.image.load("titulo/loading.jpg")
    screen.blit(pygame.transform.scale(loading, screen.get_size()), (0, 0))
    pygame.display.update()

import util
import tabuleiro
import titulo
import selecion
from pingominigame import PingoMinigame
from walkminigame import WalkMinigame
from spacedengue import SpaceMinigame
from fnaf_minigame import PistolMosquito

#minigames
minigames = [PingoMinigame, WalkMinigame, SpaceMinigame, PistolMosquito]

modo = titulo.Titulo()
tela_minigame = None
tempo_inicio_minigame = 0
delta = 1 / 60

mosquiton = pygame.image.load("fnaf_minigame/sprites/mosquito_door1-export.png").convert_alpha()
barra = pygame.image.load("fnaf_minigame/sprites/mosquito_door1-exportq.png").convert_alpha()

from jogador import Jogo
jogo = Jogo()
casas = None

#posicion de lo mouse
while True:
	util.mouse_pos = pygame.mouse.get_pos()
	if tela_minigame != None:
		util.mouse_pos = (util.mouse_pos[0] * modo.tamanho[0] / screen.get_width(), util.mouse_pos[1] * modo.tamanho[1] / screen.get_height())

	#eventos
	for event in pygame.event.get():
		if getattr(modo, "event", None) != None:
			if event.type == pygame.MOUSEBUTTONDOWN:
				event.pos = util.mouse_pos
			modo.event(event)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	#atualizando tecla
	pressionado_novo = pygame.key.get_pressed()
	util.pressionado_agora = []
	for i in range(len(pressionado_novo)):
		util.pressionado_agora.append(pressionado_novo[i] and not util.pressionado[i])
	util.pressionado = pressionado_novo

	#fechar o jogo
	if util.pressionado_agora[pygame.K_ESCAPE]:
		pygame.quit()
		sys.exit()

	#processando framesssssss
	util.clear_cache()
	resultado = modo.frame(tela_minigame or screen, delta, jogo)

	#redimensionamento do minigame
	if tela_minigame:
		if getattr(modo, "smooth", False):
			screen.blit(pygame.transform.smoothscale(tela_minigame, screen.get_size()), (0, 0))
		else:
			screen.blit(pygame.transform.scale(tela_minigame, screen.get_size()), (0, 0))

	#tamanho da barra
		size = 0.2
		height = screen.get_height() * size
		char_size = height
	#rg do personagem
		screen.blit(pygame.transform.scale(jogo.jogadores[jogo.jogador_atual].get_icone(), (char_size, char_size)), pygame.Rect(screen.get_width() - char_size, screen.get_height() - char_size, char_size, height))

	#tempo da PERDIÇÃO
	if getattr(modo, "get_tempo_da_perdicao", None):
		tempo_da_perdicao = modo.get_tempo_da_perdicao(tempo_inicio_minigame)
		t = min((pygame.time.get_ticks() - tempo_inicio_minigame) / (tempo_da_perdicao - tempo_inicio_minigame), 1)
		if t < 0:
			t = 1

		#mosquito no fundo e a barra
		mosquito_width = height * mosquiton.get_width() / mosquiton.get_height()
		screen.blit(pygame.transform.scale(mosquiton, (mosquito_width, height)), pygame.Rect(0, screen.get_height() - height, mosquito_width, height))
		barra_width = (screen.get_width() - mosquito_width - char_size) * t
		screen.blit(pygame.transform.scale(barra, (barra_width, height)), pygame.Rect(mosquito_width, screen.get_height() - height, barra_width, height))

	#timeline do game
	match resultado:
		case "selecion":
			jogo = Jogo()
			modo = selecion.Selecion(None, jogo)
			tela_minigame = None
		case "iniciar jogo":
			modo = tabuleiro.Tabuleiro(None, jogo)
			casas = modo.casas
			tela_minigame = None
		case "minigame":
			modo = random.choice(minigames)()
			tela_minigame = pygame.Surface(modo.tamanho)
			tempo_inicio_minigame = pygame.time.get_ticks()
		case "minigame0":
			modo = minigames[0]()
			tela_minigame = pygame.Surface(modo.tamanho)
			tempo_inicio_minigame = pygame.time.get_ticks()
		case "minigame1":
			modo = minigames[1]()
			tela_minigame = pygame.Surface(modo.tamanho)
			tempo_inicio_minigame = pygame.time.get_ticks()
		case "minigame2":
			modo = minigames[2]()
			tela_minigame = pygame.Surface(modo.tamanho)
			tempo_inicio_minigame = pygame.time.get_ticks()
		case "minigame3":
			modo = minigames[3]()
			tela_minigame = pygame.Surface(modo.tamanho)
			tempo_inicio_minigame = pygame.time.get_ticks()
		case "ganhou":
			jogo.receber_moedas(10)
			jogo.passar_vez()
			modo = tabuleiro.Tabuleiro(casas, jogo)
			tela_minigame = None
		case "perdeu":
			jogo.passar_vez()
			modo = tabuleiro.Tabuleiro(casas, jogo)
			tela_minigame = None
	pygame.display.update()
	delta = clock.tick() / 1000