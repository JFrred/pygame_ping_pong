import pygame
import sys
import random


def paddle_left_movement():
    paddle_left.y += paddle_left_speed
    if paddle_left.top <= 0:
        paddle_left.top = 0
    if paddle_left.bottom >= screen_height:
        paddle_left.bottom = screen_height


def paddle_right_movement():
    paddle_right.y += paddle_right_speed
    if paddle_right.top <= 0:
        paddle_right.top = 0
    if paddle_right.bottom >= screen_height:
        paddle_right.bottom = screen_height


def ball_movement():
    global ball_speed_x, ball_speed_y, paddle_right_score, paddle_left_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left < 0:
        score_time = pygame.time.get_ticks()
        paddle_right_score += 1
        print(paddle_left_score, ' - ', paddle_right_score)

    if ball.right > screen_width:
        score_time = pygame.time.get_ticks()
        paddle_left_score += 1
        print(paddle_left_score, ' - ', paddle_right_score)

    if ball.colliderect(paddle_right) and ball_speed_x > 0:
        if abs(ball.right - paddle_right.left) < 10:
            ball_speed_x *= -ball_acceleration
        elif abs(ball.bottom - paddle_right.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= ball_acceleration
        elif abs(ball.top - paddle_right.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= ball_acceleration

    if ball.colliderect(paddle_left) and ball_speed_x < 0:
        if abs(ball.left - paddle_left.right) < 10:
            ball_speed_x *= -ball_acceleration
        elif abs(ball.bottom - paddle_left.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= ball_acceleration
        elif abs(ball.top - paddle_left.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= ball_acceleration


def ball_respawn():
    global ball_speed_x, ball_speed_y, score_time

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2 - ball.width / 2, screen_height/2 - ball.height / 2)

    ball_speed_y = 7 * random.choice((1, -1))
    ball_speed_x = 7 * random.choice((1, -1))
    score_time = None


def ball_color_change():
    while True:
        return random.choice(ball_colors)


pygame.init()
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 550
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ping pong game')

ball_diameter = 25
paddle_width = 20
paddle_height = 120
paddle_edge_gap = 10

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
ball_acceleration = 1.1
paddle_left_speed = 0
paddle_right_speed = 0
paddle_speed = 10

font_color = (255, 255, 255)
line_color = (255, 0, 0)
bg_color = (0, 0, 0)
ball_color = (255, 255, 255)
ball_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 255, 255), (0, 0, 0)]
paddle_left_color = (0, 255, 0)
paddle_right_color = (0, 0, 255)
menu_color = (100, 255, 180)

ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, ball_diameter, ball_diameter)
paddle_left = pygame.Rect(paddle_edge_gap, screen_height / 2 - 70, paddle_width, paddle_height)
paddle_right = pygame.Rect(screen_width - (paddle_width + paddle_edge_gap), screen_height / 2 - 70, paddle_width, paddle_height)
menu_window = pygame.Surface((screen_width - 100, screen_height - 50))


paddle_left_score = 0
paddle_right_score = 0
game_font = pygame.font.SysFont("inkfree", 50)

score_time = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # paddle_left control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_right_speed += paddle_speed
            if event.key == pygame.K_RIGHT:
                paddle_right_speed -= paddle_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                paddle_right_speed -= paddle_speed
            if event.key == pygame.K_RIGHT:
                paddle_right_speed += paddle_speed

            # paddle_right control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                paddle_left_speed += paddle_speed
            if event.key == pygame.K_a:
                paddle_left_speed -= paddle_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                paddle_left_speed -= paddle_speed
            if event.key == pygame.K_a:
                paddle_left_speed += paddle_speed

    ball_movement()
    paddle_left_movement()
    paddle_right_movement()

    screen.fill(bg_color)
    pygame.draw.rect(screen, paddle_left_color, paddle_left)
    pygame.draw.rect(screen, paddle_right_color, paddle_right)
    pygame.draw.ellipse(screen, ball_color_change(), ball)
    pygame.draw.aaline(screen, line_color, (screen_width / 2, 0), (screen_width / 2, screen_height))

    paddle_left_text = game_font.render(f"{paddle_left_score}", False, font_color)
    screen.blit(paddle_left_text, (screen_width / 2 - 40, 15))

    paddle_right_text = game_font.render(f"{paddle_right_score}", False, font_color)
    screen.blit(paddle_right_text, (screen_width / 2 + 25, 15))

    if score_time:
        ball_respawn()

    pygame.display.flip()
    clock.tick(60)
