import pygame
import os

# Initialize pygame
pygame.init()

# Define constants
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 80
BRICK_HEIGHT = 30

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

ASSETS_DIR = "breakout/assets/default"

# Create assets directory if it doesn't exist
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# --- Generate Paddle Sprite ---
# Create a surface with a transparent background
paddle_surface = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT), pygame.SRCALPHA)
# Draw the paddle rectangle
pygame.draw.rect(paddle_surface, WHITE, (0, 0, PADDLE_WIDTH, PADDLE_HEIGHT))
pygame.image.save(paddle_surface, os.path.join(ASSETS_DIR, "paddle.png"))

# --- Generate Ball Sprite ---
# Create a square surface with a transparent background
ball_surface = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
# Draw the ball circle
pygame.draw.circle(ball_surface, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
pygame.image.save(ball_surface, os.path.join(ASSETS_DIR, "ball.png"))

# --- Generate Green Brick Sprite ---
green_brick_surface = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
green_brick_surface.fill(GREEN)
pygame.image.save(green_brick_surface, os.path.join(ASSETS_DIR, "brick_green.png"))

# --- Generate Red Brick Sprite ---
red_brick_surface = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
red_brick_surface.fill(RED)
pygame.image.save(red_brick_surface, os.path.join(ASSETS_DIR, "brick_red.png"))

print("Default theme assets generated successfully.")

pygame.quit()
