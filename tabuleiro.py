import pygame
import util
import random
import math

#detalhe das casa do mapa
CASA_SIZE = 80
CASA_STRIDE = CASA_SIZE + 8

#mapeamento
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
	"                  ",
	"                  ",
	"                  ",
	"                  ",
	"    XXXXX   XXXXX ",
	"    X   X   X   X ",
	"    X   X   X   X ",
	"    X   X   X   X ",
	"    XXXXXXXXXXXXX ",
	"        X   X     ",
	"        X   X     ",
	"        X   X     ",
	"    XXXXXXXXXXXXX ",
	"    X   X   X   X ",
	"    X   X   X   X ",
	"    X   X   X   X ",
	"    XXXXX   XXXXX ",
	"                  "
]
CENTRO = (1066 / 2 - (CASA_STRIDE * len(MAPA[0]) - (CASA_STRIDE - CASA_SIZE)) / 2, 600 / 2 - (CASA_STRIDE * len(MAPA) - (CASA_STRIDE - CASA_SIZE)) / 2)
FUNDO_OFFSET = (-8, -24)

fundo = pygame.image.load("tabuleiro/ChaoMapa.png").convert_alpha()
objetos = [
	pygame.image.load("tabuleiro/mapa_objetos_0.png").convert_alpha(),
	pygame.image.load("tabuleiro/mapa_objetos_1.png").convert_alpha(),
	pygame.image.load("tabuleiro/mapa_objetos_2.png").convert_alpha(),
	pygame.image.load("tabuleiro/mapa_objetos_3.png").convert_alpha(),
	pygame.image.load("tabuleiro/mapa_objetos_4.png").convert_alpha()
]

#cordenadas pra posição
def casa_id_para_pos(id):
    return (id[0] * CASA_STRIDE + 8, id[1] * CASA_STRIDE)

#casa do tabuleiro
class Casa:
	def __init__(self, x, y, tipo):
		self.id = (x, y)
		self.pos = casa_id_para_pos(self.id)
		self.tipo = tipo

