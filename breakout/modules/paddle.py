import pygame

class Paddle:
    def __init__(self, x, y, width, height, color, screen_width):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.screen_width = screen_width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, x):
        self.rect.x = x
        # Keep the paddle on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
