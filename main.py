# Platformer game made in PyGame by Johnny Huang (340893478) 
import pygame

# PyGame setup
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

caption = "Platformer Game"
icon = pygame.image.load("assets/walk1.png")

pygame.display.set_caption(caption)
pygame.display.set_icon(icon)

player_sprite = pygame.image.load("assets/walk1.png").convert_alpha()
player_rect = player_sprite.get_rect()

# Configurations
step = 4
gravity = 2

jumped = False

def create_platform(color, width, height, sizeX, sizeY):
    platform = pygame.draw.rect(screen, color, (width, height, sizeX, sizeY))
    return platform

def create_ground(width, height, sizeX, sizeY):
    print("Ground")
    image = pygame.image.load("assets/ground.png").convert_alpha()
    image = pygame.transform.scale(image, (sizeX, sizeY))
    platform = image.get_rect()
    screen.blit(image, (width, height))
    return platform

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        print("Jumped")
        player_rect.y -= step
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        print("Left")
        player_rect.x -= step
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        print("Right")
        player_rect.x += step

    screen.fill("white")

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

    offset = 0
    for i in range(17):
        create_ground(offset, 500, 50, 50)
        offset += 50

    # create_ground(0, 100, 50, 50)
    # create_ground(80, 100, 50, 50)
    # create_ground(160, 100, 50, 50)

    screen.blit(player_sprite, (player_rect.x, player_rect.y))

    # Essential pygame thing helps with rendering our stuff
    pygame.display.flip()

    # Make game run at 60fps
    # clock.tick(60)

pygame.quit()
