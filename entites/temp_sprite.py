import pygame
from pygame.sprite import Sprite


class TempSprite(Sprite):
    def __init__(self, rect):
        Sprite.__init__(self)
        self.rect = rect