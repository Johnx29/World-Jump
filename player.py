import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, asset):
        super().__init__()
        self.image = pygame.image.load(asset).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)