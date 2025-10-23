import pygame
from pygame.sprite import Sprite

class Wall(Sprite):
    def __init__(self, window, point):
        Sprite.__init__(self)
        self.screen = window
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/block_brick.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = point
