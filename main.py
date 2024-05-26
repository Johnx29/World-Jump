# Add other libraries to be used in the game or any python scripts
import pygame
import os
from pytmx.util_pygame import load_pygame

# PyGame essentials setup
pygame.init()
screen_width = 1260
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60
running = True

# Change caption text and change default icon to custom icon
icon = pygame.image.load(os.path.join("assets/player/", "p1_jump.png")).convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("World Jump")

# Variable to store our background image
background = pygame.image.load(os.path.join("assets/", "background.png")).convert_alpha()

# Fonts
title_font = pygame.font.Font(os.path.join("assets/fonts/", "LuckiestGuy-Regular.ttf"), 60)
button_font = pygame.font.Font(os.path.join("assets/fonts/", "LuckiestGuy-Regular.ttf"), 40)

# Sound Files
jump_sound = "jump.wav"
spike_trap_sound = "spiketrap.mp3"
victory_sound = "sboe.wav"
button_click_sound = "click.mp3"
key_collect_sound = "key2 pickup.ogg"

# Music Files
starting_music = "Intro Theme.mp3"
game_music = "music.mp3"

# Setup collision groups
key_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# WE NEED THIS BECAUSE OTHER CLASSES CAN'T INTERACT WITH LOCAL VARIABLES BUT WITH CLASSES LIKE THIS THEY CAN
class Game:
    def __init__(self):
        self.game_status = "starting-screen"
        self.level_selected = ""
        self.current_level_index = 1

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
        self.text = button_font.render(text, True, color)
        self.text_rect = self.image.get_rect()
        self.current_level_index = 1
    
    def collide(self, buttonObj, mouse, status="", level_button=False):
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_button_down = mouse_pressed[0]

        levels = {
            1 : {
                "map" : "level1",
                "starting-x" : 142,
                "starting-y" : 200
                },

            2 : {
                "map" : "level2",
                "starting-x" : 100,
                "starting-y" : 100
                },
            3 : {
                "map" : "level3",
                "starting-x" : 100,
                "starting-y" : 100
                }
        }

        # Button Hover Effect when mouse hovers over a button show it being interacted 
        if self.rect.collidepoint(mouse) and buttonObj:
            buttonObj.image.fill((100, 100, 100))

        # These run once without repeating in the game loop
        # Player clicked play button
        if mouse_button_down and self.rect.collidepoint(mouse) and status == "Play":     
            game.current_level_index = 1

            # Empty collision groups for loading next level
            block_group.empty()
            door_group.empty()
            button_group.empty()
            key_group.empty()
            spike_group.empty()
            
            # Play button click sound and stop current music and load new music
            play_sound_effect(button_click_sound)
            pygame.mixer.music.unload()
            play_music(game_music)

            # Spawn the player at each level starting pos
            player_spawn_x = levels[game.current_level_index]["starting-x"]
            player_spawn_y = levels[game.current_level_index]["starting-y"]
            player.respawn(player_spawn_x, player_spawn_y)

            # Handle loading and tell main loop to start game
            game.game_status = "game"
            level_selected = f"{levels[game.current_level_index]["map"]}"
            game.level_selected = level_selected
            load_tiled_map(f"{level_selected}.tmx")

        # Player selects a level from menu
        elif mouse_button_down and self.rect.collidepoint(mouse) and status == "level-selector":
            play_sound_effect(button_click_sound)
            game.game_status = "level-selector"      

        # Level selector hander, handle clicking the seperate levels, level_button arg used to make this work
        elif mouse_button_down and self.rect.collidepoint(mouse) and level_button:
            game.current_level_index = status

            # Empty collision groups for loading next level
            block_group.empty()
            door_group.empty()
            button_group.empty()
            key_group.empty()
            spike_group.empty()
            
            # Play button click sound and stop current music and load new music
            play_sound_effect(button_click_sound)
            pygame.mixer.music.unload()
            play_music(game_music)
            
            # Spawn the player at each level starting pos
            player_spawn_x = levels[game.current_level_index]["starting-x"]
            player_spawn_y = levels[game.current_level_index]["starting-y"]
            player.respawn(player_spawn_x, player_spawn_y)

            # Handle loading and tell main loop to start game
            game.game_status = "game"
            level_selected = f"{levels[game.current_level_index]["map"]}"
            game.level_selected = level_selected
            load_tiled_map(f"{level_selected}.tmx")

        # Player completed level and clicks next button
        elif mouse_button_down and self.rect.collidepoint(mouse) and status == "next-level":
            # Increment level to show we want next level loaded
            game.current_level_index += 1
            
            # Empty collision groups for loading next level
            block_group.empty()
            door_group.empty()
            button_group.empty()
            key_group.empty()
            spike_group.empty()

            # Play button click sound and stop current music and load new music
            play_sound_effect(button_click_sound)
            pygame.mixer.music.unload()
            play_music(game_music)

            # Spawn the player at starting pos
            player_spawn_x = levels[game.current_level_index]["starting-x"]
            player_spawn_y = levels[game.current_level_index]["starting-y"]
            player.respawn(player_spawn_x, player_spawn_y)

            # Handle loading and tell main loop to start game
            game.game_status = "game"
            level_selected = f"{levels[game.current_level_index]["map"]}"
            game.level_selected = level_selected
            load_tiled_map(f"{level_selected}.tmx")

        elif mouse_button_down and self.rect.collidepoint(mouse) and status == "Back":
            button_group.empty()
            game.game_status = "starting-screen"
            game.level_selected = ""
            
            # Play button click sound and stop current music and load new music
            play_sound_effect(button_click_sound)
            pygame.mixer.music.unload()
            play_music(starting_music)

