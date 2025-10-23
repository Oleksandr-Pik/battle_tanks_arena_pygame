import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, x, y, explosions, sound):
        Sprite.__init__(self)
        self.image = pygame.image.load("image/bang3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.alpha = 0
        explosions.add(self)
        self.flag = True
        self.image.set_alpha(self.alpha)
        sound.play()
        # sound.set_volume(0.5)

    def update(self):
        if self.flag:
            self.alpha += 20
            if self.alpha >= 255:
                self.alpha = 255
                self.flag = False
        else:
            self.alpha -= 15
            if self.alpha <= 0:
                self.alpha = 0
                self.kill()
        self.image.set_alpha(self.alpha)

