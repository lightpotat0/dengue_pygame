import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1066, 600), pygame.RESIZABLE)
pygame.display.set_caption("Alerta Mosquito")
clock = pygame.time.Clock()

import util
import titulo
import tabuleiro
from pingominigame import PingoMinigame
from walkminigame import WalkMinigame
from spacedengue import SpaceMinigame
from fnaf_minigame import PistolMosquito

minigames = [PingoMinigame, WalkMinigame, SpaceMinigame, PistolMosquito]

modo = titulo.Titulo()
tela_minigame = None
tempo_inicio_minigame = 0
delta = 1 / 60

mosquiton = pygame.image.load("fnaf_minigame/sprites/mosquito_door1-export.png")
barra = pygame.image.load("fnaf_minigame/sprites/mosquito_door1-exportq.png")

andamentos = [
	pygame.image.load("assets/characterswalk1.png"),
	pygame.image.load("assets/characterswalk2.png"),
	pygame.image.load("assets/characterswalk3.png"),
	pygame.image.load("assets/characterswalk4.png")
]
icones = [
	pygame.image.load("assets/2.png"),
	pygame.image.load("assets/4.png"),
	pygame.image.load("assets/1.png"),
	pygame.image.load("assets/3.png")
]
class Jogador:
	numero = 0
	moedas = 50
	casa = (0, 0)
	direcao = (1, 0)
	def get_icone(self):
		return icones[self.numero]
	def get_andamento(self, direcao, parado = False):
		out = pygame.Surface((24, 24), pygame.SRCALPHA)
		if not isinstance(direcao, str):
			if direcao[0] < 0:
				direcao = "left"
			elif direcao[0] > 0:
				direcao = "right"
			elif direcao[1] < 0:
				direcao = "up"
			else:
				direcao = "down"
		match direcao:
			case "down":
				out.blit(andamentos[1 if parado else pygame.time.get_ticks() // 150 % 4], (0, 0), (self.numero * 24, 0 * 26 + 1, 24, 24))
			case "up":
				out.blit(andamentos[1 if parado else pygame.time.get_ticks() // 150 % 4], (0, 0), (self.numero * 24, 1 * 26 + 1, 24, 24))
			case "right":
				out.blit(andamentos[1 if parado else pygame.time.get_ticks() // 150 % 4], (0, 0), (self.numero * 24, 2 * 26 + 1, 24, 24))
			case "left":
				out.blit(andamentos[1 if parado else pygame.time.get_ticks() // 150 % 4], (0, 0), (self.numero * 24, 3 * 26 + 1, 24, 24))
		return out

class Jogo:
	jogadores = [Jogador(), Jogador()]
	for i in range(len(jogadores)):
		jogadores[i].numero = i
	jogador_atual = 0
	def passar_vez(self):
		self.jogador_atual += 1
		if self.jogador_atual >= len(self.jogadores):
			self.jogador_atual = 0
	def receber_moedas(self, moedas):
		self.jogadores[self.jogador_atual].moedas += moedas

jogo = Jogo()
casas = None

while True:
	util.mouse_pos = pygame.mouse.get_pos()
	if tela_minigame != None:
		event.pos = (util.mouse_pos[0] * modo.tamanho[0] / screen.get_width(), util.mouse_pos[1] * modo.tamanho[1] / screen.get_height())
	for event in pygame.event.get():
		if getattr(modo, "event", None) != None:
			if event.type == pygame.MOUSEBUTTONDOWN:
				event.pos = util.mouse_pos
			modo.event(event)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pressionado_novo = pygame.key.get_pressed()
	util.pressionado_agora = []
	for i in range(len(pressionado_novo)):
		util.pressionado_agora.append(pressionado_novo[i] and not util.pressionado[i])
	util.pressionado = pressionado_novo
	if util.pressionado_agora[pygame.K_ESCAPE]:
		pygame.quit()
		sys.exit()
	resultado = modo.frame(tela_minigame or screen, delta, jogo)
	if tela_minigame:
		if getattr(modo, "smooth", False):
			screen.blit(pygame.transform.smoothscale(tela_minigame, screen.get_size()), (0, 0))
		else:
			screen.blit(pygame.transform.scale(tela_minigame, screen.get_size()), (0, 0))
		if getattr(modo, "get_tempo_da_perdicao", None):
			tempo_da_perdicao = modo.get_tempo_da_perdicao(tempo_inicio_minigame)
			t = min((pygame.time.get_ticks() - tempo_inicio_minigame) / (tempo_da_perdicao - tempo_inicio_minigame), 1)
			if t < 0:
				t = 1
			size = 0.2
			height = screen.get_height() * size
			mosquito_width = height * mosquiton.get_width() / mosquiton.get_height()
			screen.blit(pygame.transform.scale(mosquiton, (mosquito_width, height)), pygame.Rect(0, screen.get_height() - height, mosquito_width, height))
			char_size = height
			barra_width = (screen.get_width() - mosquito_width - char_size) * t
			screen.blit(pygame.transform.scale(barra, (barra_width, height)), pygame.Rect(mosquito_width, screen.get_height() - height, barra_width, height))
			screen.blit(pygame.transform.scale(jogo.jogadores[jogo.jogador_atual].get_icone(), (char_size, char_size)), pygame.Rect(screen.get_width() - char_size, screen.get_height() - char_size, char_size, height))
			#screen.fill("red", pygame.Rect(0, screen.get_height() * 0.95, screen.get_width() * t, screen.get_height() * 0.05))
	match resultado:
		case "novo jogo":
			jogo = Jogo()
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