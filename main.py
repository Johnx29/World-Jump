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
        # self.image = pygame.image.load("assets/player/p1_stand.png").convert_alpha()
        self.image = pygame.image.load(os.path.join("assets/player", "p1_stand.png")).convert_alpha()
        
        for image in os.listdir("assets/player/walk"):
            self.images.append(image)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_status = "idle"
        self.animation_index = 0
        self.movement_speed = 5
        self.animation_cooldown = len(self.images)
        self.moving_left = False
        self.moving_right = False
        self.moving = False
        self.jumped = False
        self.velocity = 0
        self.current_direction = ""

    def border(self):
        # Establish a border for player left and right at x axis
        if self.rect.left < 10:
            self.rect.left = 10
        # if self.rect.right > screen_height // 2:
            # self.rect.right = screen_height // 2

        # Establish a border for player both up and down at y axis
        if self.rect.top < -0:
            self.rect.top = -0
        if self.rect.bottom > screen_width // 2:
            self.rect.bottom = screen_width // 2
    
    def update(self, group):
        movement_x = 0
        movement_y = 0
        # print("Left:", self.rect.left, "Right:", self.rect.right, "Top:", self.rect.top, "Bottom:", self.rect.bottom)
               
        keys = pygame.key.get_pressed()
        # Prevent holding two keys to walk
        if keys[pygame.K_a] and keys[pygame.K_d]:
            return

        if keys[pygame.K_a]:
            movement_x = -2
            self.moving_left = True
            self.animation_index += 1
            self.moving = True
        else:
            self.moving_left = False
            self.moving = False
        if keys[pygame.K_d]:
            movement_x = 2
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

        self.border()

        # Cooldown by preventing animation going to fast
        if self.animation_index > self.animation_cooldown:
            self.animation_index = 0

        player_animation_folder = "assets/player/walk/"

        # if self.jumped == True:
            # self.image = pygame.image.load(os.path.join("assets/player/", "p1_jump.png"))

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

        # Efficient way of handling player collision by checking rect collision --> mask collision
        player_collided = pygame.sprite.spritecollide(self, group, False)
        if player_collided:
            player_mask_collided = pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask)
            if player_mask_collided:
                # print("Hit", player_mask_collided)
                for obj in player_mask_collided:
                    if obj.rect.top:
                        self.rect.bottom - 2
                        self.rect.bottom = obj.rect.top
                        print("Oh god")

def load_tiled_map():
    tiled_map = load_pygame("level1.tmx")

    for layer in tiled_map.visible_layers:
        # print(layer)
        # Apply collision to layer objects
        if layer.name == "Objects":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
    #             # print(tiled_map.tilewidth, tiled_map.tileheight)
    #             # print(tiled_map.get_layer_by_name("Player"))
    #             # screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))
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

        # for x, y, gid in layer:
        #     tile = tiled_map.get_tile_image_by_gid(gid)
        #     if tile:
    #             # print(tiled_map.tilewidth, tiled_map.tileheight)
    #             # print(tiled_map.get_layer_by_name("Player"))
    #             # screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))
                # new_tile = Block(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                # block_group.add(new_tile)
    # # print(dir(tiled_map))

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
screen_width = 1280
screen_height = 720
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

font = pygame.font.SysFont("Helvetica", size=60, bold=True, italic=False)
game_title_text = font.render("Platformer Game", True, ("blue"))
play_text = font.render("Play", True, ("white"))
play_text_rect = play_text.get_rect()

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
            if event.key == pygame.K_w:
                player.jumped = False

    # Game menu play handler
    # if pygame.colliderect(text):
        # print("Clicked play")
        # Load next menu to select level
        # Load the selected level from 1-5 on clicked choice

    # Call the function that handles all our player movement and logic
    # block.update(player_group)
    player.update(block_group)

    # Refresh the screen
    screen.fill("white")

    # Show background replacing the screen color
    screen.blit(background, (0, 0))
    # load_tiled_map()
    # screen.blit(game_title_text, (screen_width // 3.5, screen_height // 20)) # Figure out how to center the text without number set
    # screen.blit(play_text, (screen_width // 2.4, screen_height // 2))

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