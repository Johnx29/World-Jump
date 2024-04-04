# Add other libraries to be used in the game or any python scripts
import pygame
from player import Player
from ground import Ground

# PyGame essentials setup
pygame.init()
screen_width = 960
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Change caption text and change default icon to custom icon
caption = "Platformer Game"
icon = pygame.image.load("assets/player/p1_stand.png")
pygame.display.set_caption(caption)
pygame.display.set_icon(icon)

# Call our functions to create the objects
player = Player("assets/player/p1_stand.png")
ground = Ground("assets/grassMid.png")

# Create a variable to store our background
background = pygame.image.load("assets/background.png").convert_alpha()

# Configurations
jumped = False
collided = False
step = 5
gravity = 2

# Setup collision groups
player_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
player_group.add(player)
floor_group.add(ground)

def start_game():
    """Handles all the game logic without messing with the default PyGame game loop
    """

    # Decrease player gravity allowing us to make them fall
    # player.rect.y += gravity - 1

    # Easy method to create ground maybe?
    # for i in range(0, screen_width, 70):
        # floor_group.add(ground)
        # screen.blit(ground.sprite, (i, 200 + screen_height / 2))

    # Efficient way for checking collisions, uses the mask passed through spritecollide (Pixel Perfect)
    if pygame.sprite.spritecollide(player, floor_group, False, pygame.sprite.collide_mask):
        print("Hit")

    floor_group.update((250, 250), "WTF")

    # Rendering / Drawing our images as sprites on screen
    floor_group.draw(screen)
    player_group.draw(screen)

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
        player.rect.x -= step
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        print("Right")
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