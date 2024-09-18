import pygame
import sys
from kivy.app import App
from kivy.uix.label import Label

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Paddle settings
paddle_width, paddle_height = 100, 15
paddle_speed = 15

# Ball settings
ball_size = 15
ball_speed_x = 5
ball_speed_y = 5

# Brick settings
brick_width, brick_height = 75, 20
brick_padding = 10
brick_rows, brick_cols = 5, 8

# Font settings
font = pygame.font.SysFont(None, 35)

# Initialize clock
clock = pygame.time.Clock()

def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, paddle_width, paddle_height))

def draw_ball(x, y):
    pygame.draw.ellipse(screen, WHITE, (x, y, ball_size, ball_size))

def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def main():
    # Initial positions and speeds
    paddle_x = (screen_width - paddle_width) // 2
    paddle_y = screen_height - paddle_height - 10
    ball_x, ball_y = screen_width // 2, screen_height // 2
    ball_dx, ball_dy = ball_speed_x, ball_speed_y

    # Initialize bricks
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_x = col * (brick_width + brick_padding) + 35
            brick_y = row * (brick_height + brick_padding) + 50
            bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += paddle_speed

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x <= 0 or ball_x >= screen_width - ball_size:
            ball_dx = -ball_dx
        if ball_y <= 0:
            ball_dy = -ball_dy

        # Ball collision with paddle
        if (paddle_x < ball_x + ball_size and
            paddle_x + paddle_width > ball_x and
            paddle_y < ball_y + ball_size and
            paddle_y + paddle_height > ball_y):
            ball_dy = -ball_dy

        # Ball collision with bricks
        for brick in bricks[:]:
            if (brick.left < ball_x + ball_size and
                brick.right > ball_x and
                brick.top < ball_y + ball_size and
                brick.bottom > ball_y):
                bricks.remove(brick)
                ball_dy = -ball_dy
                score += 10
                break

        screen.fill(BLACK)
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        draw_bricks(bricks)
        display_score(score)

        # Check for game over
        if ball_y >= screen_height:
            screen.fill(BLACK)
            game_over_text = font.render("Game Over! Press ESC to Quit", True, WHITE)
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2,
                                         screen_height // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

