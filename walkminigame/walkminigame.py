import pygame
from random import choice

#Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('walkminigame/Sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(120, 320))

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
        self.rect = self.image.get_rect(midbottom=(300, 320))

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

# Main Game Class
class WalkMinigame:
    def __init__(self):
        pygame.init()

        # Screen setup
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Walk Minigame')

        # Game variables
        self.clock = pygame.time.Clock()
        self.spawn = True
        self.kills = 0

        # Player setup
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        # Obstacles setup
        self.obstacles = pygame.sprite.Group()

        # Scenario setup
        self.ground = pygame.image.load('walkminigame/Sprites/ground.png').convert()
        self.groundrect = self.ground.get_rect(bottomleft=(0, 720))

        # Main loop control
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        if self.kills < 10 and self.spawn:
            self.obstacles.add(Obstacle(choice(['up', 'down', 'right']), self))
            self.spawn = False

        self.obstacles.update()

    def draw(self):
        self.screen.fill('Blue')
        self.screen.blit(self.ground, self.groundrect)

        self.player.draw(self.screen)
        self.obstacles.draw(self.screen)

        pygame.display.flip()

        if self.kills >= 10:
            print("Você ganhou!")
            self.running = False

    def quit(self):
        pygame.quit()

if __name__ == "__main__":
    game = WalkMinigame()
    game.run()
    game.quit()