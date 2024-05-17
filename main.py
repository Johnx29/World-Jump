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

def create_text(text, size, color):
    font = pygame.font.Font(os.path.join("assets/fonts/", "KnightWarrior-w16n8.otf"), size)
    new_text = font.render(text, True, (color))
    return new_text

def play_sound_effect(path, file):
    sound = pygame.mixer.Sound(os.path.join(path, file))
    channel = pygame.mixer.Channel(0)
    channel.play(sound, loops=0, maxtime=0)

def show_menu_screen(mouse):
    screen.fill("white")
    screen.blit(background, (0, 0))

    test = create_text("Platformer Game", 60, (50,191,255))
    screen.blit(test, (400, 0))

    button = Button(120, 50, "Play", "green", 520, 200)
    button.collide(mouse, "Play")
    button_group.add(button)

    button2 = Button(120, 50, "Levels", "red", 520, 300)
    button2.collide(mouse, "level-selector")
    button_group.add(button2)

    button_group.draw(screen)
    screen.blit(button.text, (540, 200))
    screen.blit(button2.text, (530, 300))

    pygame.display.flip()

def show_finished_screen(mouse):
    button_group.empty()
    screen.fill("blue")
    finished = create_text(f"Congratulation", 60, "Green")
    screen.blit(finished, (500, 100))

    button = Button(200, 50, "Next Level", "green", 400, 200)
    button.collide(mouse, "next-level")
    button_group.add(button)

    button2 = Button(100, 50, "Quit", "red", 690, 200)
    button2.collide(mouse, "Quit")
    button_group.add(button2)

    button_group.draw(screen)
    screen.blit(button.text, (420, 200))
    screen.blit(button2.text, (700, 200))

    pygame.display.flip()

def draw_level_one():
    button_group.empty()
    # Setup collision groups
    player_group = pygame.sprite.Group(player)
    player.update(block_group, spike_group, coin_group, door_group)
    
    foreground_group.draw(screen)
    block_group.draw(screen)
    spike_group.draw(screen)
    coin_group.draw(screen)
    door_group.draw(screen)
    player_group.draw(screen)
    coin_count = create_text(f"Coin: {player.coin_collected}", 40, "Gold")
    screen.blit(coin_count, (0, 0))

def draw_level_two():
    button_group.empty()
    foreground_group.draw(screen)
    block_group.draw(screen)
    player_group.draw(screen)
    door_group.draw(screen)

def show_level_selector():
    screen.fill("blue")
    button_group.empty()

    test = create_text("Level Selector", 60, (50,191,255))
    screen.blit(test, (400, 0))

    button = Button(100, 50, "01", "white", 300, 200)
    button.collide(mouse, "Level1")
    button_group.add(button)

    button2 = Button(100, 50, "02", "white", 700, 200)
    button2.collide(mouse, "Level2")
    button_group.add(button2)

    button_group.draw(screen)
    screen.blit(button.text, (300, 200))
    screen.blit(button2.text, (700, 200))

