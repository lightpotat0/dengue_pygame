import pygame
from random import choice

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('walkminigame/Sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(120, 474))

# Obstacle Class
class Obstacle(pygame.sprite.Sprite):
    directions = {
        'down': pygame.K_DOWN,
        'up': pygame.K_UP,
        'right': pygame.K_RIGHT
    }
    object_images = {
            'down': 'walkminigame/Sprites/bucketdown.png',
            'up': 'walkminigame/Sprites/trashup.png',
            'right': 'walkminigame/Sprites/tireright.png'
    }

    def __init__(self, object, minigame, index):
        super().__init__()
        #Objects Main Var
        self.minigame = minigame
        self.object = object
        self.index = index

        #Objects Image
        self.image = pygame.image.load(self.object_images[object]).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(300 + self.index*200, 474))

    def update(self):
        keys = pygame.key.get_pressed()
        direction_key = self.directions[self.object]

        #Trigger Check
        if not self.minigame.trigger:
            return

        #Key Check
        if keys[direction_key] and self.index == self.minigame.kills:
            self.kill()
            self.minigame.kills += 1
            self.minigame.trigger = False

# Main Game Class
class WalkMinigame:
    tamanho = (1280, 720)
    smooth = True
    def __init__(self):
        #Main Vars
        self.spawn = True
        self.trigger = False
        self.kills = 0

        #Player
        self.player = pygame.sprite.GroupSingle(Player())

        #Obstacles
        self.obstacles = pygame.sprite.Group()

        #Scenario
        self.clouds = pygame.image.load('walkminigame/Sprites/cloudsbackground.png').convert_alpha()
        self.clouds_rect = self.clouds.get_rect(topleft=(0, 0))
        self.background = pygame.image.load('walkminigame/Sprites/background.png').convert_alpha()
        self.background_rect = self.background.get_rect(topleft=(0, 0))
        self.ground = pygame.image.load('walkminigame/Sprites/ground.png').convert_alpha()
        self.ground_rect = self.ground.get_rect(bottomleft=(0, 720))

    def frame(self, screen, delta):
        #Trigger Check
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.trigger = True

        #Obstacle Spawn
        if self.spawn:
            for i in range(30):
                self.obstacles.add(Obstacle(choice(['up', 'down', 'right']), self, i))
            self.spawn = False

        #Scenario
        screen.fill('#87CEEB')
        screen.blit(self.clouds, self.clouds_rect)
        screen.blit(self.background, self.background_rect)
        screen.blit(self.ground, self.ground_rect)

        #Player
        self.player.draw(screen)

        #Obstcles
        self.obstacles.draw(screen)
        self.obstacles.update()

        #Win Check
        if self.kills >= 30:
            return "ganhou"

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Walk Minigame')
    clock = pygame.time.Clock()
    jogo = WalkMinigame()
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        delta = clock.tick(60) / 1000
        result = jogo.frame(screen, delta)

        if result == "ganhou":
            print("Você ganhou!")
            running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()