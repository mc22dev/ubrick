import pygame
import os

class Paddle:
    def __init__(self, x, y, width, height, color, screen_width):
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "default", "paddle.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen_width = screen_width

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, x):
        self.rect.x = x
        # Keep the paddle on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
