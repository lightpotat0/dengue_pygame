import pygame
import util
import random
import math

#detalhe das casa do mapa
CASA_SIZE = 80
CASA_STRIDE = CASA_SIZE + 8
SOMBRA_SIZE = int(80 * 1600 / 1280)

#mapeamento
TIPOS = [
	"+R$5", "+R$5", "+R$5",
	"-R$2", "-R$2",
	"dado", "dado", "dado",
	"carta",
	"minigame", "minigame", "minigame",
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
	"    XXXXXXMXXXXXX ",
	"        X   X     ",
	"        M   M     ",
	"        X   X     ",
	"    XXXXXXMXXXXXX ",
	"    X   X   X   X ",
	"    X   X   X   X ",
	"    X   X   X   X ",
	"    XXXXX   XXXXX ",
	"                  "
]

CENTRO = (1066 / 2 - (CASA_STRIDE * len(MAPA[0]) - (CASA_STRIDE - CASA_SIZE)) / 2, 600 / 2 - (CASA_STRIDE * len(MAPA) - (CASA_STRIDE - CASA_SIZE)) / 2)
CASAS_OFFSET = (8, 24)

fundo = pygame.image.load("tabuleiro/ChaoMapa.png").convert_alpha()
objetos = [
	pygame.image.load("tabuleiro/mapa_objetos_0.png").convert_alpha(),
	pygame.image.load("tabuleiro/mapa_objetos_1.png").convert_alpha(),
	pygame.image.load("tabuleiro/mapa_objetos_2.png").convert_alpha(),
	pygame.image.load("tabuleiro/mapa_objetos_3.png").convert_alpha(),
	pygame.image.load("tabuleiro/mapa_objetos_4.png").convert_alpha()
]
portal = pygame.transform.smoothscale(pygame.image.load("tabuleiro/portal.png").convert_alpha(), (256, 256))
cinero = pygame.transform.smoothscale(pygame.image.load("tabuleiro/cinero.png").convert_alpha(), (256, 256))
lixo = pygame.transform.smoothscale(pygame.image.load("tabuleiro/lixo.png").convert_alpha(), (256, 256))
dado = pygame.transform.smoothscale(pygame.image.load("tabuleiro/dado.png").convert_alpha(), (256, 256))
minigame = pygame.transform.smoothscale(pygame.image.load("tabuleiro/minigame.png").convert_alpha(), (256, 256))
medalha = pygame.transform.smoothscale(pygame.image.load("tabuleiro/medalha.png").convert_alpha(), (256, 256))
medalhas = pygame.transform.smoothscale(pygame.image.load("Biblioteca de Assets\Medalha.png").convert_alpha(), (256, 256))
carta = pygame.transform.smoothscale(pygame.image.load("tabuleiro/carta.png").convert_alpha(), (256, 256))
sombra = pygame.transform.smoothscale(pygame.image.load("tabuleiro/casabg.png").convert_alpha(), (320, 320))
interrogacao = pygame.transform.smoothscale(pygame.image.load("tabuleiro/pergunta.png").convert_alpha(), (160, 160))
seta = pygame.image.load("tabuleiro/seta.png").convert_alpha()
setas = [
	seta,
	pygame.transform.rotate(seta, 180),
	pygame.transform.rotate(seta, 90),
	pygame.transform.rotate(seta, -90)
]
DADO_SIZE = 96
dadobgs = [
	pygame.transform.smoothscale(pygame.image.load("tabuleiro/Dados/Dado Vermelho.png").convert_alpha(), (DADO_SIZE, DADO_SIZE)),
	pygame.transform.smoothscale(pygame.image.load("tabuleiro/Dados/Dado Azul.png").convert_alpha(), (DADO_SIZE, DADO_SIZE)),
	pygame.transform.smoothscale(pygame.image.load("tabuleiro/Dados/Dado Verde.png").convert_alpha(), (DADO_SIZE, DADO_SIZE)),
	pygame.transform.smoothscale(pygame.image.load("tabuleiro/Dados/Dado Amarelo.png").convert_alpha(), (DADO_SIZE, DADO_SIZE))
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
		self.pode_entrar_em_camera = False
		if casas != None:
			self.casas = casas
		else:
			self.casas = []
			casa_inicial = None
			for y in range(len(MAPA)):
				for x in range(len(MAPA[0])):
					if MAPA[y][x] == "m":
						if casa_inicial == None:
							casa_inicial = (x, y)
						self.casas.append(Casa(x, y, random.choice(TIPOS)))
					elif MAPA[y][x] == "X":
						if casa_inicial == None:
							casa_inicial = (x, y)
						self.casas.append(Casa(x, y, "medalha"))
					elif MAPA[y][x] == "Y":
						if casa_inicial == None:
							casa_inicial = (x, y)
						self.casas.append(Casa(x, y, "desisao "))
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
	cam_movida = (0, 0)
	setas_mults = [0, 0, 0, 0]
	setas_direcoes = [-1, -1, -1, -1]
	escala_mapa = 1
	tabuleiro = None

	def camerado(self, pos):
		return (pos[0] - self.cam_pos[0] + 1066 / 2, pos[1] - self.cam_pos[1] + 600 / 2)

	def event(self, ev):
		if ev.type == pygame.MOUSEBUTTONDOWN or (ev.type == pygame.KEYDOWN and ev.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]):
			if self.modo == "camera":
				self.modo = "dado"
			return True

	def frame(self, screen, delta, jogo):
		self.tempo += delta
		screen.fill(0xb4df5d)

		# uma matematicazinha complicada pra ganhar fps, renderizando o tabuleiro só se necessário (na primeira vez e se o jogador redimensionar a tela)
		# nem funcionou bem mas
		tabuleiro_size = (fundo.get_width() * CASA_STRIDE / 143 * screen.get_height() // 600, fundo.get_height() * CASA_STRIDE / 143 * screen.get_height() // 600)
		if self.tabuleiro == None or self.tabuleiro.get_size() != tabuleiro_size:
			self.tabuleiro = pygame.Surface(tabuleiro_size)
			h = fundo.get_height() * CASA_STRIDE / 143
			util.smoothscaleblit(self.tabuleiro, h, fundo, (0, 0), None, CASA_STRIDE / 143)
			util.smoothscaleblit(self.tabuleiro, h, objetos[0], (0, 0), None, CASA_STRIDE / 143)

			# mostrar todas as casas
			for casa in self.casas:
				if casa.id[0] == 0:
					# mostrar os objetos de fundo em certos pontos para aparecerem em cima das casas
					if casa.id[1] == 8:
						util.smoothscaleblit(self.tabuleiro, h, objetos[1], (0, 0), None, CASA_STRIDE / 143)
					elif casa.id[1] == 12:
						util.smoothscaleblit(self.tabuleiro, h, objetos[2], (0, 0), None, CASA_STRIDE / 143)
					elif casa.id[1] == 16:
						util.smoothscaleblit(self.tabuleiro, h, objetos[3], (0, 0), None, CASA_STRIDE / 143)
					elif casa.id[1] == 17:
						util.smoothscaleblit(self.tabuleiro, h, objetos[4], (0, 0), None, CASA_STRIDE / 143)
				sombra_pos = (casa.pos[0] - (SOMBRA_SIZE - CASA_SIZE) * 0.5, casa.pos[1] - (SOMBRA_SIZE - CASA_SIZE) * 0.5)
				if casa.tipo != "vazio":
					util.smoothscaleblit(self.tabuleiro, h, sombra, sombra_pos, None, SOMBRA_SIZE / sombra.get_height())
				match casa.tipo:
					case "teleporte":
						util.smoothscaleblit(self.tabuleiro, h, portal, casa.pos, None, CASA_SIZE / portal.get_height())
					case "+R$5":
						util.smoothscaleblit(self.tabuleiro, h, cinero, casa.pos, None, CASA_SIZE / cinero.get_height())
					case "-R$2":
						util.smoothscaleblit(self.tabuleiro, h, lixo, casa.pos, None, CASA_SIZE / lixo.get_height())
					case "dado":
						util.smoothscaleblit(self.tabuleiro, h, dado, casa.pos, None, CASA_SIZE / dado.get_height())
					case "minigame":
						util.smoothscaleblit(self.tabuleiro, h, minigame, casa.pos, None, CASA_SIZE / minigame.get_height())
					case "medalha":
						util.smoothscaleblit(self.tabuleiro, h, medalha, casa.pos, None, CASA_SIZE / medalha.get_height())
					case "carta":
						util.smoothscaleblit(self.tabuleiro, h, carta, casa.pos, None, CASA_SIZE / carta.get_height())
					case "vazio":
						pass
		if self.escala_mapa >= 1.249:
			util.smoothscaleblit(screen, 600 * 1.25, self.tabuleiro, self.camerado((0, 0)), None, 600 / screen.get_height())
		else:
			util.smoothscaleblit(screen, 600 * 1.25, self.tabuleiro, self.camerado((0, 0)), None, 600 / screen.get_height(), True)
			util.scaleblit(screen, 600 * self.escala_mapa, self.tabuleiro, self.camerado((0, 0)), None, 600 / screen.get_height())

		# mostrar e animar os jogadores
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
				case ("robux", tempo_inicio, _):
					if tempo >= tempo_inicio + 1000:
						screen.blit(self.medalhas, (200, pos.y))
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
				case ("carta", tempo_inicio, _):
					util.smoothscaleblit(screen, 600, interrogacao, self.camerado((pos[0] + 0, pos[1] + 0)))
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
			pos = (pos[0] - 2, pos[1] - 2)
			util.scaleblit(screen, 600 * self.escala_mapa, util.tint_mult(pygame.transform.scale(sprite, sprite_tamanho), (claridade, claridade, claridade, 255)), self.camerado(pos))

		# processar a vez do jogador
		jogador = jogo.jogadores[jogo.jogador_atual]
		if self.modo == "dado":
			self.dado_tempo += delta
			if self.dado_tempo >= 0.1:
				self.dado_numero = random.randint(1, 6)
				self.dado_tempo = 0

		# mover a camera
		proxima_cam_pos = casa_id_para_pos(jogo.jogadores[jogo.jogador_atual].casa)
		proxima_cam_pos = (proxima_cam_pos[0] + jogador_atual_offset[0] + 36, proxima_cam_pos[1] + jogador_atual_offset[1] + 36)
		if self.modo == "camera":
			self.escala_mapa = util.lerp(self.escala_mapa, 1.25, 16 * delta)
			proxima_cam_pos = self.cam_movida
		else:
			self.escala_mapa = util.lerp(self.escala_mapa, 1, 16 * delta)
			self.cam_movida = self.cam_pos
		if self.cam_pos == (0, 0):
			self.cam_pos = proxima_cam_pos
		else:
			speed = 16 if self.modo == "camera" else 4
			self.cam_pos = (util.lerp(self.cam_pos[0], proxima_cam_pos[0], speed * delta), util.lerp(self.cam_pos[1], proxima_cam_pos[1], speed * delta))

		# mostrar dados dos jogadores
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

		movimento = util.movimento(1024, delta)
		if self.modo == "andando" or self.modo == "dado":
			# mostrar o dado
			dado_rect = pygame.Rect(0, 0, DADO_SIZE, DADO_SIZE)
			dado_rect.center = (screen.get_width() * 600 / screen.get_height() * 0.5, 600 * 0.75)
			util.smoothscaleblit(screen, 600, dadobgs[jogo.jogador_atual], dado_rect.topleft)
			dado_texto = self.font_dado.render(str(self.dado_numero), True, "black")
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 24, dado_rect.y + 8))
			dado_texto = util.tint_mult(dado_texto, (0, 0, 0, 31))
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 25, dado_rect.y + 7))
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 24, dado_rect.y + 6))
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 23, dado_rect.y + 7))
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 26, dado_rect.y + 8))
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 22, dado_rect.y + 8))
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 25, dado_rect.y + 9))
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 24, dado_rect.y + 10))
			util.smoothscaleblit(screen, 600, dado_texto, (dado_rect.x + 23, dado_rect.y + 9))
		elif self.modo == "carta":
			pass
		elif self.modo == "camera":
			# mostrar setas do movimento da camera
			self.setas_mults = [
				util.clamp(self.setas_mults[0] + self.setas_direcoes[0] * 4 * delta, -1.0, 2.0), # cima
				util.clamp(self.setas_mults[1] + self.setas_direcoes[1] * 4 * delta, -1.0, 2.0), # baixo
				util.clamp(self.setas_mults[2] + self.setas_direcoes[2] * 4 * delta, -1.0, 2.0), # esquerda
				util.clamp(self.setas_mults[3] + self.setas_direcoes[3] * 4 * delta, -1.0, 2.0) # direita
			]
			movendo = [movimento[1] < 0, movimento[1] > 0, movimento[0] < 0, movimento[0] > 0]
			for i in range(0, 4):
				if self.setas_mults[i] > 1.0:
					self.setas_direcoes[i] = -1
					self.setas_mults[i] = 2.0 - self.setas_mults[i]
				elif self.setas_mults[i] < 0.0:
					if movendo[i]:
						self.setas_direcoes[i] = 1
						self.setas_mults[i] = -self.setas_mults[i]
					else:
						self.setas_mults[i] = 0.0
				elif movendo[i] and self.setas_direcoes[i] == 0 and self.setas_mults[i] == 0.0:
					self.setas_direcoes[i] = 1
			util.smoothscaleblit(screen, 600, setas[0], (screen.get_width() * 600 / screen.get_height() / 2 - 32, (1 - self.setas_mults[0]) * 8), None, 0.25)
			util.smoothscaleblit(screen, 600, setas[1], (screen.get_width() * 600 / screen.get_height() / 2 - 32, 600 - 64 - (1 - self.setas_mults[1]) * 8), None, 0.25)
			util.smoothscaleblit(screen, 600, setas[2], ((1 - self.setas_mults[2]) * 8, 300 - 32), None, 0.25)
			util.smoothscaleblit(screen, 600, setas[3], (screen.get_width() * 600 / screen.get_height() - 64 - (1 - self.setas_mults[3]) * 8, 300 - 32), None, 0.25)

		# processar o andamento do jogador
		if self.modo == "andando":
			self.dado_tempo += delta
			if self.dado_tempo >= 0.5:
				casa = self.encontrar_casa(jogador.casa)
				if casa.tipo == "medalha":
					self.dado_numero = 0
				if self.dado_numero == 0:
					match casa.tipo:
						case "minigame":
							if self.dado_tempo >= 1:
								return "minigame"
						case "carta":
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
							jogador.moedas -= 3
							if jogador.moedas < 0:
								jogador.moedas = 0
							self.modo = "animando"
							self.dado_tempo = 0
						case "teleporte":
							self.animar("teleporte", jogador.numero)
							self.modo = "animando"
							self.dado_tempo = 0
						case "medalha":
							if jogador.moedas >= 30:
								self.animar("robux", jogador.numero)
								self.animar("riqueza", jogador.numero)
								self.modo = "animando"
								jogador.moedas -= 30
								jogador.medalhas += 1
								if self.dado_tempo >= 1:
									self.modo = "dado"
									self.dado_numero = random.randint(1, 6)
									self.dado_tempo = 0
							else: 
								self.animar("pobreza", jogador.numero)
								self.modo = "animando"
								if self.dado_tempo >= 1:
									self.modo = "dado"
									self.dado_numero = random.randint(1, 6)
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

		match self.modo:
			case "dado":
				if util.pressionado_agora[pygame.K_SPACE] or util.pressionado_agora[pygame.K_RETURN]:
					self.dado_tempo = 0
					self.modo = "andando"
				elif movimento[0] != 0 or movimento[1] != 0:
					if self.pode_entrar_em_camera:
						self.modo = "camera"
				else:
					self.pode_entrar_em_camera = True
			case "camera":
				virtual_width = screen.get_width() * 600 / screen.get_height()
				self.cam_movida = (util.clamp(self.cam_movida[0] + movimento[0], 1066 / 2, fundo.get_width() - 1960 * virtual_width / 1066), util.clamp(self.cam_movida[1] + movimento[1], 600 / 2, fundo.get_height() - 1620))