class Key(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(pygame.sprite.Sprite):
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
        self.animation_cooldown = 11
        self.moving_left = False
        self.moving_right = False
        self.moving = False
        self.velocity = 0
        self.current_direction = ""
        self.jumped = False
        self.has_key = False
        self.died = False
        self.completed_level = False

    def respawn(self, x, y):
        self.images = []
        self.image = pygame.image.load(os.path.join("assets/player", "p1_stand.png")).convert_alpha()
        
        for image in os.listdir("assets/player/walk"):
            self.images.append(image)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_index = 0
        self.movement_speed = 4
        self.animation_cooldown = 11
        self.moving_left = False
        self.moving_right = False
        self.moving = False
        self.velocity = 0
        self.current_direction = ""
        self.jumped = False
        self.has_key = False
        self.died = False
        self.completed_level = False
    
    def update(self):
        movement_x = 0
        movement_y = 0
               
        keys = pygame.key.get_pressed()
        # DON'T ALLOW PEOPLE TO HOLD 2 KEYS TO WALK
        if keys[pygame.K_a] and keys[pygame.K_d]:
            return

        # Keys for WASD
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement_x = -self.movement_speed
            self.moving_left = True
            self.animation_index += 1
            self.moving = True
        else:
            self.moving_left = False
            self.moving = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement_x = self.movement_speed
            self.moving_right = True
            self.animation_index += 1
            self.moving = True
        else:
            self.moving_right = False
            self.moving = False
        if keys[pygame.K_w] and self.jumped == False:
            self.velocity = -15
            self.jumped = True
            play_sound_effect(jump_sound)
        elif keys[pygame.K_UP] and self.jumped == False:
            self.velocity = -15
            self.jumped = True
            play_sound_effect(jump_sound)

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
        if self.jumped and self.current_direction == "Right":
            self.image = pygame.image.load(os.path.join(player_folder, "p1_jump.png")).convert_alpha()
        elif self.jumped and self.current_direction == "Left":
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
            # Show them jumping still even if they are currently moving
            if self.jumped == True and self.current_direction == "Right":
                self.image = pygame.image.load(os.path.join(player_folder, "p1_jump.png")).convert_alpha()
            elif self.jumped and self.current_direction == "Left":
                image = pygame.image.load(os.path.join(player_folder, "p1_jump.png")).convert_alpha()
                flipped = pygame.transform.flip(image, True, False)
                self.image = flipped

        # COLLISION DETECTIONS START HERE

        # VERTICAL_COLLISION
        # Move player rect by y-axis a bit to ensure it is on vertical collision
        self.rect.y += movement_y
        vertical_collision = pygame.sprite.spritecollide(self, block_group, False)
        if vertical_collision:
            if movement_y > 0:
                self.rect.bottom = vertical_collision[0].rect.top
                movement_y = 0
                self.jumped = False
            elif movement_y < 0:
                self.rect.top = vertical_collision[0].rect.bottom
                movement_y = 0

        # HORIZONTAL_COLLISION
        # Move player rect by x-axis a bit to ensure it is on horizontal collision        
        self.rect.x += movement_x
        horizontal_collision = pygame.sprite.spritecollide(self, block_group, False)
        if horizontal_collision:
            if movement_x > 0:
                self.rect.right = horizontal_collision[0].rect.left
                movement_x = 0
            elif movement_x < 0:
                self.rect.left = horizontal_collision[0].rect.right
                movement_x = 0

        # SPIKE_COLLISION
        spike_collision = pygame.sprite.spritecollide(self, spike_group, False)
        if spike_collision:
            play_sound_effect(spike_trap_sound)
            self.died = True
            player.respawn(70, 100)            

        # KEY COLLISION
        # DO KILL ARGUMENT IN EFFECT (Makes our KEY disappear on collided)
        key_collision = pygame.sprite.spritecollide(self, key_group, True)
        if key_collision:
            if not self.has_key:
                play_sound_effect(key_collect_sound)
                self.has_key = True

        # DOOR_COLLISION
        door_collision = pygame.sprite.spritecollide(self, door_group, False)
        if door_collision:
            if self.has_key:
                pygame.mixer.music.unload()    
                play_sound_effect(victory_sound)
                game.game_status = "completed"
                self.has_key = False

def load_tiled_map(mapfile):
    tiled_map = load_pygame(mapfile)
    

    for layer in tiled_map.visible_layers:
        # Apply collision to layer objects
        if layer.name == "Ground" or layer.name == "Wall":
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
        elif layer.name == "Door":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_door = Door(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    door_group.add(new_door)
        elif layer.name == "Key":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    new_key = Key(tile, x * tiled_map.tilewidth, y * tiled_map.tileheight)
                    key_group.add(new_key)

def play_sound_effect(file):
    sound = pygame.mixer.Sound(os.path.join("assets/audio/", file))
    channel = pygame.mixer.Channel(0)
    channel.set_volume(0.4)
    channel.play(sound, loops=0, maxtime=0)

def play_music(file):
    pygame.mixer.music.load(os.path.join("assets/music/", file))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    pygame.event.wait()

def show_menu_screen(mouse):
    button_group.empty()

    title = title_font.render("World Jump", True, (50,191,255))
    title_rect = title.get_rect()
    title_rect.center = (600, 50)

    play_button = Button(150, 50, "Play", "green", 520, 200)
    play_button.rect.center = (600, 200)
    play_button.collide(play_button, mouse, "Play")
    button_group.add(play_button)

    level_button = Button(150, 50, "Levels", "red", 520, 200)
    level_button.rect.center = (600, 400)
    level_button.collide(level_button, mouse, "level-selector")
    button_group.add(level_button)

    screen.blit(title, (title_rect))
    button_group.draw(screen)
    screen.blit(play_button.text, (play_button.rect.x+30, play_button.rect.y+10))
    screen.blit(level_button.text, (level_button.rect.x+10, level_button.rect.y+10))

    pygame.display.flip()

def show_finished_screen(mouse):
    # Refresh previous buttons to load new buttons
    button_group.empty()
    
    level_text = f"Completed: {game.level_selected}"
    finished = title_font.render(f"Completed: {game.level_selected}", True, (50,191,255))
    finished_rect = finished.get_rect()
    finished_rect.center = (600, 100)

    next_button = Button(100, 50, "Next", "green", 400, 200)
    next_button.rect.center = (500, 200)
    
    if game.current_level_index != 3:
        next_button.collide(next_button, mouse, "next-level")
        button_group.add(next_button)

    back_button = Button(100, 50, "Back", "red", 690, 100)
    back_button.rect.center = (700, 200)
    back_button.collide(back_button, mouse, "Back")
    button_group.add(back_button)

    button_group.draw(screen)
    screen.blit(finished, (finished_rect))

    if game.current_level_index != 3:
        screen.blit(next_button.text, (next_button.rect.x+2, next_button.rect.y+10))
    
    screen.blit(back_button.text, (back_button.rect.x+2, back_button.rect.y+10))

    pygame.display.flip()

def draw_level():
    # Refresh previous buttons to load new buttons
    button_group.empty()

    block_group.draw(screen)
    spike_group.draw(screen)
    door_group.draw(screen)
    key_group.draw(screen)
    player_group.draw(screen)

def show_level_selector():
    # Refresh previous buttons to load new buttons
    button_group.empty()

    # Refresh screen
    screen.fill("white")
    screen.blit(background, (0, 0))

    title = title_font.render("Level Selector", True, (50,191,255))
    title_rect = title.get_rect()
    title_rect.center = (600, 50)

    back_button = Button(100, 50, "Back", "red", 690, 100)
    back_button.rect.center = (100, 650)
    back_button.collide(back_button, mouse, "Back")
    button_group.add(back_button)

    level1_button = Button(100, 50, "01", "white", 300, 200)
    level1_button.rect.center = (400, 200)
    level1_button.collide(level1_button, mouse, 1, True)
    button_group.add(level1_button)

    level2_button = Button(100, 50, "02", "white", 700, 200)
    level2_button.rect.center = (800, 200)
    level2_button.collide(level2_button, mouse, 2, True)
    button_group.add(level2_button)

    level3_button = Button(100, 50, "03", "white", 700, 200)
    level3_button.rect.center = (400, 300)
    level3_button.collide(level3_button, mouse, 3, True)
    button_group.add(level3_button)

    button_group.draw(screen)
    screen.blit(title, (title_rect))
    screen.blit(level1_button.text, (level1_button.rect.x+20, level1_button.rect.y+10))
    screen.blit(level2_button.text, (level2_button.rect.x+20, level2_button.rect.y+10))
    screen.blit(level3_button.text, (level3_button.rect.x+20, level3_button.rect.y+10))
    screen.blit(back_button.text, (back_button.rect.x, back_button.rect.y+10))

# Create the basics

player = Player(142, 300)
game = Game()
play_music(starting_music)
player_group.add(player)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Refresh screen
    screen.fill("white")
    screen.blit(background, (0, 0))

    player.update()

    # Update / Refresh GUI state aka show game menu or show level completed screen
    mouse = pygame.mouse.get_pos()

    # Show start screen aka screen with play button
    if game.game_status == "starting-screen":
        show_menu_screen(mouse)
    elif game.game_status == "completed":
        show_finished_screen(mouse)

    # Figure out a way to cut down on this level1-level2 chain make it only follow the current index of level
    elif game.level_selected == "level1" or game.level_selected == "level2" or game.level_selected == "level3":
        draw_level()
        if player.has_key:
            key = pygame.image.load(os.path.join("assets/hud", "hud_keyYellow.png")).convert_alpha()
            screen.blit(key, (0, 0))
        else:
            key = pygame.image.load(os.path.join("assets/hud", "hud_keyYellow_disabled.png")).convert_alpha()
            screen.blit(key, (0, 0))

    elif game.game_status == "level-selector":
        show_level_selector()

    # CRITICAL DEBUGGING THIS HELPS SO MUCH
    # print("Currently On: ", game.game_status)
    # print("Level: ", game.level_selected)

    # Crucial pygame thing helps with rendering our stuff on screen
    pygame.display.flip()

    # Make game run at 60fps
    clock.tick(fps)

pygame.quit()