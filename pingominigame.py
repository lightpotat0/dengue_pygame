import pygame
import util
import random
import math

#pingando

class Balde:
	def __init__(self, pos):
		self.pos = pos
		self.cheio = 0
		self.fechado = False
		self.velocidade = random.uniform(1.4, 1.8)

class PingoMinigame:
	def __init__(self):
		self.morreu = False
		self.jumpscare_tempo = 0
		self.tempo = 0
		self.bg = pygame.image.load("pingominigame/w.png")
		self.vc = pygame.image.load("pingominigame/obj/vc.png")
		self.estalactite = [pygame.image.load(f"pingominigame/obj/estalactite{i}.png") for i in range(1, 10)]
		self.balde = pygame.image.load("pingominigame/obj/balde.png")
		self.balde_meio = pygame.image.load("pingominigame/obj/balde_meio.png")
		self.balde_mais = pygame.image.load("pingominigame/obj/balde_mais.png")
		self.balde_todo = pygame.image.load("pingominigame/obj/balde_todo.png")
		self.balde_fechado = pygame.image.load("pingominigame/obj/balde_fechado.png")
		self.mosquito = pygame.image.load("pingominigame/mosquito.png")
		self.vc_pos = (428 / 2 - self.vc.get_width() / 2, 240 / 2 - self.vc.get_height() / 2)
		self.baldes = [
			Balde((24, 219)),
			Balde((338, 217)),
			Balde((394, 39)),
			Balde((142, 113))
		]
		self.tela = pygame.Surface((428, 240))

	def frame(self, screen, delta, jogo):
		self.tempo += delta
		self.tela.fill("black")
		if not self.morreu:
			self.vc_pos = util.deslize(self.bg, self.vc, self.vc_pos, util.movimento(75, delta))
			self.vc_pos = (util.clamp(self.vc_pos[0], 0, 428 - self.vc.get_width()), util.clamp(self.vc_pos[1], 0, 240 - self.vc.get_height()))
		self.tela.blit(self.bg, (0, 0))
		for balde in self.baldes:
			balde_img = self.balde
			if util.colide_com_rect(pygame.Rect((balde.pos[0], balde.pos[1] - 20, self.balde.get_width(), self.balde.get_height() + 20)), self.vc, self.vc_pos) and not balde.fechado:
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
			self.tela.blit(balde_img, balde.pos)
			util.blitanimado(self.tela, self.estalactite, (balde.pos[0], balde.pos[1] - 20), self.tempo, 10)
		self.tela.blit(self.vc, self.vc_pos)
		fechar = False
		if self.morreu:
			self.jumpscare_tempo += delta
			aumentado = pygame.transform.scale_by(self.mosquito, self.jumpscare_tempo * 2)
			self.tela.blit(aumentado, (428 / 2 - aumentado.get_width() / 2, 240 / 2 - aumentado.get_height() / 2))
			if self.jumpscare_tempo >= 1:
				fechar = True
		screen.blit(pygame.transform.scale_by(self.tela, (screen.get_width() / 428, screen.get_height() / 240)), (0, 0))
		if fechar:
			return "perdeu"
		for balde in self.baldes:
			if not balde.fechado:
				break
		else:
			return "ganhou"
