# Platformer game made in PyGame by Johnny Huang (340893478) 
# Add other libraries to be used in the game or any python scripts
import pygame
from player import Player
from ground import Ground

# PyGame essentials setup
pygame.init()
screen_width = 960
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# Change caption text and change default icon to custom icon
caption = "Platformer Game"
icon = pygame.image.load("assets/player/p1_stand.png")
pygame.display.set_caption(caption)
pygame.display.set_icon(icon)

player = Player("assets/player/p1_stand.png")
ground = Ground("assets/grassMid.png")

# Create a variable to store our background
background = pygame.image.load("assets/background.png").convert_alpha()

# Setup collision groups
player_group = pygame.sprite.Group()
# player_group.add(ground_rect)
# print(player_group)

# Configurations
step = 5
gravity = 2

jumped = False
collided = False

def start_game():
    # Decrease player gravity allowing us to make them fall
    if not collided:
        player.rect.y += gravity - 1

    # Easy method to create ground maybe?
    for i in range(0, screen_width, 70):
        screen.blit(ground.sprite, (i, 200 + screen_height / 2))

    # player_mask = pygame.mask.from_surface(player_sprite)
    # mask = player_mask.to_surface()

    # offset_x = player.rect.x - ground_rect.x
    # offset_y = player.rect.y - ground_rect.y

    # print(offset_y)

    # if player_mask.overlap(ground_mask, (offset_x, offset_y)):
    #     print("Collided with floor")
    #     player.rect.x = player.rect.x
    #     player.rect.y = player.rect.y
    #     collided = True
    # else:
    #     print("Not colliding")
    #     collided = False

    # Show player on screen with the mask
    # screen.blit(player.mask, (player.rect.x, player.rect.x))
    screen.blit(player.sprite, (player.rect.x, player.rect.y))
    
    # for i in range(0, 80, 70):
    #     screen.blit(platform.sprite, (i, 300))

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key inputs
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        print("Jumped")
        player.rect.y -= step
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        print("Left")
        # player_sprite = pygame.image.load("assets/idle.png").convert_alpha()
        player.rect.x -= step
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        print("Right")
        # player_sprite = pygame.image.load("assets/idle.png").convert_alpha()
        player.rect.x += step

    # Refresh the screen
    screen.fill("white")

    # Show background replacing the screen color
    screen.blit(background, (0, 0))

    # This calls the start game function which allows our main loop to stay organized
    start_game()

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(60)

pygame.quit()