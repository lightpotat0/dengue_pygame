import pygame
import util

class Jogador:
	numero = 0
	personagem = None
	moedas = 50
	casa = (0, 0)
	direcao = (1, 0)
	def get_icone(self):
		return util.icones[self.personagem]
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
		#animação dos sprites no hover
		match direcao:
			case "down":
				out.blit(util.andamentos[1 if parado else pygame.time.get_ticks() // 150 % 4], (0, 0), (self.personagem * 24, 0 * 26 + 1, 24, 24))
			case "up":
				out.blit(util.andamentos[1 if parado else pygame.time.get_ticks() // 150 % 4], (0, 0), (self.personagem * 24, 1 * 26 + 1, 24, 24))
			case "right":
				out.blit(util.andamentos[1 if parado else pygame.time.get_ticks() // 150 % 4], (0, 0), (self.personagem * 24, 2 * 26 + 1, 24, 24))
			case "left":
				out.blit(util.andamentos[1 if parado else pygame.time.get_ticks() // 150 % 4], (0, 0), (self.personagem * 24, 3 * 26 + 1, 24, 24))
		return out

class Jogo:
	jogadores = [Jogador()]
	for i in range(len(jogadores)):
		jogadores[i].numero = i
	jogadores[0].personagem = 0
	jogador_atual = 0
	def passar_vez(self):
		self.jogador_atual += 1
		if self.jogador_atual >= len(self.jogadores):
			self.jogador_atual = 0
	def receber_moedas(self, moedas):
		self.jogadores[self.jogador_atual].moedas += moedas