import pygame
import random
import time

# imagens e fontes 
mosquito_image = pygame.image.load('fnaf_minigame/sprites/voando.png').convert_alpha()  
bg = pygame.image.load('fnaf_minigame/sprites/cenario.png').convert_alpha()  
tiro = pygame.image.load('fnaf_minigame/sprites/tiro.png').convert_alpha() 
vea = pygame.image.load('fnaf_minigame/sprites/vea.png').convert_alpha() 
screen_width = 1066  
screen_height = 600  
font = pygame.font.Font(None, 74)  

class Mosquito:
    def __init__(self):
        self.active = True
        self.atirou = None  # mosquito clicado
        self.fire_duration = 0.2  # tempo de tiro
        self.size = mosquito_image.get_width()  
        #posição do mosquito
        self.x = random.randint(0, screen_width - self.size)
        self.y = random.randint(0, screen_height - self.size)
        self.mosquito_rect = pygame.Rect(self.x, self.y, self.size, self.size)  # Retângulo do mosquito 
        self.speed_x = random.choice([2, 2])  # velocidade
        self.speed_y = random.choice([2, 2])  # velocidade 
        self.falling = False  
        self.inverted = False 

    def move(self):
        if not self.active and self.falling:
            self.y += 5  # mosquito caindo

            # mosquito parar de cair
            if self.y >= screen_height - mosquito_image.get_height():
                self.y = screen_height - mosquito_image.get_height()  
                self.falling = False  
        
        if self.active:
            # mosquito voando
            self.x += self.speed_x
            self.y += self.speed_y

            # atualiza o mosquito 
            self.mosquito_rect.topleft = (self.x, self.y)

            # inverte a direção do mosquito se ele bater nas bordas da tela
            if self.x <= 0 or self.x >= screen_width - mosquito_image.get_width():
                self.speed_x = -self.speed_x

            if self.y <= 0 or self.y >= screen_height - mosquito_image.get_height():
                self.speed_y = -self.speed_y

    def draw(self, screen):
        if self.active:
            screen.blit(mosquito_image, (self.x, self.y))

        # inverte o mosquito após o clique
        if self.atirou and (time.time() - self.atirou < self.fire_duration):
            mosquito_invertido = pygame.transform.flip(mosquito_image, True, True)
            screen.blit(mosquito_invertido, (self.x, self.y))
            self.inverted = True  
            self.falling = True  

        # mantém o mosquito no local
        elif not self.active and self.inverted:
            mosquito_invertido = pygame.transform.flip(mosquito_image, True, True)
            screen.blit(mosquito_invertido, (self.x, self.y))

    def deactivate(self):
        self.active = False  # O mosquito é desativado
        self.atirou = time.time()  # Marca o tempo do tiro
        self.falling = True

class Veia:
    def __init__(self, image_path, scale_factor=2):
        tamanho = (int(vea.get_width() * scale_factor), int(vea.get_height() * scale_factor)) #tamanho da vea
        self.image = pygame.transform.scale(vea, tamanho) 
        self.rect = self.image.get_rect()
        self.rect.centery = screen_height * 0.85 #coordenada da vea

    def update(self):
        mouse_x, _ = pygame.mouse.get_pos() #pega a posição do mouse
        self.rect.centerx = mouse_x #faz com que a posição da vea siga o mouse horizontalmente

    def draw(self, screen):
        screen.blit(self.image, self.rect) 

class PistolMosquito:

    tamanho = (screen_width, screen_height)  
    
    def __init__(self):
        # quantidade de mosquitos
        self.mosquitos = [Mosquito() for _ in range(10)]
        self.start_time = time.time()
        self.timer_duration = 5  # tempo pra atirar
        self.clock = pygame.time.Clock()  
        self.veia = Veia('fnaf_minigame/sprites/vea.png') 

    def event(self, event):
        # clicar
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.atirar(event.pos)  

    def atirar(self, posicao_click):
        # clicou no mosquito
        for mosquito in self.mosquitos:
            if mosquito.active and mosquito.mosquito_rect.collidepoint(posicao_click):
                mosquito.deactivate()  # mata o mosquito

    def get_tempo_da_perdicao(self, tempo_inicio):
       return tempo_inicio + self.timer_duration * 1000  # bixo que cresce o nariz

    def frame(self, screen, delta, jogo):
        elapsed_time = time.time() - self.start_time  
        screen.blit(pygame.transform.scale(bg, (screen_width, screen_height)), (0, 0))  

        self.veia.update()

        if elapsed_time < self.timer_duration:
            for mosquito in self.mosquitos:
                mosquito.move()
                mosquito.draw(screen)

            for mosquito in self.mosquitos:
                if mosquito.active:
                    break
            else:
                return "ganhou"  
        else:
            for mosquito in self.mosquitos:
                mosquito.deactivate()
            text = font.render("Você perdeu", True, (255, 0, 0))  # texto de derrota
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 1))  # Exibe o texto centralizado
            if elapsed_time >= self.timer_duration + 2:  # Dá um intervalo de 2 segundos antes de finalizar
                return "perdeu"
            
        self.veia.draw(screen)