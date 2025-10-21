import pygame
import os

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, breakable=True):
        super().__init__()
        self.breakable = breakable

        # Load image based on breakable status
        image_name = "brick_green.png" if self.breakable else "brick_red.png"
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_path, "assets", "default", image_name)

        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect(topleft=(x,y))

        self.visible = True

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
