import pygame

wall = pygame.image.load("spacedengue/graphics/wall.png").convert_alpha()

class Block(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y, row, col):
        super().__init__()
        self.image = pygame.transform.scale(wall, (size * len(shape[0]), size * len(shape))).subsurface(pygame.Rect(col * size, row * size, size, size))
        self.rect = self.image.get_rect(topleft = (x,y))

shape = [
'  xxxxxxx  ',
' xxxxxxxxx ',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = wall
        self.rect = self.image.get_rect(topleft = pos)