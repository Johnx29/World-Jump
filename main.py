# Platformer game made in PyGame by Johnny Huang (340893478) 

# Add other libraries to be used in the game or any external scripts
import pygame

# PyGame setup
pygame.init()
screen_width = 960
screen_height = 540
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
# player_sprite = pygame.image.load("assets/idle.png").convert_alpha()
# player.rect = player_sprite.get_rect()

# Create a variable to store our ground / floor
ground = pygame.image.load("assets/grassMid.png").convert_alpha()
ground_rect = ground.get_rect()

# Setup collision groups
# player_group = pygame.sprite.Group()
# player_group.add(ground_rect)
# print(player_group)

# Configurations
step = 5
gravity = 2

jumped = False
collided = False

# Player class that creates the player with its properties
class setup_player():
    def __init__(self):
        print("Created player object")
        self.sprite = pygame.image.load("assets/idle.png").convert_alpha()
        self.rect = self.sprite.get_rect()
        self.newmask = pygame.mask.from_surface(self.sprite)
        self.mask = self.newmask.to_surface()

class setup_platform():
    def __init__(self):
        print("Created platform object")
        self.sprite = pygame.image.load("assets/grassMid.png").convert_alpha()
        self.rect = self.sprite.get_rect()

class setup_floor():
    def __init__(self):
        print("Created ground object")
        self.sprite = pygame.image.load("assets/grassMid.png").convert_alpha()
        self.rect = self.sprite.get_rect()
        self.newmask = pygame.mask.from_surface(self.sprite)
        self.mask = self.newmask.to_surface()
        self.group = pygame.sprite.Group()

# floor = setup_floor()
player = setup_player()
platform = setup_platform()
# print(player)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        print("Jumped")
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

    # Decrease player gravity allowing us to make them fall
    if not collided:
        player.rect.y += gravity - 1

    # Easy method to create ground maybe?
    for i in range(0, screen_width, 70):
        screen.blit(ground, (i, 200 + screen_height / 2))
        new_ground_mask = pygame.mask.from_surface(ground)
        ground_mask = new_ground_mask.to_surface()

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

    for platforms in platform_group():
        player.mask.overlap(platform)

    # Show player on screen with the mask
    # screen.blit(player.mask, (player.rect.x, player.rect.x))
    screen.blit(player.sprite, (player.rect.x, player.rect.y))
    
    # for i in range(0, 80, 70):
    #     screen.blit(platform.sprite, (i, 300))

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(60)

pygame.quit()