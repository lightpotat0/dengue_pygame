import pygame
import random
import tabuleiro

class Confete:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed_y = random.randint(1, 1)
        self.alpha = 255

    def update(self):
        self.y += self.speed_y
        self.alpha -= 5
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, tela):
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surface.fill((*self.color, self.alpha))
        tela.blit(surface, (self.x, self.y))

    def is_visible(self):
        return self.alpha > 0

class Tela:
    def __init__(self):
        self.color = (218, 165, 32)

        self.mensagem = "Fim de Jogo"
        self.mensagem1 = "Parabéns ao Jogador!"

        self.personagens = [
            pygame.image.load("assets/characterswalk1.png").convert_alpha(),
            pygame.image.load("assets/characterswalk2.png").convert_alpha(),
            pygame.image.load("assets/characterswalk3.png").convert_alpha(),
            pygame.image.load("assets/characterswalk4.png").convert_alpha()
        ]

        self.confetes = []
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            self.confetes.append(Confete(x, y))

        self.font = pygame.font.Font("Biblioteca de Assets/fontes/tt-milks-casual-pie-base.ttf", 50)

        self.frame_atual = 0
        self.tempo_frame = 250
        self.ultimo_tempo = pygame.time.get_ticks()

    def desenha_texto(self, tela, texto, tamanho, y):
        font = pygame.font.Font("Biblioteca de Assets/fontes/tt-milks-casual-pie-base.ttf", tamanho)
        text_surface = font.render(texto, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(tela.get_width() // 2, y))
        tela.blit(text_surface, text_rect.topleft)

    def desenha_tela_vitoria(self, tela):
        tela.fill(self.color)

        self.desenha_texto(tela, self.mensagem, 64, 150)
        self.desenha_texto(tela, self.mensagem1, 48, 220)

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tempo > self.tempo_frame:
            self.frame_atual = (self.frame_atual + 1) % len(self.personagens)
            self.ultimo_tempo = tempo_atual

        scaled_sprite = pygame.transform.scale(self.personagens[self.frame_atual].subsurface((2 * 24, 0 * 26 + 1, 24, 24)), (150, 150))
        sprite_rect = scaled_sprite.get_rect(center=(tela.get_width() // 2, 350))
        tela.blit(scaled_sprite, sprite_rect.topleft)

        for confete in self.confetes:
            confete.update()
            confete.draw(tela)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Tela de Vitória')

tela_vitoria = Tela()

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    tela_vitoria.desenha_tela_vitoria(screen)

    pygame.display.flip()
