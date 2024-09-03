import pygame
import util
import random
import math

CENTRO = (1066 / 2 - (72 * 15 + 72 - 64) / 2, 600 / 2 - (72 * 9 + 72 - 64) / 2)
TIPOS = [
	"+R$5", "+R$5", "+R$5",
	"-R$2", "-R$2",
	"dado", "dado", "dado",
	#"pergunta",
	"minigame", "minigame", "minigame",
	#"medalha",
	"teleporte",
	#"item",
	#"loja",
	#"sorte"
]
CORES = [
    "red",
	"blue",
	"green",
	"yellow"
]

def casa_id_para_pos(id):
    return (CENTRO[0] + id[0] * 72, CENTRO[1] + id[1] * 72)

class Casa:
	def __init__(self, x, y, tipo):
		self.id = (x, y)
		self.pos = casa_id_para_pos(self.id)
		self.tipo = tipo

class Tabuleiro:
	def __init__(self, casas, jogo):
		self.modo = "dado"
		self.font = pygame.font.Font(None, 24)
		self.font_dado = pygame.font.Font(None, 64)
		self.dado_numero = random.randint(1, 6)
		self.dado_tempo = 0
		self.tempo = 0
		self.casa = pygame.image.load("tabuleiro/casa.png")
		self.nether_portal = pygame.image.load("tabuleiro/nether_portal.png")
		self.mapa = [
			"               ",
			"    XXX XXX    ",
			"    X XXX X    ",
			"    XX   XX    ",
			"     X   X     ",
			"    XX   XX    ",
			"    X XXX X    ",
			"    XXX XXX    ",
			"               "
		]
		if casas != None:
			self.casas = casas
		else:
			self.casas = []
			casa_inicial = None
			for x in range(len(self.mapa[0])):
				for y in range(len(self.mapa)):
					if self.mapa[y][x] == "X":
						if casa_inicial == None:
							casa_inicial = (x, y)
						self.casas.append(Casa(x, y, random.choice(TIPOS)))
					elif self.mapa[y][x] == " ":
						self.casas.append(Casa(x, y, "vazio"))
			for jogador in jogo.jogadores:
				jogador.casa = casa_inicial

	def encontrar_casa(self, id):
		for casa in self.casas:
			if casa.id == id and casa.tipo != "vazio":
				return casa
		return None

	def proxima_casa_e_direcao(self, jogador):
		direcoes = [
			(jogador.direcao[0], jogador.direcao[1]),
			(jogador.direcao[1], jogador.direcao[0]),
			(-jogador.direcao[1], -jogador.direcao[0]),
			(-jogador.direcao[0], -jogador.direcao[1])
		]
		for direcao in direcoes:
			nova_casa = (jogador.casa[0] + direcao[0], jogador.casa[1] + direcao[1])
			casa = self.encontrar_casa(nova_casa)
			if casa != None:
				return (nova_casa, direcao)
		return (jogador.casa, jogador.direcao)

	animacoes = [(None, 0, None) for _ in range(4)]
	def animar(self, animacao, numero_jogador, param = None):
		if self.animacoes[numero_jogador][0] != animacao or self.animacoes[numero_jogador][2] != param:
			self.animacoes[numero_jogador] = (animacao, pygame.time.get_ticks(), param)

	def frame(self, screen, delta, jogo):
		self.tempo += delta
		screen.fill("black")
		for casa in self.casas:
			match casa.tipo:
				case "teleporte":
					util.scaleblit(screen, 600, self.nether_portal, casa.pos, pygame.Rect(0, 16 * math.floor(self.tempo * 32.0 % 32.0), 16, 16), 4)
				case "vazio":
					util.scaleblit(screen, 600, util.tint_mult(self.casa, (63, 63, 63)), casa.pos)
				case _:
					util.scaleblit(screen, 600, self.casa, casa.pos)
					util.scaleblit(screen, 600, self.font.render(casa.tipo, True, "black"), casa.pos)
		tempo = pygame.time.get_ticks()
		for i in range(len(jogo.jogadores)):
			jogador = jogo.jogadores[i]
			pos = casa_id_para_pos(jogador.casa)
			animacao = self.animacoes[i]
			sprite = jogador.get_andamento(jogador.direcao, True)
			match animacao:
				case ("andando", tempo_inicio, (pos_inicio, direcao)):
					if tempo >= tempo_inicio + 500:
						self.animar(None, jogador.numero)
					sprite = jogador.get_andamento(direcao)
					andado = (tempo - tempo_inicio) / 500 * 72
					pos = (pos_inicio[0] + andado * direcao[0], pos_inicio[1] + andado * direcao[1])
			util.scaleblit(screen, 600, pygame.transform.scale(sprite, (60, 60)), (pos[0] + 2, pos[1] + 2))
		jogador = jogo.jogadores[jogo.jogador_atual]
		if self.modo == "dado":
			self.dado_tempo += delta
			if self.dado_tempo >= 0.1:
				self.dado_numero = random.randint(1, 6)
				self.dado_tempo = 0
			if util.pressionado_agora[pygame.K_SPACE] or util.pressionado_agora[pygame.K_RETURN]:
				self.dado_tempo = 0
				self.modo = "andando"

		cor = "white"
		if len(jogo.jogadores) >= 1:
			texto = self.font_dado.render("Jogador 1", True, "green" if jogo.jogador_atual == 0 else cor)
			util.scaleblit(screen, 600, texto, (0, 0))
			util.scaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[0].moedas}", True, cor), (0, texto.get_height()))
		if len(jogo.jogadores) >= 2:
			texto = self.font_dado.render("Jogador 2", True, "green" if jogo.jogador_atual == 1 else cor)
			util.scaleblit(screen, 600, texto, (1066 - texto.get_width(), 0))
			util.scaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[1].moedas}", True, cor), (1066 - texto.get_width(), texto.get_height()))
		if len(jogo.jogadores) >= 3:
			texto = self.font_dado.render("Jogador 3", True, "green" if jogo.jogador_atual == 2 else cor)
			util.scaleblit(screen, 600, texto, (0, 600 - texto.get_height() * 2))
			util.scaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[2].moedas}", True, cor), (0, 600 - texto.get_height()))
		if len(jogo.jogadores) >= 4:
			texto = self.font_dado.render("Jogador 4", True, "green" if jogo.jogador_atual == 3 else cor)
			util.scaleblit(screen, 600, texto, (1066 - texto.get_width(), 600 - texto.get_height() * 2))
			util.scaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[3].moedas}", True, cor), (1066 - texto.get_width(), 600 - texto.get_height()))

		util.scaleblit(screen, 600, self.font_dado.render(str(self.dado_numero), True, "red"), (533 - 32, 300 - 32))

		if self.modo == "andando":
			self.dado_tempo += delta
			if self.dado_tempo >= 0.5:
				if self.dado_numero == 0:
					casa = self.encontrar_casa(jogador.casa)
					match casa.tipo:
						case "minigame":
							return "minigame"
						case "+R$5":
							jogador.moedas += 5
							jogo.passar_vez()
						case "-R$2":
							jogador.moedas -= 2
							jogo.passar_vez()
						case "teleporte":
							jogador.casa = (random.randint(0, len(self.mapa)), random.randint(0, len(self.mapa[0])))
							while not self.encontrar_casa(jogador.casa):
								jogador.casa = (random.randint(0, len(self.mapa)), random.randint(0, len(self.mapa[0])))
							jogo.passar_vez()
					self.modo = "dado"
					self.dado_numero = random.randint(1, 6)
				else:
					self.dado_numero -= 1
					self.dado_tempo = 0
					(casa, direcao) = self.proxima_casa_e_direcao(jogador)
					jogador.casa = casa
					jogador.direcao = direcao
			if self.dado_tempo < 0.5 and self.dado_numero > 0:
				(casa, direcao) = self.proxima_casa_e_direcao(jogador)
				self.animar("andando", jogador.numero, (casa_id_para_pos(jogador.casa), direcao))
