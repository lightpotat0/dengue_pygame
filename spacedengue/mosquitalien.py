import pygame

class Mosquito(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        file_path = '../graphics/' + color + '.png'
        self.nave = pygame.image.load(file_path).convert_alpha()
        self.rect = self.nave.get_rect(topleft = (x,y))
        