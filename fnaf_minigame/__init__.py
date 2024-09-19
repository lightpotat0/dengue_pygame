import pygame
import random
import time

# Carregando os recursos
mosquito_image = pygame.image.load('fnaf_minigame/sprites/voando.png').convert_alpha()
bg = pygame.image.load('fnaf_minigame/sprites/cenario.png').convert_alpha()
tiro = pygame.image.load('fnaf_minigame/sprites/tiro.png').convert_alpha()
screen_width = 1066
screen_height = 600
font = pygame.font.Font(None, 74)

class Mosquito:
    def __init__(self):
        self.active = True
        self.atirou = None
        self.fire_duration = 0.2
        self.size = mosquito_image.get_width()
        self.x = random.randint(0, screen_width - self.size)
        self.y = random.randint(0, screen_height - self.size)
        self.mosquito_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])

    def move(self):
        if not self.active:
            return

        self.x += self.speed_x
        self.y += self.speed_y

        self.mosquito_rect.topleft = (self.x, self.y)

        # Inverter a direção ao atingir as bordas
        if self.x <= 0 or self.x >= screen_width - mosquito_image.get_width():
            self.speed_x = -self.speed_x

        if self.y <= 0 or self.y >= screen_height - mosquito_image.get_height():
            self.speed_y = -self.speed_y

    def draw(self, screen):
        if self.active:
            screen.blit(mosquito_image, (self.x, self.y))

        if self.atirou and (time.time() - self.atirou < self.fire_duration):
            screen.blit(tiro, (self.x, self.y))

    def deactivate(self):
        self.active = False
        self.atirou = time.time()

class PistolMosquito:
    tamanho = (screen_width, screen_height)
    
    def __init__(self):
        # Criar os mosquitos
        self.mosquitos = [Mosquito() for _ in range(15)]
        # Timer do jogo
        self.start_time = time.time()
        self.timer_duration = 5
        self.clock = pygame.time.Clock()

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.atirar(event.pos)

    def atirar(self, posicao_click):
        # Verifica se o clique foi em um mosquito
        for mosquito in self.mosquitos:
            if mosquito.active and mosquito.mosquito_rect.collidepoint(posicao_click):
                mosquito.deactivate()

    def get_tempo_da_perdicao(self, tempo_inicio):
        return tempo_inicio + self.timer_duration * 1000

    def frame(self, screen, delta, jogo):
        elapsed_time = time.time() - self.start_time
        screen.blit(pygame.transform.scale(bg, (screen_width, screen_height)), (0, 0))
        
        if elapsed_time < self.timer_duration:
            for mosquito in self.mosquitos:
                mosquito.move()
                mosquito.draw(screen)
            for mosquito in self.mosquitos:
                if mosquito.active:
                    break
            else:
                return "ganhou"
        else:
            for mosquito in self.mosquitos:
                mosquito.deactivate()
            text = font.render("Você perdeu", True, (255, 0, 0))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 1))
            if elapsed_time >= self.timer_duration + 2:
                return "perdeu"
