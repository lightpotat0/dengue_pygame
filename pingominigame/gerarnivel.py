import pygame
import random
import util

CELL = 64
WIDTH = int(448 / CELL)
HEIGHT = int(240 / CELL)
CENTRO = (int(428 / 2 / CELL), int(240 / 2 / CELL) + 1)

def gerar():
	random.seed()

	mapa = [[True for x in range(WIDTH + 2)] for y in range(HEIGHT + 2)]

	mapa[CENTRO[1]][CENTRO[0]] = False
	mapa[CENTRO[1] - 1][CENTRO[0]] = False

	prev_snake_pos = (CENTRO[0], CENTRO[1])
	snake_pos = (CENTRO[0], CENTRO[1])
	snake_posicoes = []
	tombos = [[random.choice([False, False, False, False, True]) for x in range(WIDTH + 2)] for y in range(HEIGHT + 2)]
	tombos[CENTRO[1]][CENTRO[0] + 1] = True
	i = 0
	while i < 64 or (len(snake_posicoes) >= 4 and i < 512):
		i += 1
		if abs(snake_pos[0] - CENTRO[0]) >= 1 and mapa[snake_pos[1]][snake_pos[0]]:
			snake_posicoes.append(snake_pos)
		mapa[snake_pos[1]][snake_pos[0]] = False
		direcoes = []
		if snake_pos[0] > 1 and snake_pos[0] <= prev_snake_pos[0]:
			if not tombos[snake_pos[1]][snake_pos[0] - 1]:
				direcoes.append((-1, 0))
				if snake_pos[0] < prev_snake_pos[0]:
					direcoes.append((-1, 0))
		if snake_pos[0] < WIDTH - 1 and snake_pos[0] >= prev_snake_pos[0]:
			if not tombos[snake_pos[1]][snake_pos[0] + 1]:
				direcoes.append((1, 0))
				if snake_pos[0] > prev_snake_pos[0]:
					direcoes.append((1, 0))
		if snake_pos[1] > 1 and snake_pos[1] <= prev_snake_pos[1]:
			if not tombos[snake_pos[1] - 1][snake_pos[0]]:
				direcoes.append((0, -1))
				if snake_pos[1] < prev_snake_pos[1]:
					direcoes.append((0, -1))
		if snake_pos[1] < HEIGHT and snake_pos[1] >= prev_snake_pos[1]:
			if not tombos[snake_pos[1] + 1][snake_pos[0]]:
				direcoes.append((0, 1))
				if snake_pos[1] > prev_snake_pos[1]:
					direcoes.append((0, 1))
		direcao = (0, 0) if len(direcoes) == 0 else random.choice(direcoes)
		prev_snake_pos = snake_pos
		snake_pos = (snake_pos[0] + direcao[0], snake_pos[1] + direcao[1])
	shuffled = snake_posicoes[:-1]
	while len(shuffled) < 3:
		shuffled.append(random.choice(shuffled))
	random.shuffle(shuffled)
	baldes = [shuffled[0], shuffled[1], shuffled[2], snake_posicoes[len(snake_posicoes) - 1]]
	for i in range(len(baldes)):
		baldes[i] = (baldes[i][0] * CELL, baldes[i][1] * CELL)
	data = bytearray()
	data2 = bytearray()
	for y in range(240):
		y_factor = y % CELL / CELL
		row = mapa[int(y / CELL)]
		row2 = mapa[int(y / CELL) + 1]
		for x in range(428):
			x_factor = x % CELL / CELL
			val_top = util.lerp(row[int(x / CELL)], row[int(x / CELL) + 1], x_factor)
			val_bottom = util.lerp(row2[int(x / CELL)], row2[int(x / CELL) + 1], x_factor)
			data.append(255)
			data.append(255)
			data.append(255)
			val = util.lerp(val_top, val_bottom, y_factor)
			if val >= 0.35:
				data.append(255)
				data2.append(255)
				data2.append(255)
				data2.append(255)
				if val < 0.4:
					data2.append(255)
				elif val < 0.45:
					data2.append(131)
				else:
					data2.append(0)
			else:
				data.append(0)
				data2.append(0)
				data2.append(0)
				data2.append(0)
				data2.append(0)
	return (pygame.image.frombytes(bytes(data), (428, 240), "RGBA"), baldes, pygame.image.frombytes(bytes(data2), (428, 240), "RGBA"))