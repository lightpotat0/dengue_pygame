import pygame
import util
import random
import math

#pingando
import pingominigame.gerarnivel

class Balde:
	def __init__(self, pos):
		self.pos = pos
		self.cheio = 0
		self.fechado = False
		self.velocidade = random.uniform(2.0, 2.6)

class PingoMinigame:
	tamanho = (428, 240)
	def __init__(self):
		self.morreu = False
		self.jumpscare_tempo = 0
		self.tempo = 0
		nivel = gerarnivel.gerar()
		self.bg = nivel[0]
		self.vc = pygame.image.load("pingominigame/obj/vc.png")
		self.estalactite = [pygame.image.load(f"pingominigame/obj/estalactite{i}.png") for i in range(1, 10)]
		self.balde = pygame.image.load("pingominigame/obj/balde.png")
		self.balde_meio = pygame.image.load("pingominigame/obj/balde_meio.png")
		self.balde_mais = pygame.image.load("pingominigame/obj/balde_mais.png")
		self.balde_todo = pygame.image.load("pingominigame/obj/balde_todo.png")
		self.balde_fechado = pygame.image.load("pingominigame/obj/balde_fechado.png")
		self.mosquito = pygame.image.load("pingominigame/mosquito.png")
		self.vc_pos = (428 / 2 - 32, 240 / 2 - 32)
		self.baldes = [
			Balde(nivel[1][0]),
			Balde(nivel[1][1]),
			Balde(nivel[1][2]),
			Balde(nivel[1][3])
		]

	def get_tempo_da_perdicao(self, tempo_inicio):
		menor = 1000000
		for balde in self.baldes:
			if not balde.fechado and balde.cheio < 20:
				menor = min(menor, (20 - balde.cheio) / balde.velocidade * 1000)
		return pygame.time.get_ticks() + menor

	def frame(self, screen, delta, jogo):
		self.tempo += delta
		screen.fill("black")
		if not self.morreu:
			self.vc_pos = util.deslize(self.bg, self.vc, self.vc_pos, util.movimento(75, delta))
			self.vc_pos = (util.clamp(self.vc_pos[0], 0, 428 - self.vc.get_width()), util.clamp(self.vc_pos[1], 0, 240 - self.vc.get_height()))
		screen.blit(self.bg, (0, 0))
		for balde in self.baldes:
			balde_img = self.balde
			if util.imagem_colide_com_rect(pygame.Rect((balde.pos[0], balde.pos[1] - 20, self.balde.get_width(), self.balde.get_height() + 20)), self.vc, self.vc_pos) and not balde.fechado:
				balde.fechado = True
				jogo.receber_moedas(3)
			if balde.fechado:
				balde_img = self.balde_fechado
			else:
				balde.cheio = min(balde.cheio + balde.velocidade * delta, 20)
				if balde.cheio >= 20:
					self.morreu = True
				if balde.cheio >= 15:
					balde_img = self.balde_todo
				elif balde.cheio >= 10:
					balde_img = self.balde_mais
				elif balde.cheio >= 5:
					balde_img = self.balde_meio
				else:
					balde_img = self.balde
			screen.blit(balde_img, balde.pos)
			util.blitanimado(screen, self.estalactite, (balde.pos[0], balde.pos[1] - 20), self.tempo, 10)
		screen.blit(self.vc, self.vc_pos)
		fechar = False
		if self.morreu:
			self.jumpscare_tempo += delta
			aumentado = pygame.transform.scale_by(self.mosquito, self.jumpscare_tempo * 2)
			screen.blit(aumentado, (428 / 2 - aumentado.get_width() / 2, 240 / 2 - aumentado.get_height() / 2))
			if self.jumpscare_tempo >= 1:
				fechar = True
		if fechar:
			return "perdeu"
		for balde in self.baldes:
			if not balde.fechado:
				break
		else:
			return "ganhou"
