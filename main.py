# Add other libraries to be used in the game or any python scripts
import pygame
from pytmx.util_pygame import load_pygame
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

def create_platform(x, y, target):
    offset = 0
    for i in range(1, target+1):
        create_block(x + offset, y)
        offset += 70

def create_door(x, y):
    new_door = Door(x, y)
    door_group.add(new_door)

def load_tiled_map():
    tiled_map = load_pygame("level1.tmx")

    for layer in tiled_map.visible_layers:
        # print(layer)
        for x, y, gid in layer:
            tile = tiled_map.get_tile_image_by_gid(gid)
            # playertile = tiled_map.get_layer_by_name("Player")
            if tile:
                # print(tiled_map.tilewidth, tiled_map.tileheight)
                # print(tiled_map.get_layer_by_name("Player"))
                # screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))
                new_tile = Block(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                all_group.add(new_tile)

    # print(dir(tiled_map))

# PyGame essentials setup
pygame.init()
screen_width = 1280
screen_height = 720
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

font = pygame.font.SysFont("Helvetica", size=60, bold=True, italic=False)
game_title_text = font.render("Platformer Game", True, ("blue"))
play_text = font.render("Play", True, ("white"))
play_text_rect = play_text.get_rect()

# Create objects like player
player = Player(100, 300)

# Setup collision groups
player_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
player_group.add(player)

load_tiled_map()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game menu play handler
    # if pygame.colliderect(text):
        # print("Clicked play")
        # Load next menu to select level
        # Load the selected level from 1-5 on clicked choice

    # Call the function that handles all our player movement and logic
    # block.update(player_group)
    player.update(all_group, door_group)

    # Refresh the screen
    screen.fill("white")

    # Show background replacing the screen color
    screen.blit(background, (0, 0))
    # load_tiled_map()
    # screen.blit(game_title_text, (screen_width // 3.5, screen_height // 20)) # Figure out how to center the text without number set
    # screen.blit(play_text, (screen_width // 2.4, screen_height // 2))

    # Render player and objects on screen
    all_group.draw(screen)
    # door_group.draw(screen)
    player_group.draw(screen)
    show_debug_menu()

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(fps)

pygame.quit()