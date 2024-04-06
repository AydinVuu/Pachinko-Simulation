import pygame
import sys
import numpy as np

width, height = 800, 600
white = (255, 255, 255)
black = (0, 0, 0)

gravity = 9.81  
radius = 20
mass = 1

class Ball:
    def __init__(self, position, velocity, radius, mass):
        self.set_pos(position)
        self.set_vel(velocity)
        self.radius = radius
        self.mass = mass

    def set_pos(self, pos):
        self.position = np.array(pos, dtype=float)

    def set_vel(self, vel):
        self.velocity = np.array(vel, dtype=float)

    def update(self, dt):
        k1v = dt * self.acceleration(self.position, self.velocity)
        k1x = dt * self.velocity
        k2v = dt * self.acceleration(self.position + 0.5 * k1x, self.velocity + 0.5 * k1v)
        k2x = dt * (self.velocity + 0.5 * k1v)
        k3v = dt * self.acceleration(self.position + 0.5 * k2x, self.velocity + 0.5 * k2v)
        k3x = dt * (self.velocity + 0.5 * k2v)
        k4v = dt * self.acceleration(self.position + k3x, self.velocity + k3v)
        k4x = dt * (self.velocity + k3v)
        self.velocity += (1/6) * (k1v + 2 * k2v + 2 * k3v + k4v)
        self.position += (1/6) * (k1x + 2 * k2x + 2 * k3x + k4x)

    def acceleration(self, position, velocity):
        return np.array([0, gravity])

    def draw(self, screen):
        pygame.draw.circle(screen, black, (int(self.position[0]), int(self.position[1])), self.radius)

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    initial_position = [width // 2, 0]
    initial_velocity = [0, 0]

    ball = Ball(initial_position, initial_velocity, radius, mass)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)
        dt = 0.05  
        ball.update(dt)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
