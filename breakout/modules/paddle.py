import pygame
import os
import math

class Paddle:
    SPEED = 15

    def __init__(self, x, y, width, height, color, screen_width, screen_height):
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "default", "paddle.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = float(x)
        self.y = float(y)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.prev_x = x
        self.prev_y = y
        self.velocity = 0
        self.target_x = x
        self.target_y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, x, y):
        self.target_x = x
        self.target_y = y

    def update(self, bricks):
        # Update velocity and previous position trackers
        self.velocity = self.rect.x - self.prev_x
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

        # Calculate direction vector
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Move paddle towards target
        if distance > 1:
            step_x = (dx / distance) * self.SPEED
            step_y = (dy / distance) * self.SPEED

            # Move horizontally
            self.x += step_x
            self.rect.x = int(round(self.x))
            colliding_bricks = [brick for brick in bricks if brick.visible and self.rect.colliderect(brick.rect)]
            for brick in colliding_bricks:
                if (self.rect.x - self.prev_x) > 0:  # Moving right
                    self.rect.right = brick.rect.left
                elif (self.rect.x - self.prev_x) < 0:  # Moving left
                    self.rect.left = brick.rect.right
                self.x = self.rect.x

            # Move vertically
            self.y += step_y
            self.rect.y = int(round(self.y))
            colliding_bricks = [brick for brick in bricks if brick.visible and self.rect.colliderect(brick.rect)]
            for brick in colliding_bricks:
                if (self.rect.y - self.prev_y) > 0:  # Moving down
                    self.rect.bottom = brick.rect.top
                elif (self.rect.y - self.prev_y) < 0:  # Moving up
                    self.rect.top = brick.rect.bottom
                self.y = self.rect.y

        # Keep the paddle on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
