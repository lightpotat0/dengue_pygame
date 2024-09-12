import pygame
import util
import random
import math

CASA_SIZE = 80
CASA_STRIDE = CASA_SIZE + 8
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
MAPA = [
	"               ",
	" XXXXX   XXXXX ",
	" X   X   X   X ",
	" XXXXXXXXXXXXX ",
	"     X   X     ",
	"     X   X     ",
	"     X   X     ",
	" XXXXXXXXXXXXX ",
	" X   X   X   X ",
	" XXXXX   XXXXX ",
	"               "
]
CENTRO = (1066 / 2 - (CASA_STRIDE * len(MAPA[0]) - (CASA_STRIDE - CASA_SIZE)) / 2, 600 / 2 - (CASA_STRIDE * len(MAPA) - (CASA_STRIDE - CASA_SIZE)) / 2)

def casa_id_para_pos(id):
    return (CENTRO[0] + id[0] * CASA_STRIDE, CENTRO[1] + id[1] * CASA_STRIDE)

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
		self.cinero = pygame.image.load("tabuleiro/cinero.png")
		self.lixo = pygame.image.load("tabuleiro/lixo.png")
		self.dado = pygame.image.load("tabuleiro/dado.png")
		self.minigame = pygame.image.load("tabuleiro/minigame.png")
		if casas != None:
			self.casas = casas
		else:
			self.casas = []
			casa_inicial = None
			for x in range(len(MAPA[0])):
				for y in range(len(MAPA)):
					if MAPA[y][x] == "X":
						if casa_inicial == None:
							casa_inicial = (x, y)
						self.casas.append(Casa(x, y, random.choice(TIPOS)))
					elif MAPA[y][x] == " ":
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

	alphas = [1, 0, 0, 0]
	animacoes = [(None, 0, None) for _ in range(4)]
	def animar(self, animacao, numero_jogador, param = None):
		if self.animacoes[numero_jogador][0] != animacao or self.animacoes[numero_jogador][2] != param:
			self.animacoes[numero_jogador] = (animacao, pygame.time.get_ticks(), param)

	def outros_jogadores_em_casa(self, casa, jogo, exceto_numero):
		conta = 0
		for j in jogo.jogadores:
			if j.numero != exceto_numero and j.casa == casa and self.animacoes[j.numero][0] == None:
				conta += 1
		return conta

	cam_pos = (0, 0)

	def camerado(self, pos):
		return (pos[0] - self.cam_pos[0] + 1066 / 2, pos[1] - self.cam_pos[1] + 600 / 2)

	def frame(self, screen, delta, jogo):
		self.tempo += delta
		screen.fill("black")
		for casa in self.casas:
			match casa.tipo:
				case "teleporte":
					util.scaleblit(screen, 600, self.nether_portal, self.camerado(casa.pos), pygame.Rect(0, 16 * math.floor(self.tempo * 32.0 % 32.0), 16, 16), CASA_SIZE / 16)
				case "+R$5":
					util.scaleblit(screen, 600, self.cinero, self.camerado(casa.pos), None, CASA_SIZE / 128)
				case "-R$2":
					util.scaleblit(screen, 600, self.lixo, self.camerado(casa.pos), None, CASA_SIZE / 128)
				case "dado":
					util.scaleblit(screen, 600, self.dado, self.camerado(casa.pos), None, CASA_SIZE / 128)
				case "minigame":
					util.scaleblit(screen, 600, self.minigame, self.camerado(casa.pos), None, CASA_SIZE / 128)
				case "vazio":
					util.scaleblit(screen, 600, util.tint_mult(self.casa, (63, 63, 63)), self.camerado(casa.pos), None, CASA_SIZE / 64)
				case _:
					util.scaleblit(screen, 600, self.casa, self.camerado(casa.pos), None, CASA_SIZE / 64)
					util.scaleblit(screen, 600, self.font.render(casa.tipo, True, "black"), self.camerado(casa.pos), None, CASA_SIZE / 64)
		tempo = pygame.time.get_ticks()
		jogador_atual_offset = (0, 0)
		for numero in [0 if jogo.jogador_atual > 0 else 1, 1 if jogo.jogador_atual > 1 else 2, 2 if jogo.jogador_atual > 2 else 3, jogo.jogador_atual]:
			if numero >= len(jogo.jogadores):
				continue
			jogador = jogo.jogadores[numero]
			outros_jogadores_em_casa = self.outros_jogadores_em_casa(jogador.casa, jogo, numero)
			pos = casa_id_para_pos(jogador.casa)
			animacao = self.animacoes[numero]
			sprite = jogador.get_andamento(jogador.direcao, True)
			match animacao:
				case ("andando", tempo_inicio, (pos_inicio, direcao)):
					if tempo >= tempo_inicio + 500:
						self.animar(None, numero)
					sprite = jogador.get_andamento(direcao)
					andado = (tempo - tempo_inicio) / 500 * CASA_STRIDE
					pos = (pos_inicio[0] + andado * direcao[0], pos_inicio[1] + andado * direcao[1])
					if jogador.numero == jogo.jogador_atual:
						jogador_atual_offset = (andado * direcao[0], andado * direcao[1])
				case ("riqueza", tempo_inicio, _):
					if tempo >= tempo_inicio + 1000:
						jogo.passar_vez()
						self.modo = "dado"
						self.dado_numero = random.randint(1, 6)
						self.animar(None, numero)
					x = (tempo - tempo_inicio) / 250 * math.pi
					if x % math.tau > math.pi:
						x -= math.pi
					pos = (pos[0], pos[1] - 24 * math.sin(x))
					sprite = jogador.get_andamento("down", True)
				case ("pobreza", tempo_inicio, _):
					if tempo >= tempo_inicio + 1000:
						jogo.passar_vez()
						self.modo = "dado"
						self.dado_numero = random.randint(1, 6)
						self.animar(None, numero)
					x = (tempo - tempo_inicio) / 250 * math.pi
					if x % math.tau > math.pi:
						x -= math.pi
					t = 1 - math.sin(x)
					sprite = util.tint_mult(sprite, (255, 255 * t, 255 * t))
				case ("teleporte", tempo_inicio, _):
					if tempo >= tempo_inicio + 1000:
						jogador.casa = (random.randint(0, len(MAPA)), random.randint(0, len(MAPA[0])))
						while not self.encontrar_casa(jogador.casa):
							jogador.casa = (random.randint(0, len(MAPA)), random.randint(0, len(MAPA[0])))
						jogo.passar_vez()
						self.modo = "dado"
						self.dado_numero = random.randint(1, 6)
						self.animar(None, numero)
					sprite = jogador.get_andamento(["down", "left", "up", "right"][(tempo - tempo_inicio) // 100 % 4], True)
			sprite_tamanho = (72, 72)
			if jogo.jogador_atual != numero:
				self.alphas[numero] = util.lerp(self.alphas[numero], 0.5, 8 * delta)
			else:
				self.alphas[numero] = util.lerp(self.alphas[numero], 1, 8 * delta)
			if jogo.jogador_atual != numero and outros_jogadores_em_casa > 0:
				match numero:
					case 0:
						pos = (pos[0] - 2, pos[1] + 4)
					case 1:
						pos = (pos[0] + 58, pos[1] + 4)
					case 2:
						pos = (pos[0] - 2, pos[1] + 52)
					case 3:
						pos = (pos[0] + 58, pos[1] + 52)
				sprite_tamanho = (24, 24)
			else:
				pos = (pos[0] + 6, pos[1] + 6)
			claridade = 255 * self.alphas[numero]
			util.scaleblit(screen, 600, util.tint_mult(pygame.transform.scale(sprite, sprite_tamanho), (claridade, claridade, claridade, 255)), self.camerado(pos))
		jogador = jogo.jogadores[jogo.jogador_atual]
		if self.modo == "dado":
			self.dado_tempo += delta
			if self.dado_tempo >= 0.1:
				self.dado_numero = random.randint(1, 6)
				self.dado_tempo = 0
			if util.pressionado_agora[pygame.K_SPACE] or util.pressionado_agora[pygame.K_RETURN]:
				self.dado_tempo = 0
				self.modo = "andando"

		proxima_cam_pos = casa_id_para_pos(jogo.jogadores[jogo.jogador_atual].casa)
		proxima_cam_pos = (proxima_cam_pos[0] + jogador_atual_offset[0] + 36, proxima_cam_pos[1] + jogador_atual_offset[1] + 36)
		self.cam_pos = (util.lerp(self.cam_pos[0], proxima_cam_pos[0], 2 * delta), util.lerp(self.cam_pos[1], proxima_cam_pos[1], 2 * delta))

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
					self.dado_numero = 0
					casa = self.encontrar_casa(jogador.casa)
					match casa.tipo:
						case "minigame":
							if self.dado_tempo >= 1:
								return "minigame"
						case "dado":
							if self.dado_tempo >= 1:
								self.modo = "dado"
								self.dado_numero = random.randint(1, 6)
								self.dado_tempo = 0
							self.animar(None, jogador.numero)
						case "+R$5":
							self.animar("riqueza", jogador.numero)
							jogador.moedas += 5
							self.modo = "animando"
							self.dado_tempo = 0
						case "-R$2":
							self.animar("pobreza", jogador.numero)
							jogador.moedas -= 2
							self.modo = "animando"
							self.dado_tempo = 0
						case "teleporte":
							self.animar("teleporte", jogador.numero)
							self.modo = "animando"
							self.dado_tempo = 0
				else:
					self.dado_numero -= 1
					if self.dado_numero > 0:
						self.dado_tempo = 0
					(casa, direcao) = self.proxima_casa_e_direcao(jogador)
					jogador.casa = casa
					jogador.direcao = direcao
			if self.dado_tempo < 0.5 and self.dado_numero > 0:
				(casa, direcao) = self.proxima_casa_e_direcao(jogador)
				self.animar("andando", jogador.numero, (casa_id_para_pos(jogador.casa), direcao))
		if self.modo != "andando" and self.modo != "animando":
			self.animar(None, 0)
			self.animar(None, 1)
			self.animar(None, 2)
			self.animar(None, 3)
