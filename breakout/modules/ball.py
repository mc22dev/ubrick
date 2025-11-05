import pygame
import os
import pymunk

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, space):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "default", "ball.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        # Physics
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.95
        self.shape.friction = 0.9
        self.shape.collision_type = 1
        space.add(self.body, self.shape)

    def update(self):
        self.rect.centerx = self.body.position.x
        self.rect.centery = self.body.position.y
