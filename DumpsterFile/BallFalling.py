import pygame
import sys

screen_width = 800
screen_height = 600
gravity = 9.8 
left_boundary = 100
right_boundary = 700

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Falling")

delta_t = 0.05
initial_position = (screen_width // 2, 0)
initial_velocity = 0 

class Ball:
    def __init__(self, screen, initial_position, initial_velocity, radius=20, color=(255, 0, 0)):
        self.screen = screen
        self.position = list(initial_position)
        self.velocity = initial_velocity
        self.radius = radius
        self.color = color

    def acceleration(self):
        return gravity

    def rk4(self, delta_t):
        k1v = self.acceleration()
        k1p = self.velocity
        k2v = self.acceleration()
        k2p = self.velocity + k1v * delta_t / 2
        k3v = self.acceleration()
        k3p = self.velocity + k2v * delta_t / 2
        k4v = self.acceleration()
        k4p = self.velocity + k3v * delta_t

        final_velocity = self.velocity + (k1v + 2*k2v + 2*k3v + k4v) * delta_t / 6
        final_position = (self.position[0], self.position[1] + (k1p + 2*k2p + 2*k3p + k4p) * delta_t / 6)

        return final_position, final_velocity

    def update(self, delta_t):
        self.position, self.velocity = self.rk4(delta_t)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

ball = Ball(screen, initial_position, initial_velocity)
is_ball_dropped = False
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: 
                is_ball_dropped = True
            elif event.key == pygame.K_a and not is_ball_dropped:
                if ball.position[0] - 10 >= left_boundary:
                    ball.position[0] -= 10
            elif event.key == pygame.K_d and not is_ball_dropped:  
                if ball.position[0] + 10 <= right_boundary:
                    ball.position[0] += 10

    if is_ball_dropped:
        ball.update(delta_t)

    screen.fill((255, 255, 255))
    ball.draw()
    pygame.display.flip()
    clock.tick(60)
