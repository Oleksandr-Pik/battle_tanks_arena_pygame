import pygame


class Tank():
    def __init__(self, window):
        self.field = window
        self.field_rect = self.field.get_rect()
        self.image = pygame.image.load("image/users_tank.png")
        self.image_rect = self.image.get_rect()
        self.image_rect.midbottom = self.field_rect.midbottom
        self.speed = 3
        # self.lives = 6
        self.angle = 0
        self.parent = None

    def bliitme(self):
        self.field.blit(self.image_rot, self.image_rect)

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.angle = 0
            if self.image_rect.y >= 0 + self.speed:
                self.image_rect.y -= self.speed

        elif keys[pygame.K_DOWN]:
            self.angle = 180
            if self.image_rect.y <= (self.field_rect.height - 32 - self.speed):
                self.image_rect.y += self.speed

        elif keys[pygame.K_LEFT]:
            self.angle = 90
            if self.image_rect.x >= 0 + self.speed:
                self.image_rect.x -= self.speed

        elif keys[pygame.K_RIGHT]:
            self.angle = -90
            if self.image_rect.x <= (self.field_rect.width - 32 - self.speed):
                self.image_rect.x += self.speed

        self.image_rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image_rect
