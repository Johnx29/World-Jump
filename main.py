# Add other libraries to be used in the game or any python scripts
import pygame
import os
from pytmx.util_pygame import load_pygame

def load_tiled_map(mapfile):
    tiled_map = load_pygame(mapfile)

    for layer in tiled_map.visible_layers:
        # Apply collision to layer objects
        if layer.name == "Objects" or layer.name == "Ground" or layer.name == "Wall":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_tile = Block(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    block_group.add(new_tile)
        elif layer.name == "Spike":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_spike = Spike(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    spike_group.add(new_spike)
        elif layer.name == "Coin":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_coin = Coin(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    coin_group.add(new_coin)
        elif layer.name == "Door":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_door = Door(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    door_group.add(new_door)
        # Load everything as image aka foreground
        else:
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_tile = Block(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    foreground_group.add(new_tile)

def create_text(text):
    font = pygame.font.SysFont("Arial", 30)
    new_text = font.render(text, True, ("gold"))
    return new_text

def play_sound_effect(path, file):
    sound = pygame.mixer.Sound(os.path.join(path, file))
    channel = pygame.mixer.Channel(0)
    channel.play(sound, loops=0, maxtime=0)

def show_finished_screen():
    print("Finished screen showed")

class Door(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.animation_index = 0
        self.movement_speed = 4
        self.animation_cooldown = len(self.images)
        self.moving_left = False
        self.moving_right = False
        self.moving = False
        self.velocity = 0
        self.current_direction = ""
        self.jump_count = 0
    
    def update(self, group, group2, group3, group4):
        movement_x = 0
        movement_y = 0
               
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
        if keys[pygame.K_w] and self.jump_count < 1:
            self.velocity = -15
            self.jump_count = 1

        # Add gravity
        self.velocity += 1
        if self.velocity > 10:
            self.velocity = 10
        movement_y += self.velocity

        # Cooldown by preventing animation going to fast
        if self.animation_index > self.animation_cooldown:
            self.animation_index = 0

        player_animation_folder = "assets/player/walk/"
        player_folder = "assets/player/"

        # Player changed direction
        if self.moving_left == True:
            self.current_direction = "Left"
        elif self.moving_right == True:
            self.current_direction = "Right"

        # Set idle animation relative to direction
        if self.current_direction == "Left" and self.moving == False:
            image = pygame.image.load(os.path.join(player_folder, "p1_stand.png")).convert_alpha()
            flipped = pygame.transform.flip(image, True, False)
            self.image = flipped
        elif self.current_direction == "Right" and self.moving == False:
            self.image = pygame.image.load(os.path.join(player_folder, "p1_stand.png")).convert_alpha()

        if self.jump_count > 0 and self.current_direction == "Right":
            self.image = pygame.image.load(os.path.join(player_folder, "p1_jump.png")).convert_alpha()
        elif self.jump_count > 0 and self.current_direction == "Left":
            image = pygame.image.load(os.path.join(player_folder, "p1_jump.png")).convert_alpha()
            flipped = pygame.transform.flip(image, True, False)
            self.image = flipped

        # Handle player walking animation
        if self.animation_index < len(self.images):
            if self.moving_left == True:
                image = pygame.image.load(os.path.join(player_animation_folder, self.images[self.animation_index])).convert_alpha()
                flipped = pygame.transform.flip(image, True, False)
                self.image = flipped
            elif self.moving_right == True:
                self.image = pygame.image.load(os.path.join(player_animation_folder, self.images[self.animation_index])).convert_alpha()

        # VERTICAL_COLLISION
        # Move player rect by y-axis a bit to ensure it is on vertical collision
        self.rect.y += movement_y
        collision = pygame.sprite.spritecollide(self, group, False)
        if collision:
            if movement_y > 0:
                self.rect.bottom = collision[0].rect.top
                movement_y = 0
                self.jump_count = 0
            elif movement_y < 0:
                self.rect.top = collision[0].rect.bottom
                movement_y = 0

        # HORIZONTAL_COLLISION
        # Move player rect by x-axis a bit to ensure it is on horizontal collision        
        self.rect.x += movement_x
        collision2 = pygame.sprite.spritecollide(self, group, False)
        if collision2:
            if movement_x > 0:
                self.rect.right = collision2[0].rect.left
                movement_x = 0
            elif movement_x < 0:
                self.rect.left = collision2[0].rect.right
                movement_x = 0

        # SPIKE_COLLISION
        spike_collision = pygame.sprite.spritecollide(self, group2, False)
        if spike_collision:
            print("Hit")
            self.rect.x = 100

        # COIN_COLLISION
        # DO KILL ARGUMENT IN EFFECT (Makes our coins disappear on collided)
        coin_collision = pygame.sprite.spritecollide(self, group3, True)
        if coin_collision:
            print("Coin Collected")

        # DOOR_COLLISION
        door_collision = pygame.sprite.spritecollide(self, group4, False)
        if door_collision:
            print("door")

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
spike_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

load_tiled_map("level1.tmx")

coin_count = create_text(f"Coin: {0}")

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call the function that handles all our player movement and logic
    player.update(block_group, spike_group, coin_group, door_group)

    # Refresh the screen
    screen.fill("white")

    # Show background replacing the screen color
    screen.blit(background, (0, 0))

    # Render player and objects on screen
    foreground_group.draw(screen)
    block_group.draw(screen)
    spike_group.draw(screen)
    coin_group.draw(screen)
    door_group.draw(screen)
    player_group.draw(screen)

    screen.blit(coin_count, (0, 0))

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(fps)

pygame.quit()