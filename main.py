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
import pingominigame
import walkminigame

minigames = [pingominigame.PingoMinigame, walkminigame.WalkMinigame]

modo = titulo.Titulo()
delta = 1 / 60

class Jogador:
	moedas = 50
	casa = (0, 0)
	direcao = (1, 0)

class Jogo:
	jogadores = [Jogador(), Jogador()]
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
	for event in pygame.event.get():
		if getattr(modo, "event", None) != None:
			modo.event(event)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pressionado_novo = pygame.key.get_pressed()
	util.pressionado_agora = []
	for i in range(0, len(pressionado_novo)):
		util.pressionado_agora.append(pressionado_novo[i] and not util.pressionado[i])
	util.pressionado = pressionado_novo
	if util.pressionado_agora[pygame.K_ESCAPE]:
		pygame.quit()
		sys.exit()
	match modo.frame(screen, delta, jogo):
		case "novo jogo":
			jogo = Jogo()
			modo = tabuleiro.Tabuleiro(None, jogo)
			casas = modo.casas
		case "minigame":
			modo = random.choice(minigames)()
		case "ganhou":
			jogo.receber_moedas(10)
			jogo.passar_vez()
			modo = tabuleiro.Tabuleiro(casas, jogo)
		case "perdeu":
			jogo.passar_vez()
			modo = tabuleiro.Tabuleiro(casas, jogo)
	pygame.display.update()
	delta = clock.tick() / 1000