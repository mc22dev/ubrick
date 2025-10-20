import pygame

class Ball:
    def __init__(self, x, y, radius, color, speed, screen_width):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.color = color
        self.speed = speed
        self.dx = 1
        self.dy = -1
        self.vy = 0
        self.screen_width = screen_width

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def move(self, gravity_enabled, gravity):
        if gravity_enabled:
            self.vy += gravity
            self.rect.y += self.vy
        else:
            self.rect.y += self.speed * self.dy

        self.rect.x += self.speed * self.dx

        # Wall collision
        if self.rect.left < 0 or self.rect.right > self.screen_width:
            self.dx *= -1
        if self.rect.top < 0:
            if gravity_enabled:
                self.vy *= -0.5 # bounce with some energy loss
            else:
                self.dy *= -1
