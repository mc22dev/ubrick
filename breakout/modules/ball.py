import pygame
import os

class Ball:
    def __init__(self, x, y, radius, color, speed, screen_width):
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "default", "ball.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.dx = 1
        self.dy = -1
        self.vy = 0
        self.screen_width = screen_width

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, gravity_enabled, gravity):
        if gravity_enabled:
            self.vy += gravity
            self.rect.y += self.vy
        else:
            self.rect.y += self.speed * self.dy

        self.rect.x += self.speed * self.dx

        # Wall collision
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx *= -1
        elif self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.dx *= -1

        if self.rect.top < 0:
            self.rect.top = 0
            if gravity_enabled:
                self.vy *= -0.5 # bounce with some energy loss
            else:
                self.dy *= -1
