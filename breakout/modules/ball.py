import pygame
import os

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, speed, screen_width):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "default", "ball.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = speed
        self.vy = -speed
        self.screen_width = screen_width
        self.FRICTION = 0.01

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, gravity_enabled, gravity):
        if gravity_enabled:
            self.vy += gravity
            # Apply friction
            self.vx *= (1 - self.FRICTION)
            self.vy *= (1 - self.FRICTION)


        self.rect.x += self.vx
        self.rect.y += self.vy

        # Wall collision
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx *= -0.7
        elif self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.vx *= -0.7

        if self.rect.top < 0:
            self.rect.top = 0
            if gravity_enabled:
                self.vy *= -0.7
            else:
                self.vy *= -1
    def handle_paddle_collision(self, paddle):
        self.rect.bottom = paddle.rect.top
        self.vy *= -1

        # Transfer paddle velocity to the ball
        self.vx += paddle.velocity * 0.5
