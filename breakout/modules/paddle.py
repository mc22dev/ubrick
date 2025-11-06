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
        self.body.position = x + width / 2, y + height / 2
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.8
        self.shape.friction = 0.8
        self.shape.collision_type = 3
        space.add(self.body, self.shape)

        self.mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.mouse_joint = pymunk.PivotJoint(self.body, self.mouse_body, (0, 0), (0, 0))
        self.mouse_joint.max_force = 1000000
        space.add(self.mouse_joint)

    def update(self):
        self.rect.centerx = self.body.position.x
        self.rect.centery = self.body.position.y

    def set_position(self, pos):
        self.mouse_body.position = pos
