import pygame

# PyGame setup
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

player_sprite = pygame.image.load("Platformer Game/assets/walk1.png")
# player.x = screen.get_width() / 2
# player.y = screen.get_width() / 2
player_rect = player_sprite.get_rect()

background = pygame.image.load("Platformer Game/assets/vaporwave-retro-art.jpg")

# obstacle = pygame.draw.rect(screen, "yellow", (350, 350, width, height))
# floor_sprite = pygame.image.load("")

# Configurations
step = 4

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        print("Up")
        player_rect.y -= step
    if keys[pygame.K_s]:
        print("Down")
        player_rect.y += step
    if keys[pygame.K_a]:
        print("Left")
        player_rect.x -= step
    if keys[pygame.K_d]:
        print("Right")
        player_rect.x += step

    # screen.fill("green")

    # print(player.y)
    print(player_rect)

    player_rect.y += 0.5

    screen.blit(background, (0, 0))

    obstacle = pygame.draw.rect(screen, "yellow", (0, 500, width, height))

    screen.blit(player_sprite, (player_rect.x, player_rect.y))

    # Essential pygame thing
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
