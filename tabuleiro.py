import pygame
import util
import random

CENTRO = (1066 / 2 - (72 * 7 + 72 - 64) / 2, 600 / 2 - (72 * 7 + 72 - 64) / 2)
TIPOS = [
	#"+R$5",
	#"-R$2",
	#"dado",
	#"pergunta",
	"minigame",
	#"medalha",
	#"teleporte",
	#"item",
	#"loja",
	#"sorte"
]

class Casa:
	def __init__(self, x, y):
		self.id = (x, y)
		self.pos = (CENTRO[0] + x * 72, CENTRO[1] + y * 72)
		self.tipo = random.choice(TIPOS)

class Tabuleiro:
	def __init__(self):
		self.modo = "dado"
		self.font = pygame.font.Font(None, 24)
		self.font_dado = pygame.font.Font(None, 64)
		self.dado_numero = random.randint(1, 6)
		self.dado_tempo = 0
		self.casa = pygame.image.load("tabuleiro/casa.png")
		self.vc = pygame.image.load("pingominigame/obj/vc.png")
		self.mapa = [
			"XXX XXX",
			"X X X X",
			"XXXXXXX",
			"  X X  ",
			"XXXXXXX",
			"X X X X",
			"XXX XXX"
		]
		self.casas = []
		for x in range(0, 7):
			for y in range(0, 7):
				if self.mapa[y][x] == "X":
					self.casas.append(Casa(x, y))

	def encontrar_casa(self, id):
		for casa in self.casas:
			if casa.id == id:
				return casa
		return None

	def frame(self, screen, delta, jogo):
		screen.fill("black")
		for casa in self.casas:
			util.scaleblit(screen, 600, self.casa, casa.pos)
			util.scaleblit(screen, 600, self.font.render(casa.tipo, True, "black"), casa.pos)
			for jogador in jogo.jogadores:
				if casa.id == jogador.casa:
					util.scaleblit(screen, 600, pygame.transform.scale(self.vc, (60, 60)), (casa.pos[0] + 2, casa.pos[1] + 2))
		jogador = jogo.jogadores[jogo.jogador_atual]
		if self.modo == "dado":
			self.dado_tempo += delta
			if self.dado_tempo >= 0.1:
				self.dado_numero = random.randint(1, 6)
				self.dado_tempo = 0
			if util.pressionado_agora[pygame.K_SPACE] or util.pressionado_agora[pygame.K_RETURN]:
				self.dado_tempo = 0
				self.modo = "andando"
		if len(jogo.jogadores) >= 1:
			cor = "green" if jogo.jogador_atual == 0 else "white"
			texto = self.font_dado.render("Jogador 1", True, cor)
			util.scaleblit(screen, 600, texto, (0, 0))
			util.scaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[0].moedas}", True, cor), (0, texto.get_height()))
		if len(jogo.jogadores) >= 2:
			cor = "green" if jogo.jogador_atual == 1 else "white"
			texto = self.font_dado.render("Jogador 2", True, cor)
			util.scaleblit(screen, 600, texto, (1066 - texto.get_width(), 0))
			util.scaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[1].moedas}", True, cor), (1066 - texto.get_width(), texto.get_height()))
		if len(jogo.jogadores) >= 3:
			cor = "green" if jogo.jogador_atual == 2 else "white"
			texto = self.font_dado.render("Jogador 3", True, cor)
			util.scaleblit(screen, 600, texto, (0, 600 - texto.get_height() * 2))
			util.scaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[2].moedas}", True, cor), (0, 600 - texto.get_height()))
		if len(jogo.jogadores) >= 4:
			cor = "green" if jogo.jogador_atual == 3 else "white"
			texto = self.font_dado.render("Jogador 4", True, cor)
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
					self.modo = "dado"
					self.dado_numero = random.randint(1, 6)
				else:
					self.dado_numero -= 1
					self.dado_tempo = 0
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
							jogador.casa = nova_casa
							jogador.direcao = direcao
							break
