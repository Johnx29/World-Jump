import pygame

class Ground():
    def __init__(self, asset):
        self.sprite = pygame.image.load(asset)
        self.rect = self.sprite.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite)