import pygame
import sys
from modules.paddle import Paddle
from modules.ball import Ball
from modules.brick import Brick
from modules.music import generate_music
import os
import pymunk

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
        self.WIDTH, self.HEIGHT = 1280, 720
        self.GRAY = (0, 0, 0) # Background Color
        self.WHITE = (255, 255, 255)
        self.PADDLE_WIDTH = 100
        self.PADDLE_HEIGHT = 20
        self.BALL_RADIUS = 10
        self.BALL_SPEED = 5
        self.BRICK_WIDTH = 80
        self.BRICK_HEIGHT = 30
        self.BRICK_SPACING = 5

        # Screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bolo Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Physics
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 900.0)
        self._create_walls()

        # Collision handler
        self.space.on_collision(1, 2, begin=self.handle_ball_brick_collision)
        self.space.on_collision(1, 3, begin=self.handle_ball_paddle_collision, post_solve=self.handle_ball_paddle_collision_post_solve)
        self.space.on_collision(3, 2, begin=self.handle_paddle_brick_collision)

        # Game objects
        self.paddle = Paddle(self.WIDTH // 2 - self.PADDLE_WIDTH // 2, self.HEIGHT - self.PADDLE_HEIGHT - 10, self.PADDLE_WIDTH, self.PADDLE_HEIGHT, self.space)
        self.ball = Ball(self.WIDTH // 2, self.HEIGHT // 2, self.BALL_RADIUS, self.space)

        self.all_sprites = pygame.sprite.Group()
        self.bricks_group = pygame.sprite.Group()
        self.all_sprites.add(self.paddle, self.ball)

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
        self.load_level(self.current_level)

        # Game state
        self.score = 0
        self.highscore = 0
        self._load_highscore()
        self.lives = 3
        self.paddle_start_x = 0
        self.paddle_start_y = 0
        self.magnetic_paddle = False
        self.ball_stuck = True
        self.ai_enabled = False
        self.running = True
        self.game_state = "welcome"
        self.selected_level = 1
        self.max_level = self._get_max_level()

        # Config screen button rects
        self.gravity_rect = None
        self.magnetic_rect = None
        self.ai_rect = None
        self.music_rect = None
        self.sound_rect = None
        self.quit_rect = None
        self.show_fps = False
        self.fps_rect = None

    def _create_walls(self):
        walls = [
            pymunk.Segment(self.space.static_body, (0, 0), (self.WIDTH, 0), 1),
            pymunk.Segment(self.space.static_body, (0, 0), (0, self.HEIGHT), 1),
            pymunk.Segment(self.space.static_body, (self.WIDTH, 0), (self.WIDTH, self.HEIGHT), 1)
        ]
        for wall in walls:
            wall.elasticity = 0.8
            wall.friction = 0.8
            self.space.add(wall)

    def handle_ball_brick_collision(self, arbiter, space, data):
        brick_shape = arbiter.shapes[1]
        brick = brick_shape.parent_brick
        points = brick.hit()
        self.score += points
        if points > 0:
            space.remove(brick_shape, brick_shape.body)
            brick.kill()
        return True

    def handle_ball_paddle_collision(self, arbiter, space, data):
        if self.magnetic_paddle:
            self.ball_stuck = True
        return True

    def handle_ball_paddle_collision_post_solve(self, arbiter, space, data):
        paddle_velocity = self.paddle.body.velocity
        self.ball.body.apply_impulse_at_local_point((paddle_velocity.x * 0.1, 0))

    def handle_paddle_brick_collision(self, arbiter, space, data):
        return False

    def _get_max_level(self):
        levels_path = os.path.join(self.base_path, "levels")
        level_files = [f for f in os.listdir(levels_path) if f.startswith("level_") and f.endswith(".txt")]
        return len(level_files)

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
        self.lives = 3
        self.paddle.rect.x = self.WIDTH // 2 - self.PADDLE_WIDTH // 2
        self.paddle.rect.y = self.HEIGHT - self.PADDLE_HEIGHT - 10
        self.ball.rect.x = self.WIDTH // 2
        self.ball.rect.y = self.HEIGHT // 2
        self.ball.vx = self.BALL_SPEED
        self.ball.vy = -self.BALL_SPEED
        self.game_state = "welcome"
        self.gravity_enabled = False
        self.magnetic_paddle = False
        self.ball_stuck = False

    def load_level(self, level_number):
        for brick in self.bricks_group:
            brick.kill()

        level_file = os.path.join(self.base_path, "levels", f"level_{level_number}.txt")
        with open(level_file, 'r') as f:
            level_data = [line.strip() for line in f]

        num_rows = len(level_data)
        num_cols = max(len(row) for row in level_data) if level_data else 0

        grid_width = num_cols * (self.BRICK_WIDTH + self.BRICK_SPACING) - self.BRICK_SPACING
        grid_height = num_rows * (self.BRICK_HEIGHT + self.BRICK_SPACING) - self.BRICK_SPACING

        offset_x = (self.WIDTH - grid_width) // 2
        offset_y = 50

        paddle_defined_in_level = False
        self.brick_zone_bottom = 0
        for row_idx, line in enumerate(level_data):
            for col_idx, char in enumerate(line):
                if char == 'P':
                    self.paddle.x = offset_x + col_idx * (self.BRICK_WIDTH + self.BRICK_SPACING)
                    self.paddle.y = offset_y + row_idx * (self.BRICK_HEIGHT + self.BRICK_SPACING)
                    self.paddle.rect.topleft = (self.paddle.x, self.paddle.y)
                    self.paddle.target_x = self.paddle.x
                    self.paddle.target_y = self.paddle.y
                    paddle_defined_in_level = True
                    continue

                hits = 0
                if char == 'X':
                    hits = 1
                elif char == 'U':
                    hits = 0
                elif '2' <= char <= '9':
                    hits = int(char)
                elif char == '0':
                    hits = 10
                else:
                    continue

                brick_x = offset_x + col_idx * (self.BRICK_WIDTH + self.BRICK_SPACING)
                brick_y = offset_y + row_idx * (self.BRICK_HEIGHT + self.BRICK_SPACING)

                brick = Brick(brick_x, brick_y, hits_required=hits, space=self.space)
                self.all_sprites.add(brick)
                self.bricks_group.add(brick)
                if brick_y + self.BRICK_HEIGHT > self.brick_zone_bottom:
                    self.brick_zone_bottom = brick_y + self.BRICK_HEIGHT

        if not paddle_defined_in_level:
            self.paddle.x = self.WIDTH // 2 - self.PADDLE_WIDTH // 2
            self.paddle.y = self.HEIGHT - self.PADDLE_HEIGHT - 10
            self.paddle.rect.topleft = (self.paddle.x, self.paddle.y)
            self.paddle.target_x = self.paddle.x
            self.paddle.target_y = self.paddle.y

        self.paddle_start_x = self.paddle.x
        self.paddle_start_y = self.paddle.y
        self.ball_stuck = True

    def _lose_life(self):
        self.lives -= 1
        if self.lives > 0:
            self.paddle.x = self.paddle_start_x
            self.paddle.y = self.paddle_start_y
            self.paddle.rect.topleft = (self.paddle.x, self.paddle.y)
            self.paddle.target_x = self.paddle.x
            self.paddle.target_y = self.paddle.y
            self.ball_stuck = True
        else:
            if self.score > self.highscore:
                self.highscore = self.score
                self._save_highscore()
            self.game_state = "game_over"

    def run(self):
        while self.running:
            is_playing = self.game_state == "playing"
            pygame.mouse.set_visible(not is_playing)
            pygame.event.set_grab(is_playing)

            if self.game_state == "welcome":
                self.handle_events()
                self.draw_welcome_screen()
            elif self.game_state == "playing":
                self.handle_events()
                self.update()
                self.draw()
            elif self.game_state == "game_over":
                self.handle_events()
                self.draw_game_over()
            elif self.game_state == "you_win":
                self.handle_events()
                self.draw_you_win()
            elif self.game_state == "config":
                self.handle_events()
                self.draw_config_screen()
            elif self.game_state == "paused":
                self.handle_events()
                self.draw_paused_screen()

            self.clock.tick(60)

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

    def draw_you_win(self):
        self.screen.fill(self.GRAY)
        you_win_text = self.font.render("You Win!", True, self.WHITE)
        self.screen.blit(you_win_text, (self.WIDTH // 2 - you_win_text.get_width() // 2, self.HEIGHT // 2 - you_win_text.get_height() // 2))
        pygame.display.flip()

    def draw_config_screen(self):
        self.screen.fill(self.GRAY)
        title_text = self.font.render("Configuration", True, self.WHITE)
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 50))

        # Gravity option
        gravity_text = self.font.render(f"Gravity: {'On' if self.gravity_enabled else 'Off'} (g)", True, self.WHITE)
        self.gravity_rect = self.screen.blit(gravity_text, (self.WIDTH // 2 - gravity_text.get_width() // 2, 150))

        # Magnetic paddle option
        magnetic_text = self.font.render(f"Magnetic Paddle: {'On' if self.magnetic_paddle else 'Off'} (m)", True, self.WHITE)
        self.magnetic_rect = self.screen.blit(magnetic_text, (self.WIDTH // 2 - magnetic_text.get_width() // 2, 200))

        # AI mode option
        ai_text = self.font.render(f"AI Mode: {'On' if self.ai_enabled else 'Off'} (a)", True, self.WHITE)
        self.ai_rect = self.screen.blit(ai_text, (self.WIDTH // 2 - ai_text.get_width() // 2, 250))

        # Music option
        music_text = self.font.render(f"Music: {'On' if self.music_enabled else 'Off'} (u)", True, self.WHITE)
        self.music_rect = self.screen.blit(music_text, (self.WIDTH // 2 - music_text.get_width() // 2, 300))

        # Sound effects option
        sound_text = self.font.render(f"Sound Effects: {'On' if self.sound_effects_enabled else 'Off'} (s)", True, self.WHITE)
        self.sound_rect = self.screen.blit(sound_text, (self.WIDTH // 2 - sound_text.get_width() // 2, 350))

        # Show FPS option
        fps_text = self.font.render(f"Show FPS: {'On' if self.show_fps else 'Off'} (f)", True, self.WHITE)
        self.fps_rect = self.screen.blit(fps_text, (self.WIDTH // 2 - fps_text.get_width() // 2, 400))

        # Quit option
        quit_text = self.font.render("Quit (q)", True, self.WHITE)
        self.quit_rect = self.screen.blit(quit_text, (self.WIDTH // 2 - quit_text.get_width() // 2, 450))

        pygame.display.flip()

    def draw_paused_screen(self):
        self.screen.fill(self.GRAY)
        paused_text = self.font.render("Paused", True, self.WHITE)
        self.screen.blit(paused_text, (self.WIDTH // 2 - paused_text.get_width() // 2, self.HEIGHT // 2 - paused_text.get_height() // 2))
        pygame.display.flip()

    def draw_welcome_screen(self):
        self.screen.fill(self.GRAY)

        # Manually update ball position for preview
        self.ball.rect.x = self.paddle.rect.x + self.paddle.rect.width // 2 - self.ball.rect.width // 2
        self.ball.rect.y = self.paddle.rect.y - self.ball.rect.height

        # Draw the bricks for the selected level
        self.bricks_group.draw(self.screen)
        self.screen.blit(self.paddle.image, self.paddle.rect)
        self.screen.blit(self.ball.image, self.ball.rect)

        # Create a semi-transparent panel for the text
        panel_height = 200
        panel_y_start = self.HEIGHT - 220
        text_panel = pygame.Surface((self.WIDTH, panel_height))
        text_panel.set_alpha(150)
        text_panel.fill((0, 0, 0))  # Black background
        self.screen.blit(text_panel, (0, panel_y_start))

        title_text = self.font.render("Bolo Breakout", True, self.WHITE)
        level_text = self.font.render(f"Level: {self.selected_level}/{self.max_level}", True, self.WHITE)
        controls_text = self.font.render("Use left/right arrows to change level", True, self.WHITE)
        prompt_text = self.font.render("Press any key to start", True, self.WHITE)

        # Adjust text positions to be on the panel
        text_y_start = panel_y_start + 20
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, text_y_start))
        self.screen.blit(level_text, (self.WIDTH // 2 - level_text.get_width() // 2, text_y_start + 50))
        self.screen.blit(controls_text, (self.WIDTH // 2 - controls_text.get_width() // 2, text_y_start + 100))
        self.screen.blit(prompt_text, (self.WIDTH // 2 - prompt_text.get_width() // 2, text_y_start + 150))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state == "game_over":
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self._reset_game()
            elif self.game_state == "you_win":
                if event.type == pygame.KEYDOWN:
                    self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "welcome":
                    self.current_level = self.selected_level
                    self.load_level(self.current_level)
                    self.game_state = "playing"
            if event.type == pygame.KEYDOWN:
                if self.game_state == "welcome":
                    if event.key == pygame.K_LEFT:
                        self.selected_level = max(1, self.selected_level - 1)
                        self.load_level(self.selected_level)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_level = min(self.max_level, self.selected_level + 1)
                        self.load_level(self.selected_level)
                    else:
                        self.current_level = self.selected_level
                        self.load_level(self.current_level)
                        self.game_state = "playing"
                elif event.key == pygame.K_c:
                    if self.game_state == "playing":
                        self.game_state = "config"
                    elif self.game_state == "config":
                        self.game_state = "playing"
                if event.key == pygame.K_p:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        self.game_state = "playing"
                elif self.game_state == "config":
                    if event.key == pygame.K_g:
                        self.gravity_enabled = not self.gravity_enabled
                    elif event.key == pygame.K_m:
                        self.magnetic_paddle = not self.magnetic_paddle
                        if not self.magnetic_paddle:
                            self.ball_stuck = False
                    elif event.key == pygame.K_a:
                        self.ai_enabled = not self.ai_enabled
                    elif event.key == pygame.K_u:
                        self.music_enabled = not self.music_enabled
                        if self.music_enabled:
                            self.background_music.play(-1)
                        else:
                            self.background_music.stop()
                    elif event.key == pygame.K_s:
                        self.sound_effects_enabled = not self.sound_effects_enabled
                    elif event.key == pygame.K_f:
                        self.show_fps = not self.show_fps
                    elif event.key == pygame.K_q:
                        self.running = False
            if self.game_state == "config" and event.type == pygame.MOUSEBUTTONDOWN:
                if self.gravity_rect and self.gravity_rect.collidepoint(event.pos):
                    self.gravity_enabled = not self.gravity_enabled
                elif self.fps_rect and self.fps_rect.collidepoint(event.pos):
                    self.show_fps = not self.show_fps
                elif self.magnetic_rect and self.magnetic_rect.collidepoint(event.pos):
                    self.magnetic_paddle = not self.magnetic_paddle
                    if not self.magnetic_paddle:
                        self.ball_stuck = False
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
                elif self.quit_rect and self.quit_rect.collidepoint(event.pos):
                    self.running = False
            if self.game_state == "playing":
                if event.type == pygame.MOUSEMOTION:
                    self.paddle.set_position((event.pos[0], self.paddle.body.position.y))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.magnetic_paddle = not self.magnetic_paddle
                    if event.key == pygame.K_a:
                        self.ai_enabled = not self.ai_enabled
                if event.type == pygame.MOUSEBUTTONDOWN and self.ball_stuck:
                    self.ball_stuck = False
                    self.ball.body.apply_impulse_at_local_point((0, -700))

    def update(self):
        if self.ai_enabled:
            # AI controls the paddle
            target_x = self.ball.body.position.x
            self.paddle.set_position((target_x, self.paddle.body.position.y))

        # Step the physics simulation
        dt = 1.0 / 60.0
        self.space.step(dt)

        # Update sprite positions from physics bodies
        self.all_sprites.update()

        if self.ball_stuck:
            self.ball.body.position = self.paddle.body.position.x, self.paddle.body.position.y - self.PADDLE_HEIGHT
            self.ball.body.velocity = 0, 0

        # Check for ball out of bounds
        if self.ball.body.position.y > self.HEIGHT:
            self._lose_life()

        # Check for level completion
        if not any(brick.breakable for brick in self.bricks_group):
            if self.sound_enabled and self.sound_effects_enabled:
                self.win_sound.play()
            self.current_level += 1
            if self.current_level > 50:
                self.game_state = "you_win"
            else:
                self.load_level(self.current_level)

    def draw(self):
        self.screen.fill(self.GRAY)

        self.all_sprites.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))


        # Draw level
        level_text = self.font.render(f"Level: {self.current_level}", True, self.WHITE)
        self.screen.blit(level_text, (self.WIDTH // 2 - 50, 10))

        # Draw lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, self.WHITE)
        self.screen.blit(lives_text, (self.WIDTH - 100, 10))

        if self.show_fps:
            fps = self.clock.get_fps()
            fps_text = self.font.render(f"FPS: {fps:.2f}", True, self.WHITE)
            self.screen.blit(fps_text, (10, self.HEIGHT - 40))

        pygame.display.flip()
