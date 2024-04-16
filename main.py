# Add other libraries to be used in the game or any python scripts
import pygame
from player import Player
from block import Block
from door import Door

def show_debug_menu():
    example = create_text(f"Left: {player.rect.left}")
    example2 = create_text(f"Right: {player.rect.right}")
    example3 = create_text(f"Top: {player.rect.top}")
    example4 = create_text(f"Bottom: {player.rect.bottom}")
    example5 = create_text(f"X: {player.rect.x} | Y: {player.rect.y}")

    screen.blit(example, (0, 0))
    screen.blit(example2, (0, 40))
    screen.blit(example3, (0, 80))
    screen.blit(example4, (0, 120))
    screen.blit(example5, (0, 160))

def create_text(text):
    font = pygame.font.SysFont("Arial", 20)
    new_text = font.render(text, True, ("black"))
    return new_text

def create_floor():
    for i in range(0, screen_width, 70):
        floor = Block("assets/grassMid.png", i, screen_height - 70)
        all_group.add(floor)

def create_block(x, y):
    new_block = Block("assets/grassMid.png", x, y)
    all_group.add(new_block)

def create_door(x, y):
    new_door = Door(x, y)
    door_group.add(new_door)

# PyGame essentials setup
pygame.init()
screen_width = 960
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60
running = True

# Change caption text and change default icon to custom icon
icon = pygame.image.load("assets/player/p1_stand.png")
caption = "Platformer Game"
pygame.display.set_icon(icon)
pygame.display.set_caption(caption)

# Variable to store our background image
background = pygame.image.load("assets/background.png").convert_alpha()

font = pygame.font.SysFont("arial", 30)
text = font.render("Blah", False, ("black"))

# Create objects like player
player = Player(100, 300)

# Setup collision groups
player_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
player_group.add(player)

# Create the floor
create_floor()
create_block(100, 200)
create_block(400, 400)
create_door(screen_width - 70, 400)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call the function that handles all our player movement and logic
    # block.update(player_group)
    player.update(all_group, door_group)

    # Refresh the screen
    screen.fill("white")

    # Show background replacing the screen color
    screen.blit(background, (0, 0))
    show_debug_menu()
    # Render player and objects on screen
    all_group.draw(screen)
    door_group.draw(screen)
    player_group.draw(screen)

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(fps)

pygame.quit()