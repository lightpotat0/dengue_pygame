import pygame
import util
import random

class Cenario:
    def __init__(self) -> None:
        self.bg = pygame.image.load('fnaf_minigame/sprites/cenario.png')
        self.mosquito_over = pygame.image.load('fnaf_minigame/sprites/bain.png')
        self.mosquito_posicao = "lá"
        self.mosquito_situacion = "vivo"
        self.musquito_door = pygame.image.load('fnaf_minigame/sprites/mosquito_door1.png')
        #self.musquito2 = pygame.image.load('fnaf_minigame/sprites/')
        #self.click = pygame.image.load('fnaf_minigame/sprites/')
        #self.mosquito_die1 = pygame.image.load('fnaf_minigame/sprites/mosquito_die1')
        #self.mosquito_die2 = pygame.image.load('fnaf_minigame/sprites/')
        self.cont = 0
 
    def frame(self, screen, delta, jogo):
        if self.cont < 0:
            self.cont += delta
        else:
            self.mosquito_posicao = "aqui"

        screen.blit(pygame.transform.scale(self.bg, screen.get_size()), (0, 0))
        match self.mosquito_posicao:
            case "aqui":
                util.scaleblit(screen, 180, self.musquito_door, (0, 55))

            
