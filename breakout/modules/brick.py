import pygame
import os
import pymunk

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, hits_required, space):
        super().__init__()
        self.hits_required = hits_required
        self.breakable = hits_required > 0

        self.update_image()
        self.rect = self.image.get_rect(topleft=(x, y))

        # Physics
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = x + self.rect.width / 2, y + self.rect.height / 2
        shape = pymunk.Poly.create_box(body, self.rect.size)
        shape.elasticity = 0.5
        shape.friction = 0.7
        shape.collision_type = 2 # Differentiate bricks
        shape.parent_brick = self # Link back to the sprite
        space.add(body, shape)

    def update_image(self):
        if not self.breakable:
            image_name = "brick_red.png"
        elif self.hits_required == 1:
            image_name = "brick_green.png"
        else:
            image_name = f"brick_{self.hits_required}.png"

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_path, "assets", "default", image_name)
        self.image = pygame.image.load(image_path).convert_alpha()

    def hit(self):
        if self.breakable:
            self.hits_required -= 1
            if self.hits_required == 0:
                self.kill()
                return 10
            else:
                self.update_image()
        return 0
