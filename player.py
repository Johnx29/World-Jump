import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        self.image = pygame.image.load("assets/player/p1_stand.png").convert_alpha()
        
        for image in os.listdir("assets/player/walk"):
            self.images.append(image)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_status = "idle"
        self.animation_index = 0
        self.movement_speed = 5
        self.animation_cooldown = 13
        self.moving_left = False
        self.moving_right = False
        self.velocity = 1
        self.landed = False

    def border(self):
        # Establish a border for player left and right at x axis
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.right > 960:
            self.rect.right = 960

        # Establish a border for player both up and down at y axis
        if self.rect.top < -0:
            self.rect.top = -0
        if self.rect.bottom > 540:
            self.rect.bottom = 540
    
    def update(self, group, group2):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        # print("Left:", self.rect.left, "Right:", self.rect.right, "Top:", self.rect.top, "Bottom:", self.rect.bottom)

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.movement_speed
            self.animation_index += 1
            self.moving_left = True
        elif keys[pygame.K_a] == False or keys[pygame.K_LEFT] == False:
            self.moving_left = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.movement_speed
            self.animation_index += 1
            self.moving_right = True
        elif keys[pygame.K_d] == False or keys[pygame.K_RIGHT] == False:
            self.moving_right = False
        if keys[pygame.K_w] == True or keys[pygame.K_UP] == True and self.jumped == False:
            self.rect.y += -15
            self.jumped = True
        elif keys[pygame.K_w] == False or keys[pygame.K_UP] == False:
            self.jumped = False


        # Cooldown by preventing animation going to fast
        if self.animation_index > self.animation_cooldown:
            self.animation_index = 0

        # Handle player animation maybe when polished try using the keywords like "idle", "walk", and "jump"
        if self.animation_index < len(self.images):
            if self.moving_left == True:
                image = pygame.image.load(f"assets/player/walk/{self.images[self.animation_index]}").convert_alpha()
                flipped = pygame.transform.flip(image, True, False)
                self.image = flipped
            elif self.moving_right == True:
                self.image = pygame.image.load(f"assets/player/walk/{self.images[self.animation_index]}").convert_alpha()
            elif self.moving_left == False and self.moving_right == False:
                self.image = pygame.image.load("assets/player/p1_stand.png").convert_alpha()
            elif self.moving_left == False:
                image = pygame.image.load("assets/player/p1_stand.png").convert_alpha()
                flipped = pygame.transform.flip(image, True, False)
                self.image = flipped

        # Efficient way of handling player collision by checking rect collision --> mask collision
        player_collided = pygame.sprite.spritecollide(self, group, False)
        if player_collided:
            player_mask_collided = pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask)
            if player_mask_collided:
                for obj in player_mask_collided:
                    self.rect.top = obj.rect.bottom
                    self.rect.bottom = obj.rect.top
                    print(obj, obj.rect.x, obj.rect.y, obj.rect.top)
                # print("Hit", player_collided, player_mask_collided)
                # self.image.fill("red")
                self.landed = True
        else:
            self.landed = False

        player_collided_door = pygame.sprite.spritecollide(self, group2, False)
        if player_collided_door:
            print("Door touched")

        # Decrease player gravity
        if not self.landed:
            self.rect.y += 1

        # Move player sprite
        self.rect.x += dx

        self.border()