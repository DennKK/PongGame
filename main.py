import pygame
import sys

pygame.init()

# COLORS
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
RED = (128, 0, 0)
BLACK = (50, 50, 0)
DARK_GRAY = (120, 120, 120)

# SIZES
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

PLATFORM_WIDTH = 10
PLATFORM_HEIGHT = 100

# COORDINATES
BALL_X_POS = SCREEN_WIDTH / 2
BALL_y_POS = SCREEN_HEIGHT / 2

PLATFORM_Y_POS = 250

# VELOCITY
PLATFORM_VEL = 10

ball_speed_x = 7
ball_speed_y = 7

# PLATFORMS SCORE
platform1_score = 0
platform2_score = 0

# FONT
SCORE_FONT = pygame.font.SysFont("Courier", 30)

# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# RECTANGLES
platform1 = pygame.rect.Rect(10, PLATFORM_Y_POS, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform2 = pygame.rect.Rect(SCREEN_WIDTH - 20, PLATFORM_Y_POS, PLATFORM_WIDTH, PLATFORM_HEIGHT)

ball = pygame.Rect(BALL_X_POS, BALL_y_POS, 30, 30)

border = pygame.Rect(SCREEN_WIDTH // 2 - 2.5, 0, 5, SCREEN_HEIGHT)

# FPS
FPS = 60


def draw_window(platform1_score, platform2_score):
    screen.fill(GRAY)

    pygame.draw.rect(screen, GREEN, platform1)
    pygame.draw.rect(screen, GREEN, platform2)

    pygame.draw.rect(screen, DARK_GRAY, border)

    platform1_score_text = SCORE_FONT.render("Score: " + str(platform1_score), 1, BLACK)
    platform2_score_text = SCORE_FONT.render("Score: " + str(platform2_score), 1, BLACK)
    screen.blit(platform1_score_text, (25, 10))
    screen.blit(platform2_score_text, (SCREEN_WIDTH - platform2_score_text.get_width() - 25, 10))

    pygame.draw.ellipse(screen, RED, ball)

    pygame.display.update()


def platform1_movement(key_pressed, platform1):
    if key_pressed[pygame.K_w] and platform1.y - PLATFORM_VEL > 0:
        platform1.y -= PLATFORM_VEL

    if key_pressed[pygame.K_s] and platform1.y + PLATFORM_VEL + platform1.height < SCREEN_HEIGHT:
        platform1.y += PLATFORM_VEL


def platform2_movement(key_pressed, platform2):
    if key_pressed[pygame.K_UP] and platform2.y - PLATFORM_VEL > 0:
        platform2.y -= PLATFORM_VEL

    if key_pressed[pygame.K_DOWN] and platform2.y + PLATFORM_VEL + platform2.height < SCREEN_HEIGHT:
        platform2.y += PLATFORM_VEL


def ball_animation():

    global ball_speed_x, ball_speed_y, platform1_score, platform2_score

    # Makes the ball move
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # If the ball hits the top or bottom edge, the ball bounces
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Checks if the ball hits the platform1 and makes the ball bounce
    if ball.colliderect(platform1) and ball_speed_x < 0:
        if abs(ball.left - platform1.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - platform1.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - platform1.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    # Checks if the ball hit the platform2 and makes the ball bounce
    if ball.colliderect(platform2) and ball_speed_x > 0:
        if abs(ball.right - platform2.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - platform2.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - platform2.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    # If the ball flew away, then it returns on start position and increase platform score
    if ball.left <= 0:
        ball.x = BALL_X_POS
        ball.y = BALL_y_POS
        ball_speed_y *= -1
        platform2_score += 1
    if ball.right >= SCREEN_WIDTH:
        ball.x = BALL_X_POS
        ball.y = BALL_y_POS
        ball_speed_y *= -1
        platform1_score += 1


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key_pressed = pygame.key.get_pressed()
        platform1_movement(key_pressed, platform1)
        platform2_movement(key_pressed, platform2)

        ball_animation()

        draw_window(platform1_score, platform2_score)


if __name__ == "__main__":
    main()
