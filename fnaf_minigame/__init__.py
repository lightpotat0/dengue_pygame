import pygame
import util
import random

class Cenario:
    def __init__(self) -> None:
        self.bg = pygame.image.load('fnaf_minigame/sprites/cenario.png')
        self.mosquito_over = pygame.image.load('fnaf_minigame/sprites/bain.png')
        self.mosquito_posicao = "lá"
      #  self.mosquito_situacion = "vivo"
        self.musquito_door = pygame.image.load('fnaf_minigame/sprites/mosquito_door1.png')
        self.musquito_door1 = pygame.image.load('fnaf_minigame/sprites/mosquito_door2.png')
        #self.click = pygame.image.load('fnaf_minigame/sprites/')
       # self.clicou = "clicou"
      #  self.mosquito_die1 = pygame.image.load('fnaf_minigame/sprites/mosquito_die1')
        #self.mosquito_die2 = pygame.image.load('fnaf_minigame/sprites/')
        self.cont = 0
        self.timer = random.randrange(0, 3)
 
    def frame(self, screen, delta, jogo,):

        #bixos aparecendo
        if self.cont < self.timer:
            self.cont += delta
        else:
            self.mosquito_posicao = "aqui"

        if self.cont < self.timer:
            self.cont += delta
        else:
            self.mosquito_posicao = "acula"          
        
        #click 
       # for event in events:
        #    if event.type == pygame.MOUSEBUTTONUP:
       #         if self.rect.collidepoint(event.pos):
           #         self.clicou = "clicada"

        screen.blit(pygame.transform.scale(self.bg, screen.get_size()), (0, 0))
        match self.mosquito_posicao:
            case "aqui":
                util.scaleblit(screen, 180, self.musquito_door, (0, 55))
            case "acula":
                util.scaleblit(screen, 180, self.musquito_door1, (200, 55))
        
       # match self.clicou:
         #   case "clicada":
           #     util.scaleblit(screen, 180, self.mosquito_die1, (0, 55))
            
