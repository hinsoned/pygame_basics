import pygame
# using from imports only a portion of sys
# exit closes any code you are running
from sys import exit

#this must be run before all other pygame code. It starts pygame.
pygame.init()

#this is to create the window the player will see. The display surface.
#You must pass in at least one argument here, a tuple with the 
#width and height of the game window
screen = pygame.display.set_mode((800, 400))

#change the name of the game window
pygame.display.set_caption('Runner')
#create a clock to control frame rate
clock = pygame.time.Clock()
#create a font. None will be a default pygame font
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = True

# this is a surface to go on the display surface. Takes a file path to an image
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
# text must be rendered to a surface then blitted on to the display surface
text_surface = test_font.render('My Game', False, (64, 64, 64))
text_rect = text_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

#this loop is always true so it must be broken from the inside
#the entire game runs in this. It is what keeps the screen created
#above from just disappearing imediately.
while True:

    mouse_pos = pygame.mouse.get_pos()
    #this is the event loop or event handler
    #it looks for input and handles it
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #this is effectively the opposit of pygame.init()
            pygame.quit()
            # exit closes the code running the while loop
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(mouse_pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 800
    
    #draw and update all elements here
            
    if game_active:
        #now draw the surface on the display surface 
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        pygame.draw.rect(screen, '#c0e8ec' , text_rect)
        pygame.draw.rect(screen, '#c0e8ec', text_rect, 10)

        screen.blit(text_surface, text_rect)
        snail_rect.left -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill('Blue')

    #this updates the display surface each time the code reads it
    pygame.display.update()
    #this tells pygame to not run the while loop more than 60 times per second
    clock.tick(60)