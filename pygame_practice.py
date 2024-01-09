import pygame
# using from imports only a portion of sys
# exit closes any code you are running
from sys import exit
from random import randint

#keep track of the time the player has played
def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f'SCORE: {current_time//1000}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: 
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    #display walk or jump animation
    global player_surface, player_index

    if player_rect.bottom <300:
        # jump
        player_surface = player_jump
    else:
        # walk
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
        

# this must be run before all other pygame code. It starts pygame.
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
game_active = False
start_time = 0
score = 0

# this is a surface to go on the display surface. Takes a file path to an image
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
# text must be rendered to a surface then blitted on to the display surface
#text_surface = test_font.render('My Game', False, (64, 64, 64))
#text_rect = text_surface.get_rect(center = (400, 50))

#snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

#fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

#Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect( center = (400,200))

intro_text = test_font.render('Pixel Runner', False, (111,196,169))
intro_text_rect = intro_text.get_rect(center = (400,80))
restart_text = test_font.render('Press Space To Start', False, (111,196,169))
restart_text_rect = restart_text.get_rect(center = (400,330))
#this loop is always true so it must be broken from the inside
#the entire game runs in this. It is what keeps the screen created
#above from just disappearing imediately.

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer =pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer =pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 500)



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
            if event.type == obstacle_timer:
                if randint(0,2):
                    new_snail_rect = snail_surface.get_rect(bottomright=(randint(900, 1100), 300))
                    obstacle_rect_list.append(new_snail_rect)
                else:
                    new_fly_rect = fly_surface.get_rect(bottomright=(randint(900, 1100), 210))
                    obstacle_rect_list.append(new_fly_rect)
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()
        

    #draw and update all elements here
            
    if game_active:
        #now draw the surface on the display surface 
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        #pygame.draw.rect(screen, '#c0e8ec' , text_rect)
        #pygame.draw.rect(screen, '#c0e8ec', text_rect, 10)
        #screen.blit(text_surface, text_rect)
        score = display_score()//1000

        #obstacle movment
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        # collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        #these reset the player and the obstacle list
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
    
        score_message = test_font.render(f'Your Score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(intro_text, intro_text_rect)
        if score == 0:
            screen.blit(restart_text, restart_text_rect)
        else:
            screen.blit(score_message, score_message_rect)

    #this updates the display surface each time the code reads it
    pygame.display.update()
    #this tells pygame to not run the while loop more than 60 times per second
    clock.tick(60)