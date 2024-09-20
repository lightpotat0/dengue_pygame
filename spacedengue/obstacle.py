import pygame

wall = pygame.image.load("spacedengue/graphics/wall.png").convert_alpha()

class Block(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y, row, col):
        super().__init__()
        #self.image = pygame.Surface((size,size))
        #self.image.fill(color)
        self.image = wall.subsurface(pygame.Rect((col * size, row * size, size, size)))
        self.rect = self.image.get_rect(topleft = (x,y))

shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']