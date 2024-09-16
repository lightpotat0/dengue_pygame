import pygame

screen_width = 1066
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
size1 = (200, 300)
size2 = (100, 100)
size3 = (50, 50)

fundo = pygame.image.load("selecion/fundo.png")
enzo = pygame.transform.scale(pygame.image.load("selecion/enzo_gabriel.jpg"), size1)
jm = pygame.transform.scale(pygame.image.load("selecion/joao_maria.jpg"), size1)
an = pygame.transform.scale(pygame.image.load("selecion/ana_leticia.jpg"), size1)
hk = pygame.transform.scale(pygame.image.load("selecion/helena_karan.jpg"), size1)

c_enzo = pygame.transform.scale(pygame.image.load("selecion/enzu.jpg"), size2)
c_jm = pygame.transform.scale(pygame.image.load("selecion/jm.jpg"), size2)
c_an = pygame.transform.scale(pygame.image.load("selecion/an.jpg"), size2)
c_hk = pygame.transform.scale(pygame.image.load("selecion/hk.jpg"), size2)

number1 = pygame.transform.scale(pygame.image.load("selecion/1.png"), size3)
number2 = pygame.transform.scale(pygame.image.load("selecion/2.png"), size3)
number3 = pygame.transform.scale(pygame.image.load("selecion/3.png"), size3)
number4 = pygame.transform.scale(pygame.image.load("selecion/4.png"), size3)

hover_sprites = [
	pygame.image.load("assets/characterswalk1.png"),
	pygame.image.load("assets/characterswalk2.png"),
	pygame.image.load("assets/characterswalk3.png"),
	pygame.image.load("assets/characterswalk4.png")
]

border_color_vermei = (255, 0, 0)
border_color_azuli = (0, 162, 255)
border_color_amare = (255, 196, 0)
border_color_verdi = (24, 196, 26)
border_size = 10
border_size1 = 5
border_radius = 10


def draw_image_with_border(screen, image, pos, border_color, border_size, border_radius):
    image_rect = image.get_rect(topleft=pos)
    
    pygame.draw.rect(screen, border_color, 
                     (image_rect.x - border_size, image_rect.y - border_size, 
                      image_rect.width + border_size*2, image_rect.height + border_size*2), border_radius=border_radius)
    
    screen.blit(image, pos)
    return image_rect 

def frame(screen, bg):
    screen.blit(pygame.transform.scale(bg, (screen_width, screen_height)), (0, 0))

def is_mouse_over(image_rect):
    mouse_pos = pygame.mouse.get_pos()
    return image_rect.collidepoint(mouse_pos)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame(screen, fundo)

    jm_rect = draw_image_with_border(screen, jm, (50, 50), border_color_vermei, border_size, border_radius)
    hk_rect = draw_image_with_border(screen, hk, (305, 50), border_color_azuli, border_size, border_radius)
    enzo_rect = draw_image_with_border(screen, enzo, (560, 50), border_color_verdi, border_size, border_radius)
    an_rect = draw_image_with_border(screen, an, (820, 50), border_color_amare, border_size, border_radius)

    draw_image_with_border(screen, c_jm, (300, 420), border_color_vermei, border_size1, border_radius)
    draw_image_with_border(screen, c_hk, (420, 420), border_color_azuli, border_size1, border_radius)
    draw_image_with_border(screen, c_enzo, (540, 420), border_color_verdi, border_size1, border_radius)
    draw_image_with_border(screen, c_an, (660, 420), border_color_amare, border_size1, border_radius)

    screen.blit(number1, (52, 55))  
    screen.blit(number2, (308, 55))  
    screen.blit(number3, (563, 55))  
    screen.blit(number4, (823, 55))

    if is_mouse_over(jm_rect):
        sprite_to_blit = pygame.transform.scale(hover_sprites[3].subsurface((2 * 24, 0 * 26 + 1, 24, 24)), (150, 150))
        screen.blit(sprite_to_blit, (65, 380))
    elif is_mouse_over(hk_rect):
        sprite_to_blit = pygame.transform.scale(hover_sprites[3].subsurface((1 * 24, 0 * 26 + 1, 24, 24)), (150, 150))
        screen.blit(sprite_to_blit, (65, 380))
    elif is_mouse_over(enzo_rect):
        sprite_to_blit = pygame.transform.scale(hover_sprites[3].subsurface((3 * 24, 0 * 26 + 1, 24, 24)), (150, 150))
        screen.blit(sprite_to_blit, (65, 380))
    elif is_mouse_over(an_rect):
        sprite_to_blit = pygame.transform.scale(hover_sprites[3].subsurface((0 * 24, 0 * 26 + 1, 24, 24)), (150, 150))
        screen.blit(sprite_to_blit, (65, 380))
    pygame.display.flip()

pygame.quit()