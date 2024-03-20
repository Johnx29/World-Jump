# Main Menu that is ran when you start the game launches, basically the starting menu

# Add other libraries or external scripts
import pygame

# PyGame setup
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

def create_text(name):
    font = pygame.font.SysFont("Arial", 64)
    text = font.render(name, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 2)
    return text, text_rect

def create_button():
    surface = pygame.Surface((50, 50))
    button = pygame.draw.rect(surface, "Red", (0, 250, 250, 0))
    return button, surface

text, text_rect = create_text("Platformer Game")
# button = create_button()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((51, 153, 255))

    screen.blit(text, (text_rect))

    surface = pygame.Surface((50, 50))
    button = pygame.draw.rect(screen, "green", (0, 200, 200, 200))
    text2, text_rect = create_text("Play")
    screen.blit(text2, (0, 200, 200, 200))

    screen.blit(surface, (0, 200, 0, 0))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()