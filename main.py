# Platformer game made in PyGame by Johnny Huang (340893478) 

# Import other modules or scripts
import pygame
# import Spritesheet

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

# Get our background
background = pygame.image.load("assets/foreground.png").convert_alpha()

# Get our player sprite
player_sprite = pygame.image.load("assets/idle.png").convert_alpha()
player_rect = player_sprite.get_rect()


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

ground, ground_rect = create_ground(80, 80)

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

    player_rect.y += gravity - 1

    # Borders
    # platform = create_platform("brown", 0, 550, width, 50)
    # platform2 = create_platform("brown", 0, 10, 50, width)
    # platform3 = create_platform("brown", 750, 10, 50, width)
    # platform4 = create_platform("brown", 0, 0, width, 50)

    # Blocks
    # block = create_platform("green", 50, 500, 200, 50)
    # block2 = create_platform("green", 300, 400, 200, 50)

    # block3 = create_platform("green", 50, 50, 50, 50)

    # door = create_platform("blue", 700, 200, 50, 100)

    # Easy method to create ground maybe?
    offset = 0
    for i in range(16):
        # Never create objects in the game loop instead store them then blit them inside the loop
        screen.blit(ground, (i + offset, screen_height - 80))
        offset += 50
    
    collision = pygame.Rect.colliderect(player_rect, ground_rect)
    # print(collision)


    screen.blit(player_sprite, (player_rect.x + 300, player_rect.y + 400))

    # Essential pygame thing helps with rendering our stuff
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(60)

pygame.quit()
