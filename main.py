# Platformer game made in PyGame by Johnny Huang (340893478) 

# Add other libraries to be used in the game or any external scripts
import pygame
from pytmx.util_pygame import load_pygame

# PyGame setup
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Change caption text and change default icon to custom icon
caption = "Platformer Game"
icon = pygame.image.load("assets/idle.png")
pygame.display.set_caption(caption)
pygame.display.set_icon(icon)

# Create a variable to store our background
background = pygame.image.load("assets/background.png").convert_alpha()

# Create a variable to store our player sprite
player_sprite = pygame.image.load("assets/idle.png").convert_alpha()
player_rect = player_sprite.get_rect()

tmxdata = load_pygame("map.tmx")
# print(dir(tmxdata))
print(tmxdata.layers)

sprite_group = pygame.sprite.Group()

# for layer in tmxdata.layers:
#     # if hasattr("layer", "data"):
#     print(layer)
#     for x, y, surf in layer.tiles():
#         print(x, y, surf)
#         floor = pygame.image.load("assets/ground.jpg")
#         floor_rect = floor.get_rect()
#         sprite_group.add(floor)


for i in range(20):
    floor = pygame.sprite.Sprite()
    floor_image = pygame.image.load("assets/ground.jpg")
    floor.image = floor_image
    floor_rect = floor_image.get_rect()
    sprite_group.add(floor)

# for item in tmxdata.name:
    # print(item)


# Configurations
step = 5
gravity = 2

jumped = False


def create_platform(color, width, height, sizeX, sizeY):
    '''Used for debugging purposes when I have no assets

    Arguments: 
        Color : Color value
        width : int
        height : int
        sizeX : int
        sizeY : int

    Returns:
        the platform which is a rect
    '''
    platform = pygame.draw.rect(screen, color, (width, height, sizeX, sizeY))
    return platform

def create_ground(sizeX, sizeY):
    '''Easy method to create the ground

    Arguments:
        sizeX : Integer
        sizeY : Integer

    Returns:
        The image which is surface and ground that is rect
    '''
    print("Ground")
    image = pygame.image.load("assets/ground.jpg").convert_alpha()
    image = pygame.transform.scale(image, (sizeX, sizeY))
    ground = image.get_rect()
    return image, ground

def create_button():
    button = pygame.draw.Rect()
    return button

ground, ground_rect = create_ground(screen_width, 50)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        print(player_rect.y)
        if player_rect.y >= 0 and jumped == False:
            print("Jumped", jumped)
            jumped = True
            player_sprite = pygame.image.load("assets/jump.png").convert_alpha()
            player_rect.y -= step
        else:
            jumped = False
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        print("Left")
        player_sprite = pygame.image.load("assets/idle.png").convert_alpha()
        player_rect.x -= step
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        print("Right")
        player_sprite = pygame.image.load("assets/idle.png").convert_alpha()
        player_rect.x += step

    screen.fill("white")

    screen.blit(background, (0, 0))

    if player_rect.y >= 150:
        player_rect.y = player_rect.y
        player_sprite = pygame.image.load("assets/idle.png").convert_alpha()
    else:
        player_rect.y += gravity - 1

    # Easy method to create ground maybe?
    # offset = 0
    # for i in range(16):
        # Never create objects in the game loop instead store them, then blit them inside the loop
        # screen.blit(ground, (i + offset, screen_height - 80))
        # offset += 50

    screen.blit(ground, (0, 250 + screen_height / 2, 0, 0))
    
    # Add all the obstacles to a group then loop through the group to check for collision
    collision = pygame.Rect.colliderect(player_rect, ground_rect)
    # print(collision)


    screen.blit(player_sprite, (player_rect.x + screen_width / 2, player_rect.y + screen_height / 2))

    sprite_group.draw(screen)

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(60)

pygame.quit()
