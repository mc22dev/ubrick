import pygame
import os
import pymunk

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, space):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "default", "paddle.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        # Physics
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.8
        self.shape.friction = 0.8
        space.add(self.body, self.shape)

    def update(self):
        self.rect.centerx = self.body.position.x
        self.rect.centery = self.body.position.y

    def set_position(self, x):
        self.body.position = x, self.body.position.y
        self.body.velocity = 0, 0
