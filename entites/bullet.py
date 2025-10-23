import pygame
import math


class Bullet:
    def __init__(self, window, tank, sound):
        self.screen = window
        self.parent = tank
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("image/bullet.png")
        self.image_rect = self.image.get_rect()
        self.image_rect.center = tank.image_rect.center
        self.angle = tank.angle
        self.speed = 10
        sound.play()

    def blitme(self):
        self.screen.blit(self.image_rot, self.image_rect)

    def move(self):
        self.image_rot = pygame.transform.rotate(self.image, self.angle)
        self.image_rect.x -= self.speed * int(math.sin(math.radians(self.angle)))
        self.image_rect.y -= self.speed * int(math.cos(math.radians(self.angle)))
