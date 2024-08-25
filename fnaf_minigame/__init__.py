import pygame
import util
import random

class Pistol_mosquito:
    def __init__(self) -> None:
        self.bg = pygame.image.load('fnaf_minigame/sprites/cenario.png')
        self.mosquito_over = pygame.image.load('fnaf_minigame/sprites/bain.png')
        self.cisterna = pygame.image.load('fnaf_minigame/sprites/cisterna.png')
        self.mosquito_posicao = "lá"
        self.musquito_door = pygame.image.load('fnaf_minigame/sprites/mosquito_door1.png')
        self.musquito_door1 = pygame.image.load('fnaf_minigame/sprites/mosquito_door2.png')
        self.mosquito_die1 = pygame.image.load('fnaf_minigame/sprites/mosquito_die1')
        #self.mosquito_die2 = pygame.image.load('fnaf_minigame/sprites/')
        self.cont = 0
        self.timer = random.randrange(0, 3)
 
    def frame(self, screen, delta, jogo,):
        screen.blit(self.cisterna, (0, 55))
        #bixos aparecendo
        if self.cont < self.timer:
            self.cont += delta
        else:
            self.mosquito_posicao = "aqui"
            util.scaleblit(screen, 180, self.cisterna, (200, 55))

        if self.cont < self.timer:
            self.cont += delta
        else:
            self.mosquito_posicao = "acula"          
            util.scaleblit(screen, 180, self.cisterna, (200, 55))
        
        #click
        run = True 
        while run:

            if pygame.mouse.get_pressed()[0] == True:
                self.mosquito_posicao = "clicada"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        screen.blit(pygame.transform.scale(self.bg, screen.get_size()), (0, 0))
        match self.mosquito_posicao:
            case "aqui":
                util.scaleblit(screen, 180, self.musquito_door, (0, 55))
            case "acula":
                util.scaleblit(screen, 180, self.musquito_door1, (200, 55))
            case "clicada":
                util.scaleblit(screen, 180, self.mosquito_die1, (0, 55))
            
