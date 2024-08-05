#MiniGame David
import pygame
from random import randint, choice
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        #Sprites
        self.image = pygame.image.load('walkminigame\Sprites\player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(120, 320))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,object):
        super().__init__()

        self.object = object

        if object == 'down':
            self.image = pygame.image.load('walkminigame/Sprites/down.png').convert_alpha()
        elif object == 'up':
            self.image = pygame.image.load('walkminigame/Sprites/up.png').convert_alpha()
        elif object == 'right':
            self.image = pygame.image.load('walkminigame/Sprites/right.png').convert_alpha()

        self.rect = self.image.get_rect(midbottom=(300, 320))

    def update(self):
        global spawn
        keys = pygame.key.get_pressed()
        if self.object == 'down' and keys[pygame.K_DOWN]:
            self.kill()
        if self.object == 'up' and keys[pygame.K_UP]:
            self.kill()
        if self.object == 'right' and keys[pygame.K_RIGHT]:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Alerta Mosquito')
clock = pygame.time.Clock()
spawn = 3

#Player
player = pygame.sprite.GroupSingle()
player.add(Player())

#Obstacle
obstacles = pygame.sprite.Group()

#Ground
ground = pygame.image.load('walkminigame\Sprites\ground.png').convert()
groundrect = ground.get_rect(bottomleft = (0,720))

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    while len(obstacles) < 10:
        obstacles.add(Obstacle(choice(['up', 'down', 'right'])))


    screen.fill('Blue')
    screen.blit(ground,groundrect)

    player.draw(screen)

    obstacles.draw(screen)
    obstacles.update()

    pygame.display.update()
    clock.tick(60)