import pygame
import util
import random

class Cenario:
    def __init__(self) -> None:
        self.bg = pygame.image.load('fnaf_minigame/sprites/cenario.png')
        self.mosquito_over = pygame.image.load('fnaf_minigame/sprites/bain.png')
        self.musquito1 = pygame.image.load('fnaf_minigame/sprites/')
        self.musquito2 = pygame.image.load('fnaf_minigame/sprites/')
        self.click = pygame.image.load('fnaf_minigame/sprites/')
        self.mosquito_die1 = pygame.image.load('fnaf_minigame/sprites/')
        self.mosquito_die2 = pygame.image.load('fnaf_minigame/sprites/')
        self.cont = 0
 #estou fazendo ainda, tenha calma, vou dar commit completo só quando eu tiver todos os sprites de mosquito.
    def frame(self, screen, delta, jogo):
        if self.cont <= 8:
            self.cont += 1
        self.screen.blit(self.bg)

        

