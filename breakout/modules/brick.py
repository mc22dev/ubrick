import pygame

class Brick:
    def __init__(self, x, y, width, height, color, breakable=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.visible = True
        self.breakable = breakable

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)
