import pygame
import util


screen_width = 1066
screen_height = 600
fundo = pygame.image.load("selecion/fundo.png")


def frame(self, screen):
    self.screen.blit(pygame.transform.scale(bg, (screen_width, screen_height)), (0, 0))