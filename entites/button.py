import pygame


class Button():
    def __init__(self, window, y, text, *args):
        self.w = 270
        self.h = 90
        self.screen = window
        self.screen_rect = self.screen.get_rect()
        self.x = self.screen_rect.centerx - self.w / 2
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color_off = (223, 156, 36)
        self.color_on = (113, 137, 41)
        self.color_text = (35, 57, 55)
        self.rect_shadow = (self.x + 5, self.y + 5, self.w, self.h)
        self.screen_alfa = pygame.Surface((self.screen_rect.w, self.screen_rect.h), pygame.SRCALPHA)
        self.is_button_on = False
        self.args = args
        self.font = pygame.font.SysFont(None, 40, bold=True, italic=False)
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color_text)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def blitme(self):
        self.color = self.color_on if self.is_button_on else self.color_off
        pygame.draw.rect(self.screen_alfa, (*self.color, 128), self.rect_shadow, width=0, border_radius=15)
        self.screen.blit(self.screen_alfa, (0, 0))
        pygame.draw.rect(self.screen, self.color, self.rect, width=0, border_radius=15)
        pygame.draw.rect(self.screen, self.color_text, self.rect, width=5, border_radius=15)
        self.screen.blit(self.text_surface, self.text_rect)

    def mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_button_on = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and self.is_button_on and event.button == 1:
            if self.args:
                for action in self.args:
                    action()
            else:
                return True

