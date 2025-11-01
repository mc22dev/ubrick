import pygame
import sys
from modules.paddle import Paddle
from modules.ball import Ball
from modules.brick import Brick
from modules.music import generate_music
import os

class Game:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pygame.init()
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except pygame.error:
            self.sound_enabled = False

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.GRAY = (0, 0, 0) # Background Color
        self.WHITE = (255, 255, 255)
        self.PADDLE_WIDTH = 100
        self.PADDLE_HEIGHT = 20
        self.BALL_RADIUS = 10
        self.BALL_SPEED = 5
        self.BRICK_WIDTH = 80
        self.BRICK_HEIGHT = 30
        self.BRICK_SPACING = 5
        self.GRAVITY = 0.2

        # Screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bolo Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Game objects
        self.paddle = Paddle(self.WIDTH // 2 - self.PADDLE_WIDTH // 2, self.HEIGHT - self.PADDLE_HEIGHT - 10, self.PADDLE_WIDTH, self.PADDLE_HEIGHT, self.WHITE, self.WIDTH)
        self.ball = Ball(self.WIDTH // 2, self.HEIGHT // 2, self.BALL_RADIUS, self.WHITE, self.BALL_SPEED, self.WIDTH)

        self.music_enabled = True
        self.sound_effects_enabled = True

        if self.sound_enabled:
            self.paddle_hit_sound = pygame.mixer.Sound(os.path.join(self.base_path, "assets", "default", "paddle_hit.wav"))
            self.brick_hit_sound = pygame.mixer.Sound(os.path.join(self.base_path, "assets", "default", "brick_hit.wav"))
            self.win_sound = pygame.mixer.Sound(os.path.join(self.base_path, "assets", "default", "win.wav"))
            self.background_music = generate_music()
            if self.music_enabled:
                self.background_music.play(-1)

        # Levels
        self.current_level = 1
        self.bricks = self.load_level(self.current_level)

        # Game state
        self.score = 0
        self.highscore = 0
        self._load_highscore()
        self.gravity_enabled = False
        self.magnetic_paddle = False
        self.ball_stuck = False
        self.ai_enabled = False
        self.running = True
        self.game_state = "playing"

        # Config screen button rects
        self.gravity_rect = None
        self.magnetic_rect = None
        self.ai_rect = None
        self.music_rect = None
        self.sound_rect = None

    def _load_highscore(self):
        highscore_file = os.path.join(self.base_path, "highscore.txt")
        try:
            with open(highscore_file, 'r') as f:
                self.highscore = int(f.read())
        except (FileNotFoundError, ValueError):
            self.highscore = 0

    def _save_highscore(self):
        highscore_file = os.path.join(self.base_path, "highscore.txt")
        with open(highscore_file, 'w') as f:
            f.write(str(self.highscore))

    def _reset_game(self):
        self.score = 0
        self.current_level = 1
        self.bricks = self.load_level(self.current_level)
        self.paddle.rect.x = self.WIDTH // 2 - self.PADDLE_WIDTH // 2
        self.paddle.rect.y = self.HEIGHT - self.PADDLE_HEIGHT - 10
        self.ball.rect.x = self.WIDTH // 2
        self.ball.rect.y = self.HEIGHT // 2
        self.ball.dx = 1
        self.ball.dy = -1
        self.ball.vy = 0
        self.game_state = "playing"
        self.gravity_enabled = False
        self.magnetic_paddle = False
        self.ball_stuck = False

    def load_level(self, level_number):
        bricks = []
        level_file = os.path.join(self.base_path, "levels", f"level_{level_number}.txt")
        with open(level_file, 'r') as f:
            level_data = [line.strip() for line in f]

        num_rows = len(level_data)
        num_cols = len(level_data[0]) if num_rows > 0 else 0

        grid_width = num_cols * (self.BRICK_WIDTH + self.BRICK_SPACING) - self.BRICK_SPACING
        grid_height = num_rows * (self.BRICK_HEIGHT + self.BRICK_SPACING) - self.BRICK_SPACING

        offset_x = (self.WIDTH - grid_width) // 2
        offset_y = 50

        for row_idx, line in enumerate(level_data):
            for col_idx, char in enumerate(line):
                if char in 'XU':
                    brick_x = offset_x + col_idx * (self.BRICK_WIDTH + self.BRICK_SPACING)
                    brick_y = offset_y + row_idx * (self.BRICK_HEIGHT + self.BRICK_SPACING)
                    breakable = (char == 'X')
                    brick = Brick(brick_x, brick_y, breakable=breakable)
                    bricks.append(brick)
        return bricks

    def run(self):
        while self.running:
            if self.game_state == "playing":
                self.handle_events()
                self.update()
                self.draw()
            elif self.game_state == "game_over":
                self.draw_game_over()
            elif self.game_state == "you_win":
                self.draw_you_win()
            elif self.game_state == "config":
                self.handle_events()
                self.draw_config_screen()

        pygame.quit()
        sys.exit()

    def draw_game_over(self):
        self.screen.fill(self.GRAY)
        game_over_text = self.font.render("Game Over", True, self.WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        highscore_text = self.font.render(f"High Score: {self.highscore}", True, self.WHITE)
        restart_text = self.font.render("Press any key to play again", True, self.WHITE)

        self.screen.blit(game_over_text, (self.WIDTH // 2 - game_over_text.get_width() // 2, self.HEIGHT // 2 - 100))
        self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, self.HEIGHT // 2 - 50))
        self.screen.blit(highscore_text, (self.WIDTH // 2 - highscore_text.get_width() // 2, self.HEIGHT // 2))
        self.screen.blit(restart_text, (self.WIDTH // 2 - restart_text.get_width() // 2, self.HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self._reset_game()

    def draw_you_win(self):
        self.screen.fill(self.GRAY)
        you_win_text = self.font.render("You Win!", True, self.WHITE)
        self.screen.blit(you_win_text, (self.WIDTH // 2 - you_win_text.get_width() // 2, self.HEIGHT // 2 - you_win_text.get_height() // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.running = False

    def draw_config_screen(self):
        self.screen.fill(self.GRAY)
        title_text = self.font.render("Configuration", True, self.WHITE)
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 50))

        # Gravity option
        gravity_text = self.font.render(f"Gravity: {'On' if self.gravity_enabled else 'Off'}", True, self.WHITE)
        self.gravity_rect = self.screen.blit(gravity_text, (self.WIDTH // 2 - gravity_text.get_width() // 2, 150))

        # Magnetic paddle option
        magnetic_text = self.font.render(f"Magnetic Paddle: {'On' if self.magnetic_paddle else 'Off'}", True, self.WHITE)
        self.magnetic_rect = self.screen.blit(magnetic_text, (self.WIDTH // 2 - magnetic_text.get_width() // 2, 200))

        # AI mode option
        ai_text = self.font.render(f"AI Mode: {'On' if self.ai_enabled else 'Off'}", True, self.WHITE)
        self.ai_rect = self.screen.blit(ai_text, (self.WIDTH // 2 - ai_text.get_width() // 2, 250))

        # Music option
        music_text = self.font.render(f"Music: {'On' if self.music_enabled else 'Off'}", True, self.WHITE)
        self.music_rect = self.screen.blit(music_text, (self.WIDTH // 2 - music_text.get_width() // 2, 300))

        # Sound effects option
        sound_text = self.font.render(f"Sound Effects: {'On' if self.sound_effects_enabled else 'Off'}", True, self.WHITE)
        self.sound_rect = self.screen.blit(sound_text, (self.WIDTH // 2 - sound_text.get_width() // 2, 350))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if self.game_state == "playing":
                        self.game_state = "config"
                    elif self.game_state == "config":
                        self.game_state = "playing"
            if self.game_state == "config" and event.type == pygame.MOUSEBUTTONDOWN:
                if self.gravity_rect and self.gravity_rect.collidepoint(event.pos):
                    self.gravity_enabled = not self.gravity_enabled
                elif self.magnetic_rect and self.magnetic_rect.collidepoint(event.pos):
                    self.magnetic_paddle = not self.magnetic_paddle
                elif self.ai_rect and self.ai_rect.collidepoint(event.pos):
                    self.ai_enabled = not self.ai_enabled
                elif self.music_rect and self.music_rect.collidepoint(event.pos):
                    self.music_enabled = not self.music_enabled
                    if self.music_enabled:
                        self.background_music.play(-1)
                    else:
                        self.background_music.stop()
                elif self.sound_rect and self.sound_rect.collidepoint(event.pos):
                    self.sound_effects_enabled = not self.sound_effects_enabled
            if self.game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.gravity_enabled = not self.gravity_enabled
                    if event.key == pygame.K_m:
                        self.magnetic_paddle = not self.magnetic_paddle
                    if event.key == pygame.K_a:
                        self.ai_enabled = not self.ai_enabled
                if event.type == pygame.MOUSEBUTTONDOWN and self.ball_stuck:
                    self.ball_stuck = False

    def update(self):
        # Paddle movement
        if self.ai_enabled:
            # AI controls the paddle
            self.paddle.move(self.ball.rect.centerx - self.paddle.rect.width // 2)
        else:
            # Player controls the paddle
            mouse_x = pygame.mouse.get_pos()[0]
            self.paddle.move(mouse_x - self.paddle.rect.width // 2)

        # Ball movement
        if not self.ball_stuck:
            self.ball.move(self.gravity_enabled, self.GRAVITY)

        # Ball and paddle collision
        if self.ball.rect.colliderect(self.paddle.rect):
            if self.magnetic_paddle:
                self.ball_stuck = True
            else:
                # Prevent the ball from sinking into the paddle
                self.ball.rect.bottom = self.paddle.rect.top
                if self.gravity_enabled:
                    self.ball.vy *= -0.8
                else:
                    self.ball.dy *= -1
                if self.sound_enabled and self.sound_effects_enabled:
                    self.paddle_hit_sound.play()

        if self.ball_stuck:
            self.ball.rect.x = self.paddle.rect.x + self.paddle.rect.width // 2 - self.ball.rect.width // 2
            self.ball.rect.y = self.paddle.rect.y - self.ball.rect.height

        # Ball and brick collision
        for brick in self.bricks:
            if brick.visible and self.ball.rect.colliderect(brick.rect):
                if brick.breakable:
                    brick.visible = False
                    self.score += 10

                # Collision logic
                # To find the side of collision, we check the overlap of the rectangles
                # And see which side has the minimum overlap

                overlap_left = self.ball.rect.right - brick.rect.left
                overlap_right = brick.rect.right - self.ball.rect.left
                overlap_top = self.ball.rect.bottom - brick.rect.top
                overlap_bottom = brick.rect.bottom - self.ball.rect.top

                min_overlap_x = min(overlap_left, overlap_right)
                min_overlap_y = min(overlap_top, overlap_bottom)

                if min_overlap_x < min_overlap_y:
                    self.ball.dx *= -1
                elif min_overlap_y < min_overlap_x:
                    if self.gravity_enabled:
                        self.ball.vy *= -0.5
                    else:
                        self.ball.dy *= -1
                else: # Corner hit
                    self.ball.dx *= -1
                    if self.gravity_enabled:
                        self.ball.vy *= -0.5
                    else:
                        self.ball.dy *= -1

                if self.sound_enabled and self.sound_effects_enabled:
                    self.brick_hit_sound.play()
                break

        # Check for level completion
        if all(not brick.visible for brick in self.bricks if brick.breakable):
            if self.sound_enabled and self.sound_effects_enabled:
                self.win_sound.play()
            self.current_level += 1
            if self.current_level > 50:
                self.game_state = "you_win"
            else:
                self.bricks = self.load_level(self.current_level)

        # Ball and bottom wall collision
        if self.ball.rect.bottom > self.HEIGHT:
            if self.score > self.highscore:
                self.highscore = self.score
                self._save_highscore()
            self.game_state = "game_over"

    def draw(self):
        self.screen.fill(self.GRAY)

        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw gravity status
        gravity_text = self.font.render(f"Gravity: {'On' if self.gravity_enabled else 'Off'}", True, self.WHITE)
        self.screen.blit(gravity_text, (self.WIDTH - 150, 10))

        # Draw magnetic paddle status
        magnetic_text = self.font.render(f"Magnetic: {'On' if self.magnetic_paddle else 'Off'}", True, self.WHITE)
        self.screen.blit(magnetic_text, (self.WIDTH - 150, 40))

        # Draw AI mode status
        ai_text = self.font.render(f"AI Mode: {'On' if self.ai_enabled else 'Off'}", True, self.WHITE)
        self.screen.blit(ai_text, (self.WIDTH - 150, 70))

        # Draw level
        level_text = self.font.render(f"Level: {self.current_level}", True, self.WHITE)
        self.screen.blit(level_text, (self.WIDTH // 2 - 50, 10))

        pygame.display.flip()
        self.clock.tick(60)
