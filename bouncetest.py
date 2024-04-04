import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

ball_radius = 20
ball_color = RED
ball_speed = 5

stationary_ball_radius = 40
stationary_ball_color = BLUE
stationary_ball_position = (WIDTH // 2, HEIGHT // 2)

ball_position = [WIDTH // 2, 0] 
ball_velocity = [0, ball_speed]
gravity = 0.1
bounce_factor = 0.8

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball_velocity[1] += gravity
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]

    #Collision
    distance = ((ball_position[0] - stationary_ball_position[0]) ** 2 + (ball_position[1] - stationary_ball_position[1]) ** 2) ** 0.5
    if distance <= ball_radius + stationary_ball_radius:
        ball_velocity[1] *= -bounce_factor

    #Balls
    pygame.draw.circle(screen, ball_color, (int(ball_position[0]), int(ball_position[1])), ball_radius)
    pygame.draw.circle(screen, stationary_ball_color, stationary_ball_position, stationary_ball_radius)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