#o tabuleiro
class Tabuleiro:
	def __init__(self, casas, jogo):
		self.modo = "dado"
		self.font = pygame.font.Font(None, 24)
		self.font_dado = pygame.font.Font(None, 128)
		self.dado_numero = random.randint(1, 6)
		self.dado_tempo = 0
		self.tempo = 0
		self.portal = pygame.transform.smoothscale(pygame.image.load("tabuleiro/portal.png").convert_alpha(), (128, 128))
		self.cinero = pygame.transform.smoothscale(pygame.image.load("tabuleiro/cinero.png").convert_alpha(), (128, 128))
		self.lixo = pygame.transform.smoothscale(pygame.image.load("tabuleiro/lixo.png").convert_alpha(), (128, 128))
		self.dado = pygame.transform.smoothscale(pygame.image.load("tabuleiro/dado.png").convert_alpha(), (128, 128))
		self.minigame = pygame.transform.smoothscale(pygame.image.load("tabuleiro/minigame.png").convert_alpha(), (128, 128))
		if casas != None:
			self.casas = casas
		else:
			self.casas = []
			casa_inicial = None
			for y in range(len(MAPA)):
				for x in range(len(MAPA[0])):
					if MAPA[y][x] == "X":
						if casa_inicial == None:
							casa_inicial = (x, y)
						self.casas.append(Casa(x, y, random.choice(TIPOS)))
					elif MAPA[y][x] == " ":
						self.casas.append(Casa(x, y, "vazio"))
						
			for jogador in jogo.jogadores:
				jogador.casa = casa_inicial


	#encontrar id da casa
	def encontrar_casa(self, id):
		for casa in self.casas:
			if casa.id == id and casa.tipo != "vazio":
				return casa
		return None

	#próxima casa e direção
	def proxima_casa_e_direcao(self, jogador):
		direcoes = [
			(jogador.direcao[0], jogador.direcao[1]), #frente
			(jogador.direcao[1], jogador.direcao[0]), #direita
			(-jogador.direcao[1], -jogador.direcao[0]), #trás 
			(-jogador.direcao[0], -jogador.direcao[1]) #esquerda
		]

		for direcao in direcoes:
			nova_casa = (jogador.casa[0] + direcao[0], jogador.casa[1] + direcao[1])
			casa = self.encontrar_casa(nova_casa)
			if casa != None:
				return (nova_casa, direcao)
		return (jogador.casa, jogador.direcao)

	#animações
	alphas = [0, 0, 0, 0] #transparencia dos sprites
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
		screen.fill(0xb4df5d)
		util.smoothscaleblit(screen, 600, fundo, self.camerado(FUNDO_OFFSET), None, CASA_STRIDE / 142)
		util.smoothscaleblit(screen, 600, objetos[0], self.camerado(FUNDO_OFFSET), None, CASA_STRIDE / 142)
		for casa in self.casas:
			if casa.id[0] == 0:
				if casa.id[1] == 8:
					util.smoothscaleblit(screen, 600, objetos[1], self.camerado(FUNDO_OFFSET), None, CASA_STRIDE / 142)
				elif casa.id[1] == 12:
					util.smoothscaleblit(screen, 600, objetos[2], self.camerado(FUNDO_OFFSET), None, CASA_STRIDE / 142)
				elif casa.id[1] == 16:
					util.smoothscaleblit(screen, 600, objetos[3], self.camerado(FUNDO_OFFSET), None, CASA_STRIDE / 142)
				elif casa.id[1] == 17:
					util.smoothscaleblit(screen, 600, objetos[4], self.camerado(FUNDO_OFFSET), None, CASA_STRIDE / 142)
			match casa.tipo:
				case "teleporte":
					#util.scaleblit(screen, 600, self.nether_portal, self.camerado(casa.pos), None, CASA_SIZE / 1300)
					util.smoothscaleblit(screen, 600, self.portal, self.camerado(casa.pos), None, CASA_SIZE / self.portal.get_height())
				case "+R$5":
					util.smoothscaleblit(screen, 600, self.cinero, self.camerado(casa.pos), None, CASA_SIZE / self.cinero.get_height())
				case "-R$2":
					util.smoothscaleblit(screen, 600, self.lixo, self.camerado(casa.pos), None, CASA_SIZE / self.lixo.get_height())
				case "dado":
					util.smoothscaleblit(screen, 600, self.dado, self.camerado(casa.pos), None, CASA_SIZE / self.dado.get_height())
				case "minigame":
					util.smoothscaleblit(screen, 600, self.minigame, self.camerado(casa.pos), None, CASA_SIZE / 128)
				case "vazio":
					pass
					#util.scaleblit(screen, 600, util.tint_mult(self.casa, (63, 63, 63)), self.camerado(casa.pos), None, CASA_SIZE / 64)
				case _:
					util.scaleblit(screen, 600, self.casa, self.camerado(casa.pos), None, CASA_SIZE / 64)
					util.smoothscaleblit(screen, 600, self.font.render(casa.tipo, True, "black"), self.camerado(casa.pos), None, CASA_SIZE / 64)
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
				if self.alphas[numero] == 0:
					self.alphas[numero] = 0.5
				else:
					self.alphas[numero] = util.lerp(self.alphas[numero], 0.5, 8 * delta)
			else:
				if self.alphas[numero] == 0:
					self.alphas[numero] = 1
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
			claridade = util.clamp(255 * self.alphas[numero], 0, 255)
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
		if self.cam_pos == (0, 0):
			self.cam_pos = proxima_cam_pos
		else:
			self.cam_pos = (util.lerp(self.cam_pos[0], proxima_cam_pos[0], 4 * delta), util.lerp(self.cam_pos[1], proxima_cam_pos[1], 4 * delta))

		cor = "white"
		if len(jogo.jogadores) >= 1:
			texto = self.font_dado.render("Jogador 1", True, "green" if jogo.jogador_atual == 0 else cor)
			util.smoothscaleblit(screen, 600, texto, (0, 0), None, 0.5)
			util.smoothscaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[0].moedas}", True, cor), (0, texto.get_height() / 2), None, 0.5)
		if len(jogo.jogadores) >= 2:
			texto = self.font_dado.render("Jogador 2", True, "green" if jogo.jogador_atual == 1 else cor)
			util.smoothscaleblit(screen, 600, texto, (1066 - texto.get_width(), 0), None, 0.5)
			util.smoothscaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[1].moedas}", True, cor), (1066 - texto.get_width() / 2, texto.get_height() / 2), None, 0.5)
		if len(jogo.jogadores) >= 3:
			texto = self.font_dado.render("Jogador 3", True, "green" if jogo.jogador_atual == 2 else cor)
			util.smoothscaleblit(screen, 600, texto, (0, 600 - texto.get_height() * 2), None, 0.5)
			util.smoothscaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[2].moedas}", True, cor), (0, 600 - texto.get_height() / 2), None, 0.5)
		if len(jogo.jogadores) >= 4:
			texto = self.font_dado.render("Jogador 4", True, "green" if jogo.jogador_atual == 3 else cor)
			util.smoothscaleblit(screen, 600, texto, (1066 - texto.get_width(), 600 - texto.get_height() * 2), None, 0.5)
			util.smoothscaleblit(screen, 600, self.font_dado.render(f"R${jogo.jogadores[3].moedas}", True, cor), (1066 - texto.get_width() / 2, 600 - texto.get_height() / 2), None, 0.5)

		util.smoothscaleblit(screen, 600, self.font_dado.render(str(self.dado_numero), True, "red"), (533 - 32, 300 - 32))

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
