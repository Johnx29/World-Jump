# Add other libraries to be used in the game or any python scripts
import pygame
import os
from pytmx.util_pygame import load_pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        self.image = pygame.image.load(os.path.join("assets/player", "p1_stand.png")).convert_alpha()
        
        for image in os.listdir("assets/player/walk"):
            self.images.append(image)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_status = "idle"
        self.animation_index = 0
        self.movement_speed = 4
        self.animation_cooldown = len(self.images)
        self.moving_left = False
        self.moving_right = False
        self.moving = False
        self.jumped = False
        self.velocity = 0
        self.current_direction = ""
    
    def update(self, group):
        movement_x = 0
        movement_y = 0
        # print("Left:", self.rect.left, "Right:", self.rect.right, "Top:", self.rect.top, "Bottom:", self.rect.bottom)
               
        keys = pygame.key.get_pressed()
        # Prevent holding two keys to walk
        if keys[pygame.K_a] and keys[pygame.K_d]:
            return

        if keys[pygame.K_a]:
            movement_x = -self.movement_speed
            self.moving_left = True
            self.animation_index += 1
            self.moving = True
        else:
            self.moving_left = False
            self.moving = False
        if keys[pygame.K_d]:
            movement_x = self.movement_speed
            self.moving_right = True
            self.animation_index += 1
            self.moving = True
        else:
            self.moving_right = False
            self.moving = False

        # Add gravity
        self.velocity += 1
        if self.velocity > 10:
            self.velocity = 10
        movement_y += self.velocity

        # Move player sprite
        self.rect.x += movement_x
        self.rect.y += movement_y

        # Cooldown by preventing animation going to fast
        if self.animation_index > self.animation_cooldown:
            self.animation_index = 0

        player_animation_folder = "assets/player/walk/"

        # Player changed direction
        if self.moving_left == True:
            self.current_direction = "Left"
        elif self.moving_right == True:
            self.current_direction = "Right"

        # Set idle animation relative to direction
        if self.current_direction == "Left" and self.moving == False:
            image = pygame.image.load(os.path.join("assets/player/", "p1_stand.png")).convert_alpha()
            flipped = pygame.transform.flip(image, True, False)
            self.image = flipped
        elif self.current_direction == "Right" and self.moving == False:
            self.image = pygame.image.load(os.path.join("assets/player/", "p1_stand.png")).convert_alpha()

        # Handle player walking animation
        if self.animation_index < len(self.images):
            if self.moving_left == True:
                image = pygame.image.load(os.path.join(player_animation_folder, self.images[self.animation_index])).convert_alpha()
                flipped = pygame.transform.flip(image, True, False)
                self.image = flipped
            elif self.moving_right == True:
                self.image = pygame.image.load(os.path.join(player_animation_folder, self.images[self.animation_index])).convert_alpha()

        # VERTICAL_COLLISION
        collision = pygame.sprite.spritecollide(self, group, False)
        if collision:
            for obj in collision:
                if movement_y > 0:
                    self.rect.bottom = obj.rect.top
                elif movement_y < 0:
                    self.rect.top = obj.rect.bottom

def load_tiled_map():
    tiled_map = load_pygame("level1.tmx")

    for layer in tiled_map.visible_layers:
        # Apply collision to layer objects
        if layer.name == "Objects" or layer.name == "Ground":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_tile = Block(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    block_group.add(new_tile)
        elif layer.name == "Wall":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_tile = Block(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    block_group.add(new_tile)
        # Load everything as image aka foreground
        else:
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    # print(tile, layer.name)
                    new_tile = Block(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    foreground_group.add(new_tile)

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

# PyGame essentials setup
pygame.init()
screen_width = 1260
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60
running = True

# Change caption text and change default icon to custom icon
icon = pygame.image.load(os.path.join("assets/player/", "p1_jump.png"))
pygame.display.set_icon(icon)
pygame.display.set_caption("Platformer Game")

# Variable to store our background image
background = pygame.image.load(os.path.join("assets/", "background.png")).convert_alpha()

# Create objects like player
player = Player(100, 300)

# Setup collision groups
player_group = pygame.sprite.Group(player)
foreground_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()

load_tiled_map()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle player jumping, don't allow hold
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.jumped = True
                player.velocity = -15
        if event.type == pygame.KEYUP:
            # print("Let go")
            if event.key == pygame.K_w:
                player.jumped = False

    # Call the function that handles all our player movement and logic
    player.update(block_group)

    # Refresh the screen
    screen.fill("white")

    # Show background replacing the screen color
    screen.blit(background, (0, 0))

    # Render player and objects on screen
    foreground_group.draw(screen)
    block_group.draw(screen)
    player_group.draw(screen)
    show_debug_menu()

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(fps)

pygame.quit()