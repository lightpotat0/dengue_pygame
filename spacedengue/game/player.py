import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.imag = pygame.image.load("spacedengue/game/graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)