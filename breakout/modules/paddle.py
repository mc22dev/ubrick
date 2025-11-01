import pygame
import os

class Paddle:
    def __init__(self, x, y, width, height, color, screen_width, screen_height):
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "default", "paddle.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last_x = x
        self.prev_x = x
        self.prev_y = y
        self.velocity = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, x, y):
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
        self.velocity = x - self.last_x
        self.last_x = x
        self.rect.x = x
        self.rect.y = y
        # Keep the paddle on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
