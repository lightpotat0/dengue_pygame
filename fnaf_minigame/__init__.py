import pygame
import util
import random
import time

#coisas
mosquito_image = pygame.image.load('fnaf_minigame/sprites/voando.png')
bg = pygame.image.load('fnaf_minigame/sprites/cenario.png')
cisterna = pygame.image.load('fnaf_minigame/sprites/cisterna.png')
bain = pygame.image.load('fnaf_minigame/sprites/bain.png')
tiro = pygame.image.load('fnaf_minigame/sprites/tiro.png')
mira = pygame.image.load('fnaf_minigame/sprites/mira.png')
screen_width = 1066
screen_height = 600
screen1 = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(None, 74)

class PistolMosquito:
    def __init__(self):
        self.image = mosquito_image
        self.size = self.image.get_width()
        self.x = random.randint(0, screen_width - self.size)
        self.y = random.randint(0, screen_height - self.size)
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])
        self.mosquito_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.active = True
        self.atirou = None
        self.fire_duration = 0.2

    def move(self):

        if not self.active:
            return
        
        self.x += self.speed_x
        self.y += self.speed_y

        self.mosquito_rect.topleft = (self.x, self.y)

        #inverte a direção bla bla bla
        if self.x <= 0 or self.x >= screen_width - self.image.get_width():
            self.speed_x = -self.speed_x

        if self.y <= 0 or self.y >= screen_height - self.image.get_height():
            self.speed_y = -self.speed_y

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

        if self.atirou and (time.time() - self.atirou < self.fire_duration):
            screen.blit(tiro, (self.x, self.y))

    def deactivate(self):
        self.active = False
        self.atirou = time.time()

# quantidade de mosquito
mosquitos = [PistolMosquito() for _ in range(15)]

#timer
start_time = time.time()
timer_duration = 5

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            mouse_pos = pygame.mouse.get_pos()
            for mosquito in mosquitos:
                if mosquito.mosquito_rect.collidepoint(mouse_pos):
                    mosquito.deactivate()
    elapsed_time = time.time() - start_time

    screen1.blit(pygame.transform.scale(bg, (screen_width, screen_height)), (0, 0))
    util.scaleblit(screen1, 150, cisterna, (82, 30))

    if elapsed_time < timer_duration:
        for mosquito in mosquitos:
            mosquito.move()
            mosquito.draw(screen1)
    else:
        for mosquito in mosquitos:
            mosquito.deactivate()
        text = font.render("Você perdeu", True, (255, 0, 0))
        screen1.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 1))
        util.scaleblit(screen1, 150, bain, (82, 30))

    pygame.display.flip()
    clock.tick(60)