class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, text, color, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = pygame.font.Font(os.path.join("assets/fonts/", "KnightWarrior-w16n8.otf"), 40)
        self.text = self.font.render(text, False, color)
        self.text_rect = self.image.get_rect()
    
    def collide(self, mouse, status=""):
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_button_down = mouse_pressed[0]

        levels = [
        "level1",
        "level2"
        ]
        # print(f"Level: {levels[0]}.tmx")

        if mouse_button_down and self.rect.collidepoint(mouse) and status == "Quit":
            running = False
            pygame.quit()
        elif mouse_button_down and self.rect.collidepoint(mouse) and status == "Play":
            print("Clicked play button!")
            player.game_status = "game"
            load_tiled_map(f"{levels[0]}.tmx")
        elif mouse_button_down and self.rect.collidepoint(mouse) and status == "next-level":
            print("Clicked next level button")
            load_tiled_map(f"{levels[1]}.tmx")
            player.game_status = levels[1]
        elif mouse_button_down and self.rect.collidepoint(mouse) and status == "level-selector":
            print("Clicked level selector button!")
            player.game_status = "level-selector"
        # if player.game_status == "level-selector":
            # if mouse_button_down and self.rect.collidepoint(mouse):
                # print("Selected:", status)
                # load_tiled_map(f"{status}.tmx")
            # if mouse_button_down and self.rect.collidepoint(mouse) and status == "game":
                # print("Selected Level 1")
                # player.game_status = "game"
                # player.level_selected = "Level1"
                # load_tiled_map(levels[0])
                # player_group.draw(screen)

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
        self.coin_collected = 0
        self.completed_level = False
        self.game_status = "starting-screen"
        self.level_selected = ""
    
    def update(self, group, group2, group3, group4):
        movement_x = 0
        movement_y = 0
               
        keys = pygame.key.get_pressed()
        # DON'T ALLOW PEOPLE TO HOLD 2 KEYS TO WALK
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

        # ADD GRAVITY
        self.velocity += 1
        if self.velocity > 10:
            self.velocity = 10
        movement_y += self.velocity

        # SET ANIMATION_INDEX TO ZERO WHEN IT GOES THROUGH THEM ALL, TO KEEP WALKING
        if self.animation_index > self.animation_cooldown:
            self.animation_index = 0

        player_animation_folder = "assets/player/walk/"
        player_folder = "assets/player/"

        # CHECK IF PLAYER CHANGED DIRECTION
        if self.moving_left == True:
            self.current_direction = "Left"
        elif self.moving_right == True:
            self.current_direction = "Right"

        # SET IDLE ANIMATION RELATIVE TO DIRECTION
        if self.current_direction == "Left" and self.moving == False:
            image = pygame.image.load(os.path.join(player_folder, "p1_stand.png")).convert_alpha()
            flipped = pygame.transform.flip(image, True, False)
            self.image = flipped
        elif self.current_direction == "Right" and self.moving == False:
            self.image = pygame.image.load(os.path.join(player_folder, "p1_stand.png")).convert_alpha()

        # SET JUMP ANIMATION RELATIVE TO DIRECTION
        if self.jump_count > 0 and self.current_direction == "Right":
            self.image = pygame.image.load(os.path.join(player_folder, "p1_jump.png")).convert_alpha()
        elif self.jump_count > 0 and self.current_direction == "Left":
            image = pygame.image.load(os.path.join(player_folder, "p1_jump.png")).convert_alpha()
            flipped = pygame.transform.flip(image, True, False)
            self.image = flipped

        # HANDLE PLAYER WALKING ANIMATION
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
            self.coin_collected += 1

        # DOOR_COLLISION
        door_collision = pygame.sprite.spritecollide(self, group4, False)
        if door_collision:
            if not self.game_status == "completed":
                self.game_status = "completed"

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
player_group = pygame.sprite.Group()
foreground_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()

# load_tiled_map("level1.tmx")

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call the function that handles all our player movement and logic
    # player.update(block_group, spike_group, coin_group, door_group)

    # Refresh the screen
    screen.fill("white")

    # Show background replacing the screen color
    screen.blit(background, (0, 0))

    # Update / Refresh GUI state aka show game menu or show level completed screen
    mouse = pygame.mouse.get_pos()
    # Show start screen aka screen with play button
    if player.game_status == "starting-screen":
        show_menu_screen(mouse)
    # Player clicked play button instead of level button, start game
    elif player.game_status == "game":
        print("Reached")
        draw_level_one()
    # Player completed game show completed screen
    elif player.game_status == "completed":
        show_finished_screen(mouse)
        # if player.level_selected
    elif player.game_status == "level-selector":
        show_level_selector()
    # elif player.game_status == "game" and player.level_selected == "Level1":
    #     draw_level_one()
    # elif player.game_status == "game" and player.level_selected == "Level2":
    #     draw_level_two()

    print("Game: ", player.game_status)
    print("Level: ", player.level_selected)

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(fps)

pygame.quit()