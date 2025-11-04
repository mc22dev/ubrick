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
DARK_GRAY = (80, 80, 80)

BRICK_BREAKABLE_COLOR = WHITE
BRICK_UNBREAKABLE_COLOR = DARK_GRAY

ASSETS_DIR = "breakout/assets/default"

# Create assets directory if it doesn't exist
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# --- Generate Paddle Sprite ---
# Create a surface with a transparent background
paddle_surface = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT), pygame.SRCALPHA)
# Draw the paddle rectangle with rounded corners
pygame.draw.rect(paddle_surface, WHITE, (0, 0, PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=PADDLE_HEIGHT // 2)
pygame.image.save(paddle_surface, os.path.join(ASSETS_DIR, "paddle.png"))

# --- Generate Ball Sprite ---
# Create a square surface with a transparent background
ball_surface = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
# Draw the ball circle
pygame.draw.circle(ball_surface, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
pygame.image.save(ball_surface, os.path.join(ASSETS_DIR, "ball.png"))

# --- Generate Breakable Brick Sprite ---
# Create a surface with a transparent background
breakable_brick_surface = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT), pygame.SRCALPHA)
# Draw the brick with rounded corners
pygame.draw.rect(breakable_brick_surface, BRICK_BREAKABLE_COLOR, (0, 0, BRICK_WIDTH, BRICK_HEIGHT), border_radius=5)
pygame.image.save(breakable_brick_surface, os.path.join(ASSETS_DIR, "brick_green.png"))

# --- Generate Unbreakable Brick Sprite ---
# Create a surface with a transparent background
unbreakable_brick_surface = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT), pygame.SRCALPHA)
# Draw the brick with rounded corners
pygame.draw.rect(unbreakable_brick_surface, BRICK_UNBREAKABLE_COLOR, (0, 0, BRICK_WIDTH, BRICK_HEIGHT), border_radius=5)
pygame.image.save(unbreakable_brick_surface, os.path.join(ASSETS_DIR, "brick_red.png"))

# --- Generate Multi-Hit Brick Sprites ---
font = pygame.font.Font(None, 36)
for i in range(1, 10):
    brick_surface = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT), pygame.SRCALPHA)
    # Define a unique color for each brick level
    color = (255 - i * 20, 100 + i * 15, 100)
    pygame.draw.rect(brick_surface, color, (0, 0, BRICK_WIDTH, BRICK_HEIGHT), border_radius=5)

    # Add text indicating the number of hits remaining
    text = font.render(str(i), True, DARK_GRAY)
    text_rect = text.get_rect(center=(BRICK_WIDTH // 2, BRICK_HEIGHT // 2))
    brick_surface.blit(text, text_rect)

    pygame.image.save(brick_surface, os.path.join(ASSETS_DIR, f"brick_{i+1}.png"))


print("Default theme assets generated successfully.")

pygame.quit()
