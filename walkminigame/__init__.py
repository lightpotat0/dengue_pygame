import pygame
from random import randint, choice

#Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('walkminigame/Sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(120, 474))

#Obstacle Class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, object, minigame):
        super().__init__()
        self.minigame = minigame
        self.object = object

        object_images = {
            'down': 'walkminigame/Sprites/bucketdown.png',
            'up': 'walkminigame/Sprites/trashup.png',
            'right': 'walkminigame/Sprites/tireright.png'
        }

        self.image = pygame.image.load(object_images[object]).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(300, 474))

    def update(self): #Update Obstacles
        keys = pygame.key.get_pressed()

        directions = {
            'down': pygame.K_DOWN,
            'up': pygame.K_UP,
            'right': pygame.K_RIGHT
        }

        if self.object in directions and keys[directions[self.object]]:
            self.kill()
            self.minigame.kills += 1
            self.minigame.spawn = True

#Main Game Class
class WalkMinigame:
    def __init__(self):
        self.screen = pygame.Surface((1280, 720))
        self.spawn = True
        
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())
        
        self.obstacles = pygame.sprite.Group()
        self.kills = 0
        
        # Clouds
        self.clouds = pygame.image.load('walkminigame/Sprites/cloudsbackground.png').convert_alpha()
        self.clouds_rect = self.clouds.get_rect(topleft=(0, 0))

        # Background
        self.background = pygame.image.load('walkminigame/Sprites/background.png').convert_alpha()
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        # Ground
        self.ground = pygame.image.load('walkminigame/Sprites/ground.png').convert_alpha()
        self.ground_rect = self.ground.get_rect(bottomleft=(0, 720))

    def frame(self, screen, delta, jogo):
        if self.spawn:
            self.obstacles.add(Obstacle(choice(['up', 'down', 'right']), self))
            self.spawn = False

        self.screen.fill('#87CEEB')
        self.screen.blit(self.clouds, self.clouds_rect)
        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.ground, self.ground_rect)
        
        self.player.draw(self.screen)

        
        self.obstacles.draw(self.screen)
        
        self.obstacles.update()
        
        screen.blit(pygame.transform.scale(self.screen, screen.get_size()), (0, 0))

        if self.kills >= 30:
            self.spawn = False
            return "ganhou"

'''
def main(): #Testejogo
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Walk Minigame')
    clock = pygame.time.Clock()
    jogo = WalkMinigame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        delta = clock.tick(60) / 1000
        result = jogo.frame(screen, delta, jogo)

        if result == "ganhou":
            print("Você ganhou!")
            running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
'''