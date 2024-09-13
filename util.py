import pygame
import math

pressionado = pygame.key.get_pressed()
pressionado_agora = pressionado
mouse_pos = (0, 0)


def clamp(v, x, y):
	return max(min(v, y), x)

scalecache = {}
def scaleblit(screen, altura_esperada, obj, pos, area = None, escala_extra = 1):
	escala_tela = screen.get_height() / altura_esperada
	escala_total = escala_tela * escala_extra
	escalado = scalecache.get((obj, escala_total))
	if escalado == None:
		escalado = pygame.transform.scale_by(obj, escala_total)
		scalecache[(obj, escala_total)] = escalado
	if area != None:
		screen.blit(escalado, (pos[0] * escala_tela, pos[1] * escala_tela), pygame.rect.Rect(area[0] * escala_total, area[1] * escala_total, area[2] * escala_total, area[3] * escala_total))
	else:
		screen.blit(escalado, (pos[0] * escala_tela, pos[1] * escala_tela), None)

smoothscalecache = {}
def smoothscaleblit(screen, altura_esperada, obj, pos, area = None, escala_extra = 1):
	escala_tela = screen.get_height() / altura_esperada
	escala_total = escala_tela * escala_extra
	escalado = smoothscalecache.get((obj, escala_total))
	if escalado == None:
		escalado = pygame.transform.smoothscale_by(obj, escala_total)
		smoothscalecache[(obj, escala_total)] = escalado
	if area != None:
		screen.blit(escalado, (pos[0] * escala_tela, pos[1] * escala_tela), pygame.rect.Rect(area[0] * escala_total, area[1] * escala_total, area[2] * escala_total, area[3] * escala_total))
	else:
		screen.blit(escalado, (pos[0] * escala_tela, pos[1] * escala_tela), None)

def tint(obj, cor):
	obj = obj.copy()
	obj.fill((191, 191, 191, 255), None, pygame.BLEND_RGBA_MULT)
	obj.fill(cor, None, pygame.BLEND_RGB_ADD)
	return obj

def tint_mult(obj, cor):
	if cor != (255, 255, 255, 255) and cor != (255, 255, 255) and cor != "white":
		obj = obj.copy()
		obj.fill(cor, None, pygame.BLEND_RGBA_MULT)
	return obj

def blitanimado(screen, obj, pos, tempo, fps):
	frame_atual = int(tempo * fps) % len(obj)
	screen.blit(obj[frame_atual], pos)

def lerp(x, y, t):
	return x + (y - x) * t

def imagem_colide_com_rect(rect, obj, pos):
	return rect.colliderect(obj.get_rect().move(pos[0], pos[1]))

def colide_com_imagem(img, obj, pos):
	return img.get_at((int(pos[0]), int(pos[1])))[3] != 0\
		or img.get_at((int(pos[0]) + obj.get_width(), int(pos[1])))[3] != 0\
		or img.get_at((int(pos[0]), int(pos[1]) + obj.get_height()))[3] != 0\
		or img.get_at((int(pos[0]) + obj.get_width(), int(pos[1]) + obj.get_height()))[3] != 0

def movimento(pixelsporsegundo, delta):
	move_x = 0
	move_y = 0
	if pressionado[pygame.K_w] or pressionado[pygame.K_UP]:
		move_y -= 1
	if pressionado[pygame.K_s] or pressionado[pygame.K_DOWN]:
		move_y += 1
	if pressionado[pygame.K_a] or pressionado[pygame.K_LEFT]:
		move_x -= 1
	if pressionado[pygame.K_d] or pressionado[pygame.K_RIGHT]:
		move_x += 1
	length = math.sqrt(move_x * move_x + move_y * move_y)
	if length > 1:
		move_x /= length
		move_y /= length
	return (move_x * pixelsporsegundo * delta, move_y * pixelsporsegundo * delta)

def deslize(img, obj, pos, movimento):
	destino = (pos[0] + movimento[0], pos[1] + movimento[1])
	if colide_com_imagem(img, obj, destino):
		destino = (pos[0] + movimento[0], pos[1])
		if colide_com_imagem(img, obj, destino):
			destino = (pos[0], pos[1] + movimento[1])
			if colide_com_imagem(img, obj, destino):
				return pos
	return destino