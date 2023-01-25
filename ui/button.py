import pygame
from ui.button_ident import ButtonIdent


class Button:

    def __init__(self, pos, size, color, text, font: pygame.font.Font, ident: ButtonIdent):
        self.x = pos[0]
        self.y = pos[1]
        self.w = size[0]
        self.h = size[1]
        self.color = color
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.txt_surface = font.render(text, True, (0, 0, 0))
        self.is_visible = True
        self.font = font
        self.ident = ident

    def draw(self, surface):
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def update_text(self, text):
        self.txt_surface = self.font.render(text, True, (0, 0, 0))

    def update_coords(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def clicked(self, event):

        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos) and self.is_visible

        return False
