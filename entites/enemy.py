from types import new_class

import pygame
import random
from pygame.sprite import Sprite


class Enemy(Sprite):
    def __init__(self, window, x, y, ):
        Sprite.__init__(self)
        self.screen = window
        self.screen_rect = self.screen.get_rect()
        self.img = pygame.image.load("image/enemy.png")
        self.image = self.img
        self.rect = self.image.get_rect()
        self.image_rect = self.rect
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.angle = 180
        self.direction = {0: (0, -1), 180: (0, 1), 90: (-1, 0), -90: (1, 0)}

    def turn(self):
        self.rect.x -= self.direction[self.angle][0] * self.speed
        self.rect.y -= self.direction[self.angle][1] * self.speed

        self.new_angle = random.randrange(-90, 181, 90)
        return self.new_angle

    def update(self):
        self.rect.x += self.direction[self.angle][0] * self.speed
        self.rect.y += self.direction[self.angle][1] * self.speed

        if self.rect.x < 0:
            self.rect.x = 0
            self.angle = self.turn()
        if self.rect.x > self.screen_rect.width - 32:
            self.rect.x = self.screen_rect.width - 32
            self.angle = self.turn()
        if self.rect.y < 0:
            self.rect.y = 0
            self.angle = self.turn()
        if self.rect.y > self.screen_rect.height - 32:
            self.rect.y = self.screen_rect.height - 32
            self.angle = self.turn()

        self.image = pygame.transform.rotate(self.img, self.angle)
        self.image_rot = pygame.transform.rotate(self.image, self.angle)
        self.image_rect = self.rect
