import pygame

class Player():
    def __init__(self, asset):
        print("Created player object")
        self.sprite = pygame.image.load(asset).convert_alpha()
        self.rect = self.sprite.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite)