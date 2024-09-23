import pygame
import math

pressionado = pygame.key.get_pressed()
pressionado_agora = pressionado
mouse_pos = (0, 0)

def mouse_pos_para(screen, altura_esperada):
	escala = altura_esperada / screen.get_height()
	return (mouse_pos[0] * escala, mouse_pos[1] * escala)

andamentos = [
	pygame.image.load("assets/characterswalk1.png"),
	pygame.image.load("assets/characterswalk2.png"),
	pygame.image.load("assets/characterswalk3.png"),
	pygame.image.load("assets/characterswalk4.png")
]

icones = [
	pygame.image.load("assets/2.png"),
	pygame.image.load("assets/4.png"),
	pygame.image.load("assets/1.png"),
	pygame.image.load("assets/3.png")
]

def clamp(v, x, y):
	return max(min(v, y), x)

cache_anterior = {}
cache_atual = {}
def clear_cache():
	global cache_anterior, cache_atual
	cache_anterior.clear()
	cache_anterior = cache_atual
	cache_atual = {}

def scaledrawrect(screen, altura_esperada, color, rect, border_radius = -1):
	escala = screen.get_height() / altura_esperada
	pygame.draw.rect(screen, color, (rect[0] * escala, rect[1] * escala, rect[2] * escala, rect[3] * escala), border_radius = border_radius)

def scaleblit(screen, altura_esperada, obj, pos, area = None, escala_extra = 1):
	# calcular a escala
	escala_tela = screen.get_height() / altura_esperada
	escala_total = escala_tela * escala_extra

	if area == None: # area padrão do objeto
		area = obj.get_rect()
	else:
		area = pygame.Rect(area)

	escalado = pygame.transform.scale_by(obj.subsurface(area), escala_total)
	screen.blit(escalado, (pos[0] * escala_tela, pos[1] * escala_tela))

# escala um objeto com smoothscale
def smoothscaleblit(screen, altura_esperada, obj, pos, area = None, escala_extra = 1, fake = False):
	escala_tela = screen.get_height() / altura_esperada
	escala_total = escala_tela * escala_extra

	if area == None: # area padrão do objeto
		area = obj.get_rect()
	else:
		area = pygame.Rect(area)

	key = (obj, area[0], area[1], area[2], area[3], escala_total)
	escalado = cache_atual.get(key)
	if escalado == None:
		if int(obj.get_height() * escala_total) != obj.get_height():
			escalado = cache_anterior.get(key)
			if escalado == None:
				escalado = pygame.transform.smoothscale_by(obj.subsurface(area), escala_total)
			cache_atual[key] = escalado
		else:
			escalado = obj
	if not fake:
		screen.blit(escalado, (pos[0] * escala_tela, pos[1] * escala_tela))

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
	return x + (y - x) * clamp(t, 0, 1)

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

# baseado em uma funcao tirada da wiki
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def smoothscale_draw_text(surface, altura_esperada, text, color, rect, font, escala=1, aa=True, bkg=None, sombra=False):
	rect = pygame.Rect(rect)
	if sombra:
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(-0.5, -0.5), font, escala)
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(-1, 0), font, escala)
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(-0.5, 0.5), font, escala)
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(0, -1), font, escala)
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(0, 0), font, escala)
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(0, 1), font, escala)
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(0.5, -0.5), font, escala)
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(1, 0), font, escala)
		smoothscale_draw_text(surface, altura_esperada, text, (0, 0, 0, 63), rect.move(0.5, 0.5), font, escala)
	y = rect.top
	lineSpacing = -2

	# get the height of the font
	fontHeight = font.size("Tg")[1] * escala
	rect.width /= escala
	rect.height /= escala

	while text:
		i = 1

		# determine if the row of text will be outside our area
		#if y + fontHeight > rect.bottom:
		#	break

		# determine maximum width of line
		while font.size(text[:i])[0] < rect.width and i < len(text):
			i += 1

		# if we've wrapped the text, then adjust the wrap to the last word
		if i < len(text):
			i = text.rfind(" ", 0, i) + 1

		# render the line and blit it to the surface
		if bkg:
			image = font.render(text[:i], 1, color, bkg)
			image.set_colorkey(bkg)
		else:
			image = font.render(text[:i], aa, color)

		smoothscaleblit(surface, altura_esperada, image, (rect.left, y), None, escala)
		y += fontHeight + lineSpacing

		# remove the text we just blitted
		text = text[i:]

		if i == 0:
			break

	return text